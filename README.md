AI Chat App (Flask + Groq + LangChain + FAISS)
An intelligent AI-powered web app that lets users ask questions based on uploaded documents (PDF/TXT) or have open-ended chats. It uses Groq's ultra-fast LLaMA 3 model and LangChain's Retrieval-Augmented Generation (RAG) pipeline with FAISS for document understanding.


🚀 Features
- 🔍 Upload `.pdf` or `.txt` files and ask questions about them
- 🧠 Powered by Groq’s blazing-fast LLaMA 3 model
- 🧰 Uses LangChain and FAISS for document retrieval
- 🧾 Displays chat history and uploaded documents with delete buttons
- 🌐 Fully deployable on platforms like Render


📸 Screenshots
Project View
![image](https://github.com/user-attachments/assets/cc9f92ee-a726-4627-9811-330d3cd9e876)

Uploading File and QnA
![image](https://github.com/user-attachments/assets/1cac202d-7156-4f4c-873f-a01a0c7037c0)

Delete the document
![image](https://github.com/user-attachments/assets/adf5ff38-aa97-4866-b670-0634a91715dc)

MongoDB Chat messages
![image](https://github.com/user-attachments/assets/77555947-0de6-40ee-9f5a-ad1062b14d7f)

Redix Cache messages
![image](https://github.com/user-attachments/assets/ba52f197-0e0b-47af-8cdb-79a3b97d7b8c)


🛠️ Tech Stack
  Layer                 Tools Used                                      
 Frontend           Flask + Jinja2 Templates                        
 Backend            Python (Flask), LangChain, FAISS                
 LLM API            Groq LLaMA 3       
 Embeddings         HuggingFaceEmbeddings via LangChain             
 Storage            In-memory (No persistent DB required)           
                     

📂 Project Structure
ai-chat-app/
├── app.py
├── requirements.txt
├── templates/
│ └── ask.html
│ └── base.html
├── utils/
│ └── database.py
│ └── rag_system.py
├── screenshots/
│ ├── upload.png
│ ├── ask.png
│ └── history.png


🗣️ Set Your API Keys 
> Before running the app, you need to generate two API keys:  
 1. Groq API Key from [console.groq.com](https://console.groq.com) — used to access the LLaMA model.  
 2. Hugging Face API Token from [huggingface.co](https://huggingface.co/settings/tokens) — used to create embeddings for the document text.
>These are added as environment variables named `GROQ_API_KEY` and `HUGGINGFACEHUB_API_TOKEN`.


🎥 Demo Video You can watch a full walkthrough here:  


🔗 GitHUb Repo: https://github.com/SANCHIKB01/ai-chat-app

Local Setup
bash
git clone https://github.com/SANCHIKB01/ai-chat-app.git
cd ai-chat-app
pip install -r requirements.txt
python app.py




