import os
import json
from knowledge_base import SmartKnowledgeBase

def synchronize_test_logs():
    print("==================================================")
    print(" Syncing Historical Test Logs & Error Traces...")
    print("==================================================")
    
    # Using the same unified knowledge base
    kb = SmartKnowledgeBase(collection_name="feature_requirements_kb")
    
    # Sample historical logs and known error resolutions
    historical_logs = [
        "Error trace: Element not clickable at checkout confirmation button. Resolution: Verified dynamic overlay loading state and updated wait conditions.",
        "Error trace: Registration form submission timeout. Resolution: Ensured email input field blur event triggers validation properly.",
        "Error trace: Cart item count mismatch after adding product. Resolution: Cleared session storage cache prior to test execution."
    ]
    
    metadata_records = [
        {"feature_module": "Checkout", "category": "error_resolution", "severity": "high"},
        {"feature_module": "Registration", "category": "error_resolution", "severity": "medium"},
        {"feature_module": "Cart", "category": "error_resolution", "severity": "medium"}
    ]
    
    record_ids = ["log_history_01", "log_history_02", "log_history_03"]

    kb.store_information(text_contents=historical_logs, record_details=metadata_records, record_ids=record_ids)
    print("==================================================")
    print(" Success: Historical error traces synced successfully!")
    print("==================================================")

if __name__ == "__main__":
    synchronize_test_logs()