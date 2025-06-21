from pymongo import MongoClient
import redis
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.mongo_client = None
        self.db = None
        self.redis_client = None
        self.connect()
    
    def connect(self):
        try:
            # MongoDB connection
            print("🔄 Connecting to MongoDB...")
            self.mongo_client = MongoClient(os.getenv('MONGODB_URI'))
            self.db = self.mongo_client[os.getenv('DATABASE_NAME')]
            
            # Test MongoDB connection (FIXED)
            self.mongo_client.admin.command('ping')
            print("✅ MongoDB connected successfully!")
            
            # Redis connection
            print("🔄 Connecting to Redis...")
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                password=os.getenv('REDIS_PASSWORD'),
                decode_responses=True
            )
            
            # Test Redis connection
            self.redis_client.ping()
            print("✅ Redis connected successfully!")
            
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            print("🔍 Check your .env file settings")
            print("📝 Your .env should look like:")
            print("   MONGODB_URI=mongodb+srv://username:password@cluster...")
            print("   REDIS_HOST=redis-xxxxx.cloud.redislabs.com")
            print("   REDIS_PASSWORD=your-password")
    
    def save_message(self, message, user="Anonymous"):
        """Save message to MongoDB"""
        try:
            message_doc = {
                "message": message,
                "user": user,
                "timestamp": datetime.now()
            }
            
            result = self.db.messages.insert_one(message_doc)
            
            # Also cache in Redis
            self.redis_client.lpush('recent_messages', f"{user}: {message}")
            self.redis_client.ltrim('recent_messages', 0, 9)  # Keep last 10
            
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
    
    def get_messages(self, limit=10):
        """Get messages from database"""
        try:
            messages = list(self.db.messages.find().sort("timestamp", -1).limit(limit))
            
            # Convert for JSON
            for msg in messages:
                msg['_id'] = str(msg['_id'])
                msg['timestamp'] = msg['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            
            return messages
            
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
    
    def get_cached_messages(self):
        """Get recent messages from Redis cache"""
        try:
            return self.redis_client.lrange('recent_messages', 0, -1)
        except Exception as e:
            print(f"Error getting cached messages: {e}")
            return []