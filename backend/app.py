from typing import Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.kb_utils import get_personality_prompt, retrieve_personality, get_chroma_db
from src.agent.chat_agent import create_chat_agent,invoke_chat_agent
from langchain.agents import create_agent
from src.agent.image_agent import create_image
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

agent = None

@app.route("/api/personalities", methods=["GET"])
def get_personalities():
    db = get_chroma_db()
    all_docs = db.get()
    personalities = list(set([meta["personality_name"] for meta in all_docs["metadatas"]]))
    return jsonify({"code": 200, "data": personalities})

@app.route("/api/createagent", methods=["POST"])
def create_agent():
    global agent
    data = request.json
    personality_name = data["personality_name"]
    prompt_template = get_personality_prompt(personality_name)
    agent = create_chat_agent(prompt_template)
    return jsonify({"code": 200, "msg": "success"})

@app.route("/api/chat", methods=["POST"])
def chat():
    global agent
    data = request.json
    query = data["query"]
    personality_name = data["personality_name"]
    user_id = data["user_id"]
    res = invoke_chat_agent(
        agent,
        query=query,
        personality_name=personality_name,
        user_id=user_id,
    )
    
    messages = res.get("messages", [])
    if messages:
        last_message = messages[-1]
        if hasattr(last_message, 'content'):
            reply = last_message.content
        else:
            reply = str(last_message)
    else:
        reply = "抱歉，没有收到回复"
    
    return jsonify({"code": 200, "data": reply})

@app.route("/api/image", methods=["POST"])
def image():
    data = request.json
    query = data.get("query", "")
    personality_name = data.get("personality_name", "")
    res = create_image(personality_name, query)
    return jsonify({"code": 200, "data": res})

@app.route("/api/personality-detail", methods=["GET"])
def get_personality_detail():
    personality_name = request.args.get("name")
    personality = retrieve_personality(personality_name)
    if not personality:
        return jsonify({"code": 404, "msg": "人格不存在"})
    return jsonify({"code": 200, "data": personality})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)