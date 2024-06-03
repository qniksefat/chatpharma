import os
from azure.identity.aio import DefaultAzureCredential
from .cosmosdbservice import CosmosConversationClient
import logging
from asyncio import Lock

# Chat History CosmosDB Integration Settings
AZURE_COSMOSDB_DATABASE = os.environ.get("AZURE_COSMOSDB_DATABASE")
AZURE_COSMOSDB_ACCOUNT = os.environ.get("AZURE_COSMOSDB_ACCOUNT")
AZURE_COSMOSDB_CONVERSATIONS_CONTAINER = os.environ.get("AZURE_COSMOSDB_CONVERSATIONS_CONTAINER")
AZURE_COSMOSDB_ACCOUNT_KEY = os.environ.get("AZURE_COSMOSDB_ACCOUNT_KEY")
AZURE_COSMOSDB_ENABLE_FEEDBACK = os.environ.get("AZURE_COSMOSDB_ENABLE_FEEDBACK", "false").lower() == "true"
CHAT_HISTORY_ENABLED = AZURE_COSMOSDB_ACCOUNT and AZURE_COSMOSDB_DATABASE and AZURE_COSMOSDB_CONVERSATIONS_CONTAINER

class CosmosDBClientSingleton:
    _instance = None
    _lock = Lock()

    @classmethod
    async def get_instance(cls):
        async with cls._lock:
            if cls._instance is None:
                logging.info("Creating new CosmosDB client instance")
                cls._instance = await cls._create_client()
            else:
                logging.info("Reusing existing CosmosDB client instance")
        return cls._instance

    @classmethod
    async def _create_client(cls):
        if not CHAT_HISTORY_ENABLED:
            logging.debug("CosmosDB not configured")
            return None

        try:
            cosmos_endpoint = f"https://{AZURE_COSMOSDB_ACCOUNT}.documents.azure.com:443/"
            credential = DefaultAzureCredential() if not AZURE_COSMOSDB_ACCOUNT_KEY else AZURE_COSMOSDB_ACCOUNT_KEY

            client = CosmosConversationClient(
                cosmosdb_endpoint=cosmos_endpoint,
                credential=credential,
                database_name=AZURE_COSMOSDB_DATABASE,
                container_name=AZURE_COSMOSDB_CONVERSATIONS_CONTAINER,
                enable_message_feedback=AZURE_COSMOSDB_ENABLE_FEEDBACK,
            )
            return client
        except Exception as e:
            logging.exception("Exception in CosmosDB initialization")
            return None

async def get_cosmosdb_client():
    return await CosmosDBClientSingleton.get_instance()

