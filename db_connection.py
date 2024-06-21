import os
import time
from uuid import uuid4

from azure.cosmos import CosmosClient
from dotenv import load_dotenv


class Goal:

    def __init__(self, color):
        self.color = color
        self.timestamp = time.time()
        self.id = str(uuid4())

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "color": self.color,
            "timestamp": self.timestamp
        }


class Storage:
    def __init__(self):
        load_dotenv()
        self.client = CosmosClient(url=os.environ.get("DB_URL"), credential=os.environ.get("FEED_KEY"))
        self.database = self.client.get_database_client("kicker_statistik")
        self.container = self.database.get_container_client("kicker_statistik")

    def save_goal(self, goal_info: Goal):
        self.container.upsert_item(goal_info.to_json())
        print("Saving goal...")
