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

class ContentSource(Enum):
    REDDIT = "www.reddit.com"

class ProcessingStage(Enum):
    NEW          = "0_new"
    INTERESTING  = "1_interesting"
    SHORT_LISTED = "2_short_listed"
    USER_ACTION  = "3_action_suggested"
    ACTION_TAKEN = "4_action_taken"
    IGNORE       = "9_ignore"

class SocialMediaContent:
    def __init__(self,
                 id=None, url_id=None, title=None, kind=None,                
                 channel=None, parent_id=None,                
                 text=None, url=None,                
                 category=None, author=None,
                 created=None, score=None, num_comments=None, num_subscribers=None, upvote_ratio=None,   
                 # this is to satisfy everything else that may come in the dictionary that I dont care about            
                 **kwargs):
        self.id = id
        self.url_id = url_id
        self.title = title
        self.kind = kind

        self.channel = channel
        self.parent_id = parent_id

        self.text = text
        self.url = url

        self.category = category
        self.author = author
        self.created = created
        self.score = score
        self.num_comments = num_comments
        self.num_subscribers = num_subscribers
        self.upvote_ratio = upvote_ratio

    def __str__(self) -> str:
        # TODO: improve this later. currently this is for debug purpose only
        return f"id: {self.id} | channel: {self.channel} | category: {self.category} | comms: {self.num_comments} | subs: {self.num_subscribers}"

    def from_dict(vals: dict):
        return SocialMediaContent(**vals)

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
def get_contents_from_queue(stage: ProcessingStage, user_id: str, fields: [str] = None) -> list:
    #get the items from the queue
    items_in_queue = deque_content_ids(stage=stage, user_id=user_id)   
    #create query string
    if fields == None: 
        #return all fields except for system fields
        query = "SELECT VALUE c FROM c WHERE ARRAY_CONTAINS(@items_in_queue, c.id)"
    else:
        #include the fields only
        #TODO: include fields value check to avoid SQL injection
        query = "SELECT %s FROM c WHERE ARRAY_CONTAINS(@items_in_queue, c.id)" % ", ".join("c."+f for f in fields)

    params = [{"name": "@items_in_queue", "value": items_in_queue}]    
    items = reddit_container.query_items(query=query, parameters=params, enable_cross_partition_query=True)
    #returning as dict for now
    res = [item for item in items]
    return res

def que_content_ids(stage: ProcessingStage, user_id: str, source: ContentSource, content_ids: list[str]):
    que_msg = lambda x: ServiceBusMessage(json.dumps({"user_id": user_id, "source": source.value, "content_id": x}))
    msgs = list(map(que_msg, content_ids))
    queue = _select_queue(stage, "write")
    with queue:
        queue.send_messages(msgs)

def deque_content_ids(stage: ProcessingStage, user_id: str) -> list[str]:
    queue = _select_queue(stage, read_write="read")
    with queue:
        msgs = queue.peek_messages(max_message_count=config.get_max_batch_size(), timeout=config.get_max_wait_time())
        to_dict = lambda x: json.loads(str(x))
        # user_id == "*" means that this is applicable to all users or it doesnt matter who the user is
        is_of_user = lambda x: (user_id == "*") or (user_id == to_dict(x)["user_id"])
        res = [to_dict(msg)["content_id"] for msg in msgs if is_of_user(msg)]
    return res

def _select_queue(stage: ProcessingStage, read_write: str):
    if stage == ProcessingStage.NEW and read_write == "read":
        return servicebus_client.get_queue_receiver(queue_name=config.get_new_items_queue())
    elif stage == ProcessingStage.NEW and read_write == "write":
        return servicebus_client.get_queue_sender(config.get_new_items_queue())
    elif stage == ProcessingStage.INTERESTING and read_write == "read":
        return servicebus_client.get_queue_receiver(config.get_interesting_items_queue())
    elif stage == ProcessingStage.INTERESTING and read_write == "write":
        return servicebus_client.get_queue_sender(config.get_interesting_items_queue())
    elif stage == ProcessingStage.SHORT_LISTED and read_write == "read":
        return servicebus_client.get_queue_receiver(config.get_shortlisted_items_queue())
    elif stage == ProcessingStage.SHORT_LISTED and read_write == "write":
        return servicebus_client.get_queue_sender(config.get_shortlisted_items_queue())
    else:
        # TODO: remove the print. this is for debugging only 
        # this should ideally never happen
        print("Wrong values in select_queue(%s, %s)" % (stage, read_write))
        return None

def __exit__():

    servicebus_client.close()
    

__init__()