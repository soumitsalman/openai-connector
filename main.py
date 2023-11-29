import config
import worker_services.service_definitions as filterservice
import slack_interface.slack_client as slackbot
import social_media_datastore.dataservice as ds


# ds.update_contents_to_store([
#     {"id": "t5_2u559", "kind": "subreddit", "summary": "SR random summary", "topic": "SR  topic", "text": "SOUMIT'S RANDOM CRAP"},
#     {"id": "t3_182y2qf", "kind": "post", "summary": "POST random summary 1", "topic": "POST random topic 1"}
# ])

slackbot.start()

# workflow:
# process new items --> look for hot items and then put them in hot items queue
# process hot items --> look for interesting items and them put them in the interesting items queue & content-aug queue
# process interesting items --> slack app will take it
# process content aug items --> update content store
# NEW Items --(engagement filter)--> HOT Items --(interest filter)--> INTERESTING Items -----------------------------------> Slack app/UI
#                                                           |-------> CONTENT AUG Items --(summary generator)--> Content Store --|        




# services = [
#     filterservice.create_engagement_filtering_client(),
#     filterservice.create_interest_filtering_client("soumitsr@gmail.com"),
#     filterservice.create_summary_generation_client()
# ]

# run each service for 10 rounds
# for s in services:
#     for i in range(10):
#         s.run()


# import asyncio
# import json
# import config
# import socialmediadatastore.service as ds
# import openai_interface.tokenutils as tok
# from openai_interface.basicclient import BasicClient

# instructions = ["""You are a medical adivce assistant. 
#                 When someone has tummy ache then you will call the tummy_ache function with the users' names. 
#                 Or else (if they have some other medical issue) you will use you own knowledge base for answer and NOT call tummy_ache function"""]
# functions = [
#     {
#         "type": "function",
#         "function": {
#             "name": "tummy_ache",
#             "description": "gives medical advice and takes action for tummy ache. This function should be called ONLY when someone has tummy ache",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "names": {
#                         "type": "array",
#                         "description": "the names of the users who has tummy ache",
#                         "items": {
#                             "type": "string",
#                             "description": "each name should be a string"
#                         }
#                     }
#                 },
#                 "required": ["name"]
#             }
#         }
#     }
# ]
# msgs = [
#     #"My name is Coco and I have tummy ache, what should I do?",
#     "There are 3 friends: Jack, Jill and Bunny. Jack and Bunny has tummy ache. Jill does not have anything. What should they do?"]

# client = BasicClient(
#     api_key = config.get_openai_api_key(), 
#     org_id = config.get_openai_org_id(), 
#     instructions=instructions,
#     functions=functions
# )

# for m in msgs:
#     client.send(m)

# cosmos_client = CosmosClient.from_connection_string(config.get_az_cosmosdb_connection())

# new_items = ds._deque_content_ids(ds.ProcessingStage.NEW, "soumitsr@gmail.com")
# print("count(new_items): ", len(new_items))
# filtered_items = [i for i in new_items if random.randint(1, 21)%3 == 0]
# print("count(filtered_items)", len(filtered_items))
# ds._que_content_ids(stage = ds.ProcessingStage.INTERESTING, user_id = "soumitsr@gmail.com", source = "www.reddit.com", content_ids=filtered_items)


# msgs = [
#     "Who own world war 2",
#     "Who lost it",
#     "What are the long term implications of this",
#     "Is there going to be a ww 3",
#     "what should we do to avoid one"
# ] * 1000

# client = BasicClient(config.get_openai_api_key(), config.get_openai_org_id(), "You are a world war 2 expert")
# for msg in msgs:
#     print(client.send(msg))

#collect data


#connect to openai


# functions = [
#     {
#         "type": "function",
#         "function": {
#             "name": "save_interesting_items",
#             "description": "This function takes a list of 'id' of interesting items and saves them into a database",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "item_ids": {
#                         "type": "array",
#                         "description": "list of ids of items that are interesting",
#                         "items": {
#                             "type": "string"
#                         }
#                     }
#                 },
#                 "required": ["item_ids"]
#             }
#         }
#     }
# ]





