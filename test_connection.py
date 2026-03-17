from dotenv import load_dotenv
import os
import pymongo
import certifi

# Check .env location
env_path = os.path.join(os.getcwd(), '.env')
print("Looking for .env at:", env_path)
print(".env file exists:", os.path.exists(env_path))

# Load .env
load_dotenv(dotenv_path=env_path, override=True)

# Get URL
url = os.getenv("MONGO_DB_URL")
print("URL loaded:", url)

# Check URL
if not url:
    print("PROBLEM: URL is None - .env not loading")
elif "localhost" in url:
    print("PROBLEM: Still using localhost - update .env file")
else:
    print("URL looks good - testing Atlas connection...")
    try:
        client = pymongo.MongoClient(
            url,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )
        client.admin.command("ping")
        print("SUCCESS - MongoDB Atlas connected!")
    except Exception as e:
        print("FAILED:", str(e))