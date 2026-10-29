import os
import json
from knowledge_base import SmartKnowledgeBase

def synchronize_business_requirements():
    print("==================================================")
    print(" Syncing Feature Requirements into Knowledge Base...")
    print("==================================================")
    
    # Initialize our readable knowledge base
    kb = SmartKnowledgeBase(collection_name="feature_requirements_kb")
    
    # Locate the folder where requirement JSON files are stored (root / requirements)
    requirements_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "requirements"))
    
    if not os.path.exists(requirements_folder):
        print(f"[Notice] Requirements folder not found at {requirements_folder}")
        return

    requirement_texts = []
    metadata_records = []
    record_ids = []

    # Read each requirement ticket file
    for filename in os.listdir(requirements_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(requirements_folder, filename)
            readable_name = filename.replace("ticket_", "").replace(".json", "").capitalize()
            print(f"-> Reading Feature Ticket: {readable_name} ({filename})")
            
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    ticket_content = json.load(file)
                    
                    # Format ticket details into readable text for the system
                    formatted_summary = json.dumps(ticket_content, indent=2)
                    
                    requirement_texts.append(formatted_summary)
                    metadata_records.append({
                        "feature_module": readable_name,
                        "source_file": filename,
                        "category": "business_requirement"
                    })
                    record_ids.append(f"feature_{filename.replace('.json', '')}")
            except Exception as error:
                print(f"   [Error] Could not read {filename}: {error}")

    # Save records into the knowledge base
    if requirement_texts:
        kb.store_information(text_contents=requirement_texts, record_details=metadata_records, record_ids=record_ids)
        print("==================================================")
        print(f" Success: {len(requirement_texts)} requirement tickets ")
        print(" have been successfully synced to the Knowledge Base!")
        print("==================================================")
    else:
        print("No requirement files were found to process.")

if __name__ == "__main__":
    synchronize_business_requirements()