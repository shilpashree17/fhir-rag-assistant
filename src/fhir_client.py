import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class FHIRClient:
    def __init__(self, base_url: Optional[str] = None, access_token: Optional[str] = None):
        self.base_url = (base_url or os.getenv("FHIR_BASE_URL", "")).rstrip("/")
        self.access_token = access_token or os.getenv("FHIR_ACCESS_TOKEN")
        self.session = requests.Session()

        if self.access_token:
            self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

    def get_patient(self, patient_id: str) -> Dict[str, Any]:
        if not self.base_url:
            raise ValueError("FHIR_BASE_URL is not configured.")

        url = f"{self.base_url}/Patient/{patient_id}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def search_patients(self, query: str) -> Dict[str, Any]:
        if not self.base_url:
            raise ValueError("FHIR_BASE_URL is not configured.")

        url = f"{self.base_url}/Patient"
        params = {"name": query}
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
