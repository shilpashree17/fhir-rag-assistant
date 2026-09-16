from typing import Any, Dict, List


class RAGPipeline:
    def __init__(self, fhir_client: Any, llm_client: Any):
        self.fhir_client = fhir_client
        self.llm_client = llm_client

    def build_context(self, patient_id: str) -> Dict[str, Any]:
        patient = self.fhir_client.get_patient(patient_id)
        return {"patient": patient}

    def answer_question(self, patient_id: str, question: str) -> str:
        context = self.build_context(patient_id)
        prompt = (
            "You are a clinical assistant. Use the patient context to answer the user question.\n\n"
            f"Patient context: {context}\n\nUser question: {question}"
        )
        return self.llm_client.generate(prompt)
