from knowledge_base import SmartKnowledgeBase

def verify_knowledge_base():
    print("Initializing Smart Knowledge Base for Verification...")
    
    # Initialize using our clean, non-technical class name
    kb = SmartKnowledgeBase(collection_name="qa_testbed")

    # Sample data mimicking your QA test logs or documents
    sample_texts = [
        "cart checkout has been completed with registration flow.",
        "Error trace detected: element not clickable at point x, y.",
        "Self-healing agent automatically updates XPath selectors on UI failure."
    ]
    sample_metadata = [
        {"module": "cart"},
        {"module": "checkout"},
        {"module": "self_healing"}
    ]
    sample_ids = ["log_01", "log_02", "log_03"]

    # Store information using plain English method names
    kb.store_information(text_contents=sample_texts, record_details=sample_metadata, record_ids=sample_ids)

    # Search the knowledge base
    query = "How do self-healing agents handle UI failures?"
    print(f"\nSearching Knowledge Base for: '{query}'")
    
    # Use plain English search method
    results = kb.find_relevant_information(query, max_results=1)

    print("\n--- Top Match Found ---")
    if results and results['documents'][0]:
        print("Text:", results['documents'][0][0])
        print("Metadata:", results['metadatas'][0][0])
    else:
        print("No matching results found.")

if __name__ == "__main__":
    verify_knowledge_base()