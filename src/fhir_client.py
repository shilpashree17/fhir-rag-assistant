import requests

FHIR_URL = "https://r4.smarthealthit.org"    # Replace with your FHIR server URL

def get(resource, params=""):
    url=f"{FHIR_URL}/{resource}?{params}"
    response =requests.get(url, headers={"Accept": "application/fhir+json"})
    response.raise_for_status()
    return response.json()

def get_patient_context(patient_id):
    '''Pull a patients conditions and observations, return as plain text chunks for RAG'''
    conditions=get("Condition",f"patient={patient_id}")
    observations=get("Observation",f"patient={patient_id}")
    chunks=[]
    for entry in conditions.get("entry",[]):
        text=entry["resource"].get("code",{}).get("text")
        if text:
            chunks.append(f"Condition: {text}")

    for entry in observations.get("entry",[]):
        code=entry["resource"].get("code",{}).get("text","Observation")
        value=entry["resource"].get("valueQuantity",{}).get("value")
        unit=entry["resource"].get("valueQuantity",{}).get("unit")
        if value is not None:
            chunks.append(f"Observation: {code} ={value} {unit}".strip())

    return chunks

if __name__ == "__main__":
    test_ids= ["2d95f315-808c-4b67-836b-e56bdba9dd21","59d572ce-0c47-434e-8fe6-2aa79c0f1139","786ec762-c52d-4f65-bd73-0119a0184e80","9462ff5c-47c8-4e46-a180-1cac0a2003c4","27f12f19-ede7-4432-98d6-659b5201c9fa"]
    for test_id in test_ids:
        print(f"patient_id:{test_id} name = {requests.get(f'{FHIR_URL}/Patient/{test_id}').json().get('name','Unknown')}\n \t conditions and observations : \n\t\t {get_patient_context(test_id)} \n")
