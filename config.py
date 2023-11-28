import toml

config = toml.load("config.toml")

def get_openai_api_key() -> str:
    return config["openai"]["OPENAI_API_KEY"]

def get_openai_org_id() -> str:
    return config["openai"]["OPENAI_ORG_ID"]

def get_basic_model() -> str:
    return config["openai"]["BASIC_MODEL"]

def get_assistant_model() -> str:
    return config["openai"]["ASSISTANT_MODEL"]

def get_embeddings_model() -> str:
    return config["openai"]["EMBEDDINGS_MODEL"]

def get_max_msg_tokens() -> int:
    return config["openai"]["MAX_MSG_TOKENS"]

def get_context_window() -> int:
    return config["openai"]["MAX_CONTEXT_WINDOW"]

def get_az_servicebus_connection() -> str:
    return config["datastore"]["endpoint"]["AZ_SERVICE_BUS_CONNECTION"]

def get_new_items_queue() -> str:
    return config["datastore"]["endpoint"]["NEW_ITEMS_QUEUE"]

def get_interesting_items_queue() -> str:
    return config["datastore"]["endpoint"]["INTERESTING_ITEMS_QUEUE"]

def get_shortlisted_items_queue() -> str:
    return config["datastore"]["endpoint"]["SHORTLISTED_ITEMS_QUEUE"]

def get_az_cosmosdb_connection() -> str:
    return config["datastore"]["endpoint"]["AZ_COSMOSDB_CONNECTION"]

def get_content_store_db() -> str:
    return config["datastore"]["endpoint"]["CONTENT_STORE_DB"]

def get_reddit_store_container() -> str:
    return config["datastore"]["endpoint"]["REDDIT_STORE_CONTAINER"]

def get_user_metadata_container() -> str:
    return config["datastore"]["endpoint"]["USER_METADATA_CONTAINER"]

def get_user_action_container() -> str:
    return config["datastore"]["endpoint"]["USER_ACTION_CONTAINER"]

def get_max_wait_time() -> int:
    return config["datastore"]["runtime"]["MAX_WAIT_TIME"]

def get_max_batch_size() -> int:
    return config["datastore"]["runtime"]["MAX_BATCH_SIZE"]
