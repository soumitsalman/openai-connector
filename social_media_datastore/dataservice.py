import logging
import config
import json
from azure.cosmos import CosmosClient
from azure.servicebus import ServiceBusClient,  ServiceBusMessage
from enum import Enum

reddit_container = None
user_metadata_container = None
user_action_container = None
servicebus_client = None

ALL_USERS = "*"

# different actions you can take on a media item
class UserActionType(Enum):    
    SUBSCRIBE = "sub"
    UNSUBSCRIBE = "unsub"
    COMMENT = "comment"
    LIKE = "upvote"
    DISLIKE = "downvote"
    TRASH = "trash"

# what are the define media content sources
class ContentSource(Enum):
    REDDIT = "www.reddit.com"

# what are the difference processing stages
class ProcessingStage(Enum):
    NEW          = "new"    
    HOT = "hot"
    CONTENT_AUG = "content_aug"
    INTERESTING  = "interesting"
    _USER_ACTION  = "3_action_suggested"
    _ACTION_TAKEN = "4_action_taken"
    _IGNORE       = "9_ignore"

# TODO: deprecate. this isn't really needed. dictory works better
# class SocialMediaContent:
#     def __init__(self,
#                  id=None, url_id=None, title=None, kind=None,                
#                  channel=None, parent_id=None,                
#                  text=None, url=None,                
#                  category=None, author=None,
#                  created=None, score=None, num_comments=None, num_subscribers=None, upvote_ratio=None,   
#                  # this is to satisfy everything else that may come in the dictionary that I dont care about            
#                  **kwargs):
#         self.id = id
#         self.url_id = url_id
#         self.title = title
#         self.kind = kind

#         self.channel = channel
#         self.parent_id = parent_id

#         self.text = text
#         self.url = url

#         self.category = category
#         self.author = author
#         self.created = created
#         self.score = score
#         self.num_comments = num_comments
#         self.num_subscribers = num_subscribers
#         self.upvote_ratio = upvote_ratio

#     def __str__(self) -> str:
#         # TODO: improve this later. currently this is for debug purpose only
#         return f"id: {self.id} | channel: {self.channel} | category: {self.category} | comms: {self.num_comments} | subs: {self.num_subscribers}"

#     def from_dict(vals: dict):
#         return SocialMediaContent(**vals)

def __init__():
    cosmos_client = CosmosClient.from_connection_string(config.get_az_cosmosdb_connection())
    db = cosmos_client.get_database_client(config.get_content_store_db())
    global reddit_container 
    reddit_container = db.get_container_client(config.get_reddit_store_container())
    global user_action_container 
    user_action_container = db.get_container_client(config.get_user_action_container())
    global user_metadata_container
    user_metadata_container = db.get_container_client(config.get_user_metadata_container())
    global servicebus_client
    servicebus_client = ServiceBusClient.from_connection_string(conn_str = config.get_az_servicebus_connection(), logging_enable=True)

def get_user_interests(user_id: str) -> list[str]:
    query = "SELECT c.interests FROM c WHERE c.user_id = @user_id"
    params = [{"name": "@user_id", "value": user_id}]    
    items = user_metadata_container.query_items(query=query, parameters=params, enable_cross_partition_query=True)
    res = [item["interests"] for item in items]
    #there is no record. so return an empty array
    if len(res) == 0:
        return []
    else:
        #this will return an array of array. so just take the first item
        return res[0]

# returns max_batch_size number of contents or less. If you need to empty the queue, keep calling this
def get_contents_for_processing(stage: ProcessingStage, user_id: str, fields: [str] = None, max_items: int = config.get_max_batch_size()) -> list:
    #get the items from the queue
    items_in_queue = deque_content_ids(stage=stage, user_id=user_id, max_items = max_items)   
    return get_contents_from_store(items_in_queue, fields=fields)    

