import os
from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables
load_dotenv()

def check_db_ready():
    """Ensure the database exists before starting the app."""
    db_path = os.path.join("data", "reviews.db")
    if os.path.exists(db_path):
        print(f"Database found at {db_path}.")
        return True
    else:
        print(f"CRITICAL ERROR: Database {db_path} not found!")
        return False

# Check data readiness
data_ready = check_db_ready()

app = FastAPI(title="Phone Review Analysis API")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Phone Review Analysis API",
        "data_ready": data_ready
    }

@app.get("/status")
async def get_status():
    return {"status": "online" if data_ready else "error_no_db"}

if __name__ == "__main__":
    import uvicorn
    # Start the app if data is ready
    if data_ready:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        print("Application could not start due to missing database.")