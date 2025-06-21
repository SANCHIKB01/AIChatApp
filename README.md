# Welcome to the AI Chat Application Documentation
This application is built using Python Flask and provides the following features:

## 1. Real-time Chat System
The chat system allows users to send and receive messages in real-time. Messages are stored in MongoDB database and cached in Redis for faster access.

## 2. Document Upload and Processing
Users can upload PDF and TXT files. The system processes these documents by:
- Extracting text content
- Splitting text into smaller chunks
- Creating vector embeddings
- Storing in a searchable index

## 3. AI-Powered Question Answering
The RAG (Retrieval-Augmented Generation) system can answer questions about uploaded documents by:
- Searching for relevant document sections
- Using AI models to generate accurate answers
- Providing confidence scores

## 4. Database Integration
- MongoDB: Stores chat messages and user data
- Redis: Caches recent messages for fast retrieval
- FAISS: Vector database for document search

## 5. Deployment Features
The application can be deployed to cloud platforms like:
- Railway

## Technical Stack:
- Backend: Python Flask
- Database: MongoDB Atlas
- Cache: Redis Cloud
- AI: LLaMA Groq
- Vector Search: FAISS

For support, contact the development team.