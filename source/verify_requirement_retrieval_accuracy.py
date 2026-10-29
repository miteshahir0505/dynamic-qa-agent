import os
import json
from knowledge_base import SmartKnowledgeBase

def verify_requirement_retrieval_accuracy():
    """
    PURPOSE:
    To dynamically discover all feature requirement tickets in our project and 
    verify that the system correctly retrieves each one when questioned.
    
    HOW IT WORKS DYNAMICALLY:
    Instead of hardcoding test cases, it scans the 'requirements/' folder, 
    reads every JSON ticket found, and automatically tests retrieval precision 
    for each feature without requiring manual updates in the future.
    """
    print("==================================================")
    print(" Dynamically Verifying Requirement Retrieval Accuracy...")
    print("==================================================")
    
    # Connect to our feature requirements knowledge base
    knowledge_base = SmartKnowledgeBase(collection_name="feature_requirements_kb")
    
    # Locate the requirements folder dynamically (one level up from source/)
    requirements_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "requirements"))
    
    if not os.path.exists(requirements_folder):
        print(f"[Notice] Requirements folder not found at {requirements_folder}")
        return

    test_evaluations = []

    # Automatically build test cases based on whatever JSON files exist right now
    for filename in os.listdir(requirements_folder):
        if filename.endswith(".json"):
            # Extract clean feature name (e.g., ticket_cart.json -> cart)
            feature_name = filename.replace("ticket_", "").replace(".json", "")
            
            test_evaluations.append({
                "source_file": filename,
                "feature_name": feature_name,
                "test_question": f"What are the specifications and user requirements for {feature_name}?"
            })
    
    if not test_evaluations:
        print("No requirement tickets found to evaluate.")
        return

    passed_count = 0
    total_tests = len(test_evaluations)
    
    # Run each dynamically generated test case
    for index, evaluation in enumerate(test_evaluations, 1):
        question = evaluation["test_question"]
        keyword = evaluation["feature_name"]
        
        print(f"\nTest {index} [File: {evaluation['source_file']}]")
        print(f"   Asking System -> '{question}'")
        
        # Query the knowledge base
        search_results = knowledge_base.find_relevant_information(question, max_results=1)
        
        retrieved_content = ""
        matched_source = ""
        if search_results and search_results['documents'][0]:
            retrieved_content = search_results['documents'][0][0]
            matched_source = search_results['metadatas'][0][0].get('source_file', '')
            
        # Verify if the correct requirement file was retrieved
        if keyword.lower() in matched_source.lower() or keyword.lower() in retrieved_content.lower():
            print(f"   [PASS] System correctly retrieved requirement ticket for '{keyword}'.")
            passed_count += 1
        else:
            print(f"   [FAIL] System failed to retrieve the correct ticket for '{keyword}'.")

    print("\n==================================================")
    print(f" Verification Complete: {passed_count}/{total_tests} dynamic tickets verified successfully.")
    print("==================================================")

if __name__ == "__main__":
    verify_requirement_retrieval_accuracy()