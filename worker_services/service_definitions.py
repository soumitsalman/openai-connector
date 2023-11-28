import social_media_datastore.service as ds
from worker_services.content_processing_service_client import ContentProcessingServiceClient
       
        
# service definitions
# filters which item matches a users interests
def create_text_filtering_client(user_id: str) -> ContentProcessingServiceClient:
    areas_of_interests = ds.get_user_interests(user_id)
    instructions = [
        """You are a content filtering function. 
        You filter through social media contents like reddit posts, subreddits or comments and save the items that matches the users interests.
        
        The user will give you a list  domains that the user is interested in followed by a list social media contents like reddit posts, subreddits or comments. 
        You will filter through these contents to determine which ones match the user's interest.
        Then you will return the ONLY the ids of these items formatted as a list of json array of string.
        If there is no content that matches the users interest you will respond 'None'.
        You will NOT prefix or append any additional text to the respose

        Each list of social media contents will be formatted as a list of json objects. Each json object will have the following fields
        - id: a string that specifies the unique id of the social media content
        - kind: indicates whether this is a subreddit, post or comment
        - channel: the short name of a subreddit a post or comment belongs to. If kind == subreddit then this is the short name of the subreddit itself
        - title: title of the social media content. This may potentially be empty or missing for comments
        - text: the text material of the social media content. In case of subreddit this is description content. In case of posts or comments this is the text content""",
    ]
    prompt = "I am interested in different domains like %s. Which of the following items match my interest. Give me the ids ONLY" % (",".join(areas_of_interests))

    def collect():
        # TODO: change the queue
        return ds.get_contents_from_queue(ds.ProcessingStage.NEW, user_id=user_id, fields=["id", "kind", "text", "channel", "title"])
    def save(filtered_items):
        # TODO: change the queue
        ds.que_content_ids(ds.ProcessingStage.INTERESTING, user_id, ds.ContentSource.REDDIT, filtered_items)
    
    client = ContentProcessingServiceClient(user_id=user_id, instructions=instructions, prompt=prompt, collect_func=collect, save_func=save)
    return client

# filters hot items. no user id needed for this one
def create_hot_filtering_client() -> ContentProcessingServiceClient:
    instructions = [
        """You are a content filtering function. 
        You filter through social media contents like reddit posts, subreddits or comments and save the items that matches the users interests.
        
        The user will give you a list  domains that the user is interested in followed by a list social media contents like reddit posts, subreddits or comments. 
        You will filter through these contents to determine which ones have high engagement form other users.
        Then you will return the rank ordered list of the items based their engagement level with the highest engagement first and the lowest engagement last.
        You will ONLY return the ids of these items formatted as a list of json array of string.
        If there is no content that are of high engagement you will respond 'None'.
        You will NOT prefix or append any additional text to the respose

        Each list of social media contents will be formatted as a list of json objects. Each json object will have the following fields
        - id: a string that specifies the unique id of the social media content
        - kind: indicates where this is a subreddit, post or comment
        - title: title of the social media content. This may potentially be empty or missing for comments
        - score: This is optional. applies ONLY to items with kind == post or kind == comment. Indicates the current score provided by the social media platform. The higher the value the better
        - num_comments: This is optional. Indicates the number of user who have already made a comment to that item. The higher the better.
        - num_subscribers: This is optional. applies ONLY to items with kind == subreddit. Indicates the number of subscibers in that subreddit. The higher the better
        - upvote_ratio: This is optional. applies ONLY to items with kind == post or kind == comment. Indicates the ratio between likes vs total likes + dislikes. The higher the better.
        - created: indicates the floating point representation of the time the item was created. the newer the better""",
    ]
    prompt = "Which of the following items are of high engagement. Give me the ids ONLY"

    def collect():
        # TODO: change the queue
        return ds.get_contents_from_queue(ds.ProcessingStage.NEW, user_id="*", fields=["id", "kind", "title", "score", "num_comments", "num_subscribers", "upvote_ratio", "created"])
    def save(filtered_items):
        # TODO: change the queue
        ds.que_content_ids(ds.ProcessingStage.SHORT_LISTED, "*", ds.ContentSource.REDDIT, filtered_items)
    client = ContentProcessingServiceClient(user_id="*", instructions=instructions, prompt=prompt, collect_func= collect, save_func=save)    
    return client

# TODO: create summary and slack definition generator