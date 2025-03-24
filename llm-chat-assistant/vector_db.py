
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from typing import List, Dict

class ChromaDBHandler:
    """
    A class to handle operations with ChromaDB for storing and querying vector embeddings.
    """

    def __init__(self, api_key: str, persist_directory: str = "./chromadb", embedding_model: str = "text-embedding-ada-002"):
        """
        Initialize the ChromaDBHandler with a persistent storage directory and embedding model.

        :param api_key: API key for the embedding service.
        :param persist_directory: Directory to persist the ChromaDB collections.
        :param embedding_model: The embedding model to use for generating embeddings.
        """
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings()
        )
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name=embedding_model
        )
        self.collection = None

    def create_or_load_collection(self, collection_name: str):
        """
        Create or load a collection in ChromaDB.

        :param collection_name: Name of the collection to create or load.
        """
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Add documents to the ChromaDB collection.

        :param documents: A list of dictionaries containing 'id', 'content', and optional 'metadata'.
        """
        if not self.collection:
            raise ValueError("Collection is not initialized. Call create_or_load_collection first.")

        ids = [doc['id'] for doc in documents]
        contents = [doc['content'] for doc in documents]
        metadatas = [doc.get('metadata', {}) for doc in documents]

        self.collection.add(
            ids=ids,
            documents=contents,
            metadatas=metadatas
        )

    def query(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """
        Query the ChromaDB collection for similar documents.

        :param query_text: The query text to search for.
        :param n_results: Number of top results to return.
        :return: A list of dictionaries containing 'id', 'content', and 'metadata' of the results.
        """
        if not self.collection:
            raise ValueError("Collection is not initialized. Call create_or_load_collection first.")

        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return [
            {"id": result_id, "content": result_doc, "metadata": result_meta}
            for result_id, result_doc, result_meta in zip(results['ids'][0], results['documents'][0], results['metadatas'][0])
        ]



#%%

# class ChromaDBHandler1:
#     """
#     A class to handle operations with ChromaDB for storing and querying vector embeddings.
#     """

#     def __init__(self, api_key: str, persist_directory: str = "./chromadb", embedding_model: str = "all-MiniLM-L6-v2"):
#         """
#         Initialize the ChromaDBHandler with a persistent storage directory and embedding model.

#         :param api_key: API key for the embedding service.
#         :param persist_directory: Directory to persist the ChromaDB collections.
#         :param embedding_model: The embedding model to use for generating embeddings.
#         """
#         self.client = chromadb.PersistentClient(
#             path=persist_directory,
#             settings=Settings()
#         )
#         self.embedding_model = SentenceTransformer(embedding_model)
#         self.collection = None

#     def sentence_transformer_embedding_function(self, texts: List[str]) -> List[List[float]]:
#         """
#         Custom embedding function using Sentence Transformers.

#         :param texts: A list of strings to embed.
#         :return: A list of embeddings.
#         """
#         return self.embedding_model.encode(texts, convert_to_numpy=True).tolist()


#     def create_or_load_collection(self, collection_name: str):
#         """
#         Create or load a collection in ChromaDB.

#         :param collection_name: Name of the collection to create or load.
#         """
#         self.collection = self.client.get_or_create_collection(
#             name=collection_name,
#             embedding_function=self.sentence_transformer_embedding_function
#         )

#     def add_documents(self, documents: List[Dict[str, str]]):
#         """
#         Add documents to the ChromaDB collection.

#         :param documents: A list of dictionaries containing 'id', 'content', and optional 'metadata'.
#         """
#         if not self.collection:
#             raise ValueError("Collection is not initialized. Call create_or_load_collection first.")

#         ids = [doc['id'] for doc in documents]
#         contents = [doc['content'] for doc in documents]
#         metadatas = [doc.get('metadata', {}) for doc in documents]

#         self.collection.add(
#             ids=ids,
#             documents=contents,
#             metadatas=metadatas
#         )

#     def query(self, query_text: str, n_results: int = 5) -> List[Dict]:
#         """
#         Query the ChromaDB collection for similar documents.

#         :param query_text: The query text to search for.
#         :param n_results: Number of top results to return.
#         :return: A list of dictionaries containing 'id', 'content', and 'metadata' of the results.
#         """
#         if not self.collection:
#             raise ValueError("Collection is not initialized. Call create_or_load_collection first.")

#         results = self.collection.query(
#             query_texts=[query_text],
#             n_results=n_results
#         )
#         return [
#             {"id": result_id, "content": result_doc, "metadata": result_meta}
#             for result_id, result_doc, result_meta in zip(results['ids'], results['documents'], results['metadatas'])
#         ]

#     def persist(self):
#         """
#         Persist the ChromaDB data to disk.
#         """
#         self.client.persist()
