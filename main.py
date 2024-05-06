import json

from fastapi import FastAPI, HTTPException
from models import Patient

with open("patients.json", "r") as f:
    patient_list = json.load(f)

# Use the first name as the unique identifier. For example, in the PUT route, you'd have something like this: "/patients/{first_name}"

app = FastAPI()

patients = {patient["first_name"]: patient for patient in patient_list}


@app.get("/patients/")
async def get_patient() -> dict:
    return patients


@app.post("/patients")
async def create_patient(patient: Patient) -> Patient:
    if patient.first_name in patients:
        raise HTTPException(status_code=400, detail="Patient already exists")
    else:
        patients[patient.first_name] = patient
        return patient


@app.put("/patients/{first_name}")
async def update_patient(first_name: str, patient: Patient) -> Patient:
    if first_name not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        patients[first_name] = patient
        return patient
    


@app.delete("/patients/{first_name}")
async def delete_patient(first_name: str) -> dict:
    if first_name not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        del patients[first_name]
        return patients