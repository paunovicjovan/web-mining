import os
from dotenv import load_dotenv
from fastapi import FastAPI
from src.data.loader import run_offline_preprocessing

# Load environment variables
load_dotenv()

def initialize_data():
    """Ensure the cleaned dataset exists before starting the app."""
    raw_csv = "data/Amazon_Unlocked_Mobile.csv"
    cleaned_csv = "data/cleaned_reviews.csv"
    
    if not os.path.exists(cleaned_csv):
        print("Cleaned dataset not found. Starting offline preprocessing...")
        if os.path.exists(raw_csv):
            run_offline_preprocessing(raw_csv, cleaned_csv)
        else:
            print(f"CRITICAL ERROR: Raw dataset {raw_csv} not found!")
            return False
    else:
        print("Cleaned dataset already exists. Skipping preprocessing.")
    return True

# Initialize data
data_ready = initialize_data()

app = FastAPI(title="Phone Review Analysis API")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Phone Review Analysis API",
        "data_ready": data_ready
    }

@app.get("/status")
async def get_status():
    return {"status": "online" if data_ready else "error_no_data"}

if __name__ == "__main__":
    import uvicorn
    # If we are running this as a script, we might want to ensure data is ready
    if data_ready:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        print("Application could not start due to missing data.")