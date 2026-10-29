from knowledge_base import SmartKnowledgeBase

class SelfHealingAgent:
    def __init__(self):
        self.kb = SmartKnowledgeBase(collection_name="feature_requirements_kb")

    def diagnose_test_failure(self, test_name: str, error_trace: str):
        print(f"\n[Self-Healing Agent] Analyzing failure in test: '{test_name}'")
        
        search_query = f"{test_name} {error_trace}"
        relevant_docs = self.kb.find_relevant_information(search_query, max_results=1)
        
        context_summary = "No specific requirement ticket found."
        if relevant_docs and relevant_docs['documents'][0]:
            context_summary = relevant_docs['documents'][0][0]
            matched_file = relevant_docs['metadatas'][0][0].get('source_file', 'unknown')
            print(f"[Self-Healing Agent] Found matching requirement context from: {matched_file}")

        diagnosis = (
            f"Failure analyzed for '{test_name}'. "
            f"Checked against system requirements. Relevant Context Found:\n{context_summary}"
        )
        
        return {
            "testName": test_name,
            "diagnosis": diagnosis,
            "status": "healing_in_progress"
        }

if __name__ == "__main__":
    agent = SelfHealingAgent()
    result = agent.diagnose_test_failure(
        test_name="Checkout Flow Validation",
        error_trace="Element not clickable at checkout confirmation button."
    )
    print("\n--- Agent Diagnosis Report ---")
    for key, value in result.items():
        print(f"{key}: {value}")