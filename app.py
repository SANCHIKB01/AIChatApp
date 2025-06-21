from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from utils.rag_system import rag_system
from utils.database import DatabaseManager
import os

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "my-secret")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "txt"}

# ✅ In-memory list to store uploaded doc info
uploaded_docs = []

# MongoDB + Redis (still used for Q&A history)
db_manager = DatabaseManager()

# Check valid file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return redirect("/ask")

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

@app.route("/ask", methods=["GET", "POST"])
def ask():
    answer = None
    question = None
    filename = rag_system.get_filename()

    # ✅ Check if it's a JSON request (Postman or API call)
    if request.is_json:
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"error": "Question is required"}), 400

        answer = rag_system.ask(question)
        db_manager.save_message(f"Q: {question}", "User")
        db_manager.save_message(f"A: {answer}", "AI")

        return jsonify({
            "question": question,
            "answer": answer
        })

    # ✅ Else: It's a normal HTML form submission (browser)
    if request.method == "POST":
        # Handle file upload
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "" and allowed_file(file.filename):
                filename_only = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename_only)
                file.save(filepath)

                try:
                    rag_system.process_file(filepath)
                    flash("✅ Document processed successfully.", "success")

                    uploaded_docs.append({
                        "filename": filename_only,
                        "path": filepath
                    })

                except Exception as e:
                    flash(f"❌ Error processing file: {str(e)}", "danger")
                    return redirect("/ask")

        question = request.form.get("question")
        if question:
            answer = rag_system.ask(question)
            db_manager.save_message(f"Q: {question}", "User")
            db_manager.save_message(f"A: {answer}", "AI")

        filename = rag_system.get_filename()

    # Build chat history for browser
    messages = db_manager.get_messages(limit=10)
    chat_history = []
    for i in range(0, len(messages), 2):
        if i + 1 < len(messages):
            chat_history.append({
                "question": messages[i]["message"].replace("Q: ", ""),
                "answer": messages[i + 1]["message"].replace("A: ", "")
            })

    return render_template("ask.html",
                           answer=answer,
                           question=question,
                           filename=filename,
                           chat_history=chat_history,
                           uploaded_docs=uploaded_docs)




# ✅ Delete specific uploaded document (by index)
@app.route("/delete-upload/<int:index>", methods=["POST"])
def delete_upload(index):
    try:
        doc = uploaded_docs[index]
        if os.path.exists(doc["path"]):
            os.remove(doc["path"])  # Remove from disk
        uploaded_docs.pop(index)    # Remove from in-memory list
        rag_system.clear()          # Reset RAG system state
        flash("🗑️ Document deleted.", "info")
    except IndexError:
        flash("❌ Invalid document index.", "danger")
    return redirect("/ask")

if __name__ == "__main__":
    app.run(debug=True)
