import social_media_datastore.dataservice as ds
from worker_services.content_processing_service_client import ContentProcessingServiceClient
       
        
# service definitions
# filters which item matches a users interests
# it looks into HOT items queue, finds interesting items and inserts into both INTERESTING items queue and CONTENT AUG queue
def create_interest_filtering_client(user_id: str) -> ContentProcessingServiceClient:
    areas_of_interests = ds.get_user_interests(user_id)
    instructions = [
        """You are a content filtering function. 
        You filter through social media contents like reddit posts, subreddits or comments and save the items that matches the users interests.
        
        The user will give you a list domains that the user is interested in.
        Then the user will give you a list social media contents like reddit posts, subreddits or comments. 
        You will filter through these contents to determine which ones match the user's interest.
        Then you will return the ids of these items. Output format should be an array of string as per JSON schema.
        If there is no content that matches the users interest you will respond 'None'.
        You will NOT prefix or append any additional content to the respose that violates the JSON schema

        Each list of social media contents will be formatted as a list of json objects. Each json object will have the following fields
        - id: a string that specifies the unique id of the social media content
        - kind: indicates whether this is a subreddit, post or comment
        - channel: the short name of a subreddit a post or comment belongs to. If kind == subreddit then this is the short name of the subreddit itself
        - title: title of the social media content. This may potentially be empty or missing for comments
        - text: the text material of the social media content. In case of subreddit this is description content. In case of posts or comments this is the text content""",
    ]
    prompt = f"I am interested in different domains like {(', '.join(areas_of_interests))}. Which of the following items match my interest. Give me the ids ONLY. Make sure the output is parsable through python json.loads() function"

    # collector function: from HOT items
    def collect():
        return ds.get_contents_for_processing(ds.ProcessingStage.HOT, user_id=user_id, fields=["id", "kind", "text", "channel", "title"])
    # save function: saves into both INTERESTING items queue and CONTENT AUG queue
    def save(filtered_items):
        ds.que_content_ids(ds.ProcessingStage.INTERESTING, user_id, ds.ContentSource.REDDIT, filtered_items)
        ds.que_content_ids(ds.ProcessingStage.CONTENT_AUG, "*", ds.ContentSource.REDDIT, filtered_items)
    
    client = ContentProcessingServiceClient(instructions=instructions, prompt=prompt, collect_func=collect, save_func=save, process_name="<interest_filtering>")
    return client

# filters hot items. no user id needed for this one
# this service looks into NEW ITEMS queue and determines which ones are hot and inserts them in HOT Items queue
def create_engagement_filtering_client() -> ContentProcessingServiceClient:
    instructions = [
        """You are a content filtering function. 
        You filter through social media contents like reddit posts and subreddits and decide what is generating high engagement.
        
        The user will give you a list social media contents like reddit posts and subreddits. 
        You will filter through these contents to determine which ones have high engagement form other users.
        Then you will return the rank ordered list of the items based their engagement level with the highest engagement first and the lowest engagement last.
        You will ONLY return the ids of these items. Output format should an array of string as per JSON schema
        If there is no content that are of high engagement you will respond 'None'.
        You will NOT prefix or append any additional content to the respose that violates the JSON schema

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
    prompt = "Which of the following items are of high engagement. Give me the ids ONLY. Make sure the output is parsable through python json.loads() function"

    # collector function: from NEW Items
    def collect():
        return ds.get_contents_for_processing(ds.ProcessingStage.NEW, user_id="*", fields=["id", "kind", "title", "score", "num_comments", "num_subscribers", "upvote_ratio", "created"])
    # save function: to HOT items
    def save(filtered_items):
        ds.que_content_ids(ds.ProcessingStage.HOT, "*", ds.ContentSource.REDDIT, filtered_items)

    client = ContentProcessingServiceClient(instructions=instructions, prompt=prompt, collect_func= collect, save_func=save, process_name="<hot filtering>")    
    return client

# filters hot items. no user id needed for this one
def create_summary_generation_client() -> ContentProcessingServiceClient:
    instructions = [
        """You are a content summary and topic generation function. 
        You look through social media contents like reddit posts and subreddits determine a topic (3 words maximum) and content summary (100 words max).
        
        The user will give you a list of social media contents like reddit posts and subreddits. 
        You will process through each of these contents to generate the topic and summary.
        Topic should be 3 words or less. Summary should be 100 words or less. 
        Output format should be array of json objects as per JSON schema. Each object should contain the following fields:
        - id: provided with the user content
        - kind: provided with the user content
        - topic: generated content
        - summary: generated content
        You will NOT prefix or append any additional content to the respose that violates the JSON schema

        Each list of social media contents will be formatted as a list of json objects. Each json object will have the following fields
        - id: a string that specifies the unique id of the social media content
        - kind: indicates whether this is a subreddit, post or comment
        - channel: the short name of a subreddit a post or comment belongs to. If kind == subreddit then this is the short name of the subreddit itself
        - title: title of the social media content. This may potentially be empty or missing for comments
        - text: the text material of the social media content. In case of subreddit this is description content. In case of posts or comments this is the text content""",
    ]
    prompt = "Generate the summary and topic of the following social media items. For each item give me the 'id', 'kind', 'topic' and 'summary'. Make sure the output is parsable through python json.loads() function"

    # collector function: from CONTENT AUG queue
    def collect():
        # TODO: change the queue
        return ds.get_contents_for_processing(ds.ProcessingStage.CONTENT_AUG, user_id="*", fields=["id", "kind", "title", "text", "channel"])
    # saves it directly in the content store
    def save(filtered_items):
        # update in place in the storage
        ds.update_contents_to_store(filtered_items)
        # no need to queue for someone to pick up from any specific queue
    
    client = ContentProcessingServiceClient(instructions=instructions, prompt=prompt, collect_func= collect, save_func=save, process_name="<summary generator>")    
    return client
