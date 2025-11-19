import pickle
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="loan-approval")

# load the model with pickle
with open("model.bin", "rb") as f_in:
    pipeline = pickle.load(f_in)

@app.post("/predict")
def predict_status(customer: Dict[str, Any]):
    loan_status = pipeline.predict_proba(customer)[:, 1]
    loan_status = float(loan_status[0])
    return {
        "loan probability": loan_status,
        "approved" : bool(loan_status >= 0.5)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)