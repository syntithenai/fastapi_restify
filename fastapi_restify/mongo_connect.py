from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

class MongoConnect():
    db_client: AsyncIOMotorClient = None

    async def get_db_client(self) -> AsyncIOMotorClient:
        """Return database client instance."""
        if self.db_client is None:
            await self.connect_db()
        return self.db_client


    async def connect_db(self, db_url = None):
        """Create database connection."""
        connect_string = config('MONGO_URI')
        if db_url is not None:
            connect_string = db_url
        self.db_client = AsyncIOMotorClient(connect_string)

    async def close_db(self):
        """Close database connection."""
        self.db_client.close()

mongo_connect = MongoConnect()
