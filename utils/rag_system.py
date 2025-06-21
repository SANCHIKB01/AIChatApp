import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

load_dotenv()

class RAGSystem:
    def __init__(self):
        self.qa_chain = None
        self.vector_store = None
        self.filename = None
        self.preview = None

        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-8b-8192"
        )
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        print("✅ Groq LLaMA3 + HuggingFace Embeddings loaded.")

    def load_and_prepare_document(self, filepath):
        try:
            if filepath.endswith(".txt"):
                loader = TextLoader(filepath)
            elif filepath.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
            else:
                raise ValueError("Unsupported file format. Only .txt and .pdf allowed.")

            print(f"📝 Processing {filepath}")
            documents = loader.load()

            # Set internal state
            self.filename = os.path.basename(filepath)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                self.preview = f.read(1000)  # Just a short preview

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(documents)

            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=self.vector_store.as_retriever()
            )

            print("✅ Vector store + QA chain ready.")
            return len(chunks)

        except Exception as e:
            print(f"❌ Error in document loading: {e}")
            return 0

    def process_file(self, filepath):
        return self.load_and_prepare_document(filepath)

    def answer_question(self, question):
        if not self.qa_chain:
            return "Please upload a document first."
        try:
            result = self.qa_chain.run(question)
            return result
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def get_filename(self):
        return self.filename

    def get_preview(self):
        return self.preview

    def ask(self, question):
        return self.answer_question(question)

    def clear(self):
        self.qa_chain = None
        self.vector_store = None
        self.filename = None
        self.preview = None
        print("🗑️ RAG system state cleared.")

# ✅ Required for app.py
rag_system = RAGSystem()
