#importing of operating system utilities, ChromaDB(a vector database for text embeddings locally), LlamaIndex for file reading, and Ollama integration.
import os
import chromadb
from llama_index.readers.file import PDFReader
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader,StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
#define class for managing both direct LLM calls(Rag and context calls) and RAG retreival

class TwoLlamaEngine:
#initializes default file paths for reading documents in data_dir and vectorstorage/db_path
    def __init__(self,data_dir = "./data" , db_path= "./chroma.db"):
        self.data_dir = data_dir
        self.db_path = db_path
#connects LlamaIndex to your local Ollama Llama 3 instance running at localhost:11434, with a 120-second timeout window
        self.llm = Ollama(
            model = "llama3.2",
            base_url = "http://localhost:11434",
            request_timeout=300.0,
            context_window=2048,
            additional_kwargs={"num_ctx": 2048}

        )
#connecting LlamaIndex to local nomic-embed-text model in Ollama to calculate vector representations of text
        self.embed_model = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url="http://localhost:11434",
        request_timeout=300.0
        )
#sets default global LLM and embedding models across all LlamaIndex indexing.
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model

#creates/opens persistent vector database folder on disk
        self.db = chromadb.PersistentClient(path=self.db_path)
#Retrieves or initializes a collection named conference_info
        self.chroma_collection = self.db.get_or_create_collection("conference_info")
#ChromaVectorStore and StorageContext: Wraps Chroma database in storage layer compatable with LlamaIndex
        self.vector_store = ChromaVectorStore(chroma_collection = self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store = self.vector_store)
#declare query_engine and executes index initialization
        self.query_engine = None
        self.init_index()
#if os.path.exists..., checks if document directory contains files
#SimpleDirectoryReader(...).load_data, parses text from files in data/.
#VectorStoreIndex.from_documents(...) Chunks/tokenizes document text, generates vector embeddings, and stores them in ChromaDB
#VectorStoreIndex.from_vector_store(...), if no new files exsist, loads vectors directly from disk
#index.as_query_engine(similarity_top_k=3, builds query interface fetching 3 most relevant document chunks per query
    def init_index(self):
        if self.chroma_collection.count() > 0:
            print(f"[RAG Engine] Loading existing index from ChromaDB ({self.chroma_collection.count()} vectors)...")
            index = VectorStoreIndex.from_vector_store(
                self.vector_store,
                storage_context=self.storage_context
    )
        else:
            print("[RAG Engine] ChromaDB is empty. Reading files with PDFReader...")

            # <--- 2. INSERT YOUR SNIPPET HERE inside the else block --->
            if os.path.exists(self.data_dir) and os.listdir(self.data_dir):
                file_extractor = {".pdf": PDFReader()}
                documents = SimpleDirectoryReader(
                    self.data_dir,
                    file_extractor=file_extractor
                ).load_data()

                index = VectorStoreIndex.from_documents(
                    documents,
                    storage_context=self.storage_context
                )
            else:
                raise FileNotFoundError(f"No documents found in '{self.data_dir}'.")

        self.query_engine = index.as_query_engine(similarity_top_k=2,response_mode="compact")

    def ask_direct(self, question: str) -> str:
        response = self.llm.complete(question)
        return str(response)

    def ask_rag(self, question: str)-> str:
        if not self.query_engine:
            return "No documents found. Please add file relative to the conference to the data directory in this project."
        response = self.query_engine.query(question)
        return str(response)