def get_contents_from_store(content_ids: list[str], fields: [str] = None) -> list:
    #create query string
    if fields == None: 
        #return all fields except for system fields
        query = "SELECT VALUE c FROM c WHERE ARRAY_CONTAINS(@items_in_queue, c.id)"
    else:
        #include the fields only
        #TODO: include fields value check to avoid SQL injection
        query = f"SELECT {', '.join('c.'+f for f in fields)} FROM c WHERE ARRAY_CONTAINS(@items_in_queue, c.id)"

    params = [{"name": "@items_in_queue", "value": content_ids}]    
    items = reddit_container.query_items(query=query, parameters=params, enable_cross_partition_query=True)
    #returning as dict for now
    res = [item for item in items]
    return res

# updates content fields in the store. values MUST contain id field and the kind field to denote the item
def update_contents_to_store(values: list[dict]):
    for val in values:
        operations = [{"op": "add", "path": f"/{field}", "value": fval} for field, fval in val.items() if field not in ["id", "kind"]]
        reddit_container.patch_item(item=val["id"], partition_key=val['kind'], patch_operations=operations)

def que_content_ids(stage: ProcessingStage, user_id: str, source: ContentSource, content_ids: list[str]):
    que_msg = lambda x: ServiceBusMessage(json.dumps({"user_id": user_id, "source": source.value, "content_id": x}))
    msgs = list(map(que_msg, content_ids))
    queue = _select_queue(stage, "write")
    with queue:
        queue.send_messages(msgs)
    # TODO: remove this
    print(f"[DEBUG MSG] {len(content_ids)} items QUEued for {user_id} in {stage.value} items")

def deque_content_ids(stage: ProcessingStage, user_id: str, max_items = config.get_max_batch_size()) -> list[str]:
    queue = _select_queue(stage, read_write="read")
    with queue:
        received = queue.receive_messages(max_message_count=max_items, max_wait_time=config.get_max_wait_time())
        to_dict = lambda x: json.loads(str(x))
        # user_id == "*" means that this is applicable to all users or it doesnt matter who the user is
        # so either the query wants data about any user item OR data available is for every user OR query matches the user id in the queue
        is_of_user = lambda x: (user_id == "*") or (to_dict(x).get("user_id", "*") == "*") or (user_id == to_dict(x).get("user_id", "*"))
        filtered = [msg for msg in received if is_of_user(msg)]
        # mark these as complete
        [queue.complete_message(msg) for msg in filtered]
        
    # TODO: remove this
    print(f"[DEBUG MSG] {len(filtered)} items DE-queued for {user_id} from {stage.value} items")
    # retrieve the content ids and return the result     
    return [to_dict(msg)["content_id"] for msg in filtered]

def _select_queue(stage: ProcessingStage, read_write: str):
    if stage == ProcessingStage.NEW and read_write == "read":
        return servicebus_client.get_queue_receiver(queue_name=config.get_new_items_queue())
    elif stage == ProcessingStage.NEW and read_write == "write":
        return servicebus_client.get_queue_sender(config.get_new_items_queue())
    elif stage == ProcessingStage.HOT and read_write == "read":
        return servicebus_client.get_queue_receiver(config.get_hot_items_queue())
    elif stage == ProcessingStage.HOT and read_write == "write":
        return servicebus_client.get_queue_sender(config.get_hot_items_queue())
    elif stage == ProcessingStage.INTERESTING and read_write == "read":
        return servicebus_client.get_queue_receiver(config.get_interesting_items_queue())
    elif stage == ProcessingStage.INTERESTING and read_write == "write":
        return servicebus_client.get_queue_sender(config.get_interesting_items_queue())
    elif stage == ProcessingStage.CONTENT_AUG and read_write == "read":
        return servicebus_client.get_queue_receiver(config.get_content_aug_queue())
    elif stage == ProcessingStage.CONTENT_AUG and read_write == "write":
        return servicebus_client.get_queue_sender(config.get_content_aug_queue())
    else:
        # TODO: remove the print. this is for debugging only 
        # this should ideally never happen
        print("Wrong values in select_queue(%s, %s)" % (stage, read_write))
        return None

def __exit__():

    servicebus_client.close()
    

__init__()