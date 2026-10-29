import sys
from knowledge_base import SmartKnowledgeBase

def ask_qa_assistant():
    """
    PURPOSE: 
    This script allows test runners (such as your TypeScript automation files) 
    to ask questions or pass error descriptions and instantly get the correct 
    business rule or past resolution from our QA Knowledge Base.
    
    WHY IT WAS WRITTEN:
    To bridge our test execution files with our saved requirements library 
    without needing complex technical database queries.
    """
    
    # Check if a question or error description was provided by the test runner
    if len(sys.argv) < 2:
        print("Please provide a search question or error description.")
        return

    user_question = sys.argv[1]
    
    # Connect to our feature requirements knowledge base
    knowledge_base = SmartKnowledgeBase(collection_name="feature_requirements_kb")
    
    # Search the knowledge base for the most relevant answer
    matching_records = knowledge_base.find_relevant_information(user_question, max_results=1)
    
    # Output the result so the calling test script can read it
    if matching_records and matching_records['documents'][0]:
        print(matching_records['documents'][0][0])
    else:
        print("No matching information found in the knowledge base.")

if __name__ == "__main__":
    ask_qa_assistant()