import os
import chromadb
from chromadb.utils import embedding_functions

class SmartKnowledgeBase:
    def __init__(self, collection_name: str = "qa_knowledge_base", storage_folder: str = "./local_storage"):
        """
        Initializes our local knowledge storage. 
        This keeps all our requirement documents saved securely on disk.
        """
        os.makedirs(storage_folder, exist_ok=True)
        self.database_client = chromadb.PersistentClient(path=storage_folder)
        
        # Using a reliable built-in model to understand text meaning automatically
        self.text_interpreter = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create or connect to our collection of records
        self.collection = self.database_client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.text_interpreter
        )

    def store_information(self, text_contents: list[str], record_details: list[dict], record_ids: list[str]):
        """
        Saves text documents along with their descriptions and unique IDs into the knowledge base.
        """
        self.collection.add(
            documents=text_contents,
            metadatas=record_details,
            ids=record_ids
        )
        print(f"[Knowledge Base] Successfully saved {len(text_contents)} records into '{self.collection.name}'.")

    def find_relevant_information(self, search_question: str, max_results: int = 3):
        """
        Searches the knowledge base to find the documents most relevant to a given question or scenario.
        """
        results = self.collection.query(
            query_texts=[search_question],
            n_results=max_results
        )
        return results