import toml

_config = toml.load("config.toml")

def get_openai_api_key() -> str:
    return _config["openai"]["OPENAI_API_KEY"]

def get_openai_org_id() -> str:
    return _config["openai"]["OPENAI_ORG_ID"]

def get_basic_model() -> str:
    return _config["openai"]["BASIC_MODEL"]

def get_assistant_model() -> str:
    return _config["openai"]["ASSISTANT_MODEL"]

def get_embeddings_model() -> str:
    return _config["openai"]["EMBEDDINGS_MODEL"]

def get_openai_max_msg_tokens() -> int:
    return _config["openai"]["MAX_TOKENS_PER_MSG"]

def get_openai_chat_context_window() -> int:
    return _config["openai"]["MAX_CHAT_CONTENT_WINDOW"]

def get_az_servicebus_connection() -> str:
    return _config["datastore"]["endpoint"]["AZ_SERVICE_BUS_CONNECTION"]

def get_new_items_queue() -> str:
    return _config["datastore"]["endpoint"]["NEW_ITEMS_QUEUE"]

def get_hot_items_queue() -> str:
    return _config["datastore"]["endpoint"]["HOT_ITEMS_QUEUE"]

def get_content_aug_queue() -> str:
    return _config["datastore"]["endpoint"]["CONTENT_AUG_QUEUE"]

def get_interesting_items_queue() -> str:
    return _config["datastore"]["endpoint"]["INTERESTING_ITEMS_QUEUE"]

def get_user_action_queue() -> str:
    return _config["datastore"]["endpoint"]["USER_ACTION_QUEUE"]

def get_az_cosmosdb_connection() -> str:
    return _config["datastore"]["endpoint"]["AZ_COSMOSDB_CONNECTION"]

def get_content_store_db() -> str:
    return _config["datastore"]["endpoint"]["CONTENT_STORE_DB"]

def get_reddit_store_container() -> str:
    return _config["datastore"]["endpoint"]["REDDIT_STORE_CONTAINER"]

def get_user_metadata_container() -> str:
    return _config["datastore"]["endpoint"]["USER_METADATA_CONTAINER"]

def get_user_action_container() -> str:
    return _config["datastore"]["endpoint"]["USER_ACTION_CONTAINER"]

def get_max_datastore_wait_time() -> int:
    return _config["datastore"]["runtime"]["MAX_WAIT_TIME"]

def get_max_datastore_batch_size() -> int:
    return _config["datastore"]["runtime"]["MAX_BATCH_SIZE"]

def get_slack_bot_token() -> int:
    return _config["slack"]["SLACK_BOT_USER_OAUTH_TOKEN"]

def get_slack_app_token() -> int:
    return _config["slack"]["SLACK_BOT_APP_LEVEL_TOKEN"]

def get_max_slack_items_to_show() -> int:
    return _config["slack"]["MAX_ITEMS_TO_SHOW"]