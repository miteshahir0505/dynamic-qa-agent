import sys
import json
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from knowledge_base import SmartKnowledgeBase

if __name__ == "__main__":
    kb = SmartKnowledgeBase(collection_name="qa_knowledge_base", storage_folder="./local_storage")
    
    workflows = sys.argv[1:] if len(sys.argv) > 1 else ["registration", "cart", "checkout"]
    results_map = {}
    
    for workflow in workflows:
        results = kb.find_relevant_information(search_question=workflow, max_results=1)
        documents = results.get("documents", [[]])
        metadatas = results.get("metadatas", [[]])
        
        doc_text = documents[0][0] if documents and documents[0] else f"Workflow guidelines for {workflow}"
        meta = metadatas[0][0] if metadatas and metadatas[0] else {}
        
        results_map[workflow] = {
            "project": meta.get("project", workflow.capitalize()),
            "description": doc_text,
            "acceptance_criteria": meta.get("acceptance_criteria", ["Ensure compliance with workflow specs."])
        }

    print(json.dumps(results_map))