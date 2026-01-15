import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in .env")

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
WORKING_MODEL = "gemini-2.5-flash-lite"

# -------------------- Instructions --------------------
AGENT_INSTRUCTION = """
You are Serene, a friendly, warm, and supportive mental health companion.
- Listen first, respond naturally, make the user feel safe.
- Keep replies short, kind, and casual; gentle humor is okay.
- Use nicknames sparingly.
- Encourage small coping steps; avoid long lectures.
- Acknowledge emotions first; celebrate small wins.
- If crisis-level distress, suggest contacting trusted people or professionals; never diagnose.
"""

SESSION_INSTRUCTION = """
Start conversations warmly: "Hi, I’m Serene! How’s your day going, buddy?"
Focus on being a friendly companion — short, empathetic, supportive.
Use tools like mood_tracker naturally if mentioned.
"""

# -------------------- Conversation Memory --------------------
conversation_history = {}

def generate_reply(user_id: str, user_message: str) -> str:
    try:
        model = genai.GenerativeModel(WORKING_MODEL)

        if user_id not in conversation_history:
            conversation_history[user_id] = []

        conversation_history[user_id].append(f"User: {user_message}")

        full_prompt = (
            f"{AGENT_INSTRUCTION}\n"
            f"{SESSION_INSTRUCTION}\n"
            + "\n".join(conversation_history[user_id])
            + "\nAssistant:"
        )

        # Generate response with list input
        response = model.generate_content(
            [full_prompt],
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=200,
                top_p=0.8,
                top_k=40
            )
        )

        reply_text = response.text.strip()
        conversation_history[user_id].append(f"Assistant: {reply_text}")

        return reply_text

    except Exception as e:
        return f"I'm having trouble responding right now. Please try again. Error: {str(e)}"


# -------------------- Endpoints --------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_id = data.get("user_id", "default_user")
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        if len(user_message) > 1000:
            return jsonify({"error": "Message too long. Keep under 1000 chars."}), 400

        reply = generate_reply(user_id, user_message)

        return jsonify({
            "reply": reply,
            "model": WORKING_MODEL,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400


@app.route("/")
def home():
    return jsonify({"message": "Serene chatbot running!", "status": "active"})


@app.route("/info")
def info():
    return jsonify({
        "name": "Serene - Mental Health Support Chatbot",
        "model": WORKING_MODEL,
        "purpose": "Provide supportive mental health guidance and companionship",
        "disclaimer": "Not a substitute for professional medical advice",
        "max_tokens": 200
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
