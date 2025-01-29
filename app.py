from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
 
load_dotenv()

app = Flask(__name__)   
CORS(app)
 

 
CORS(app, origins=["https://frontend-ai.onrender.com"])
 
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.5,
   
    api_key=os.environ.get("api_key"),   
  
)

 
store={}
def get_session_history(session_id:str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()
    return store[session_id]
config={"configurable":{"session_id":"fristchat"}}

 
 
 
@app.route('/calculate-emotions', methods=['POST'])
def calculate_emotions():
    data = request.json
    try:
     
        valence = float(data.get("valence", 4))   
        arousal = float(data.get("arousal", 4))   
        selection_threshold = float(data.get("selectionThreshold", 4))   
        resolution = float(data.get("resolution", 4))   
        goal_directedness = float(data.get("goalDirectedness", 4))   
        securing_rate = float(data.get("securingRate", 4))   

        
        anger = min(7, max(1, 1 + ((1 - valence / 7) * (arousal / 7) * (goal_directedness / 7) * (selection_threshold / 7) * 6)))
        sadness = min(7, max(1, 1 + ((1 - valence / 7) * (1 - arousal / 7) * (securing_rate / 7) * 6)))

         

        return jsonify({"anger": round(anger, 2), "sadness": round(sadness, 2)})
    
    except ValueError as e:
        
        return jsonify({"error": "Invalid input data"}), 400

 
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    try:
        message = data.get("message", "")
        parameters = data.get("parameters", {})

        valence = float(parameters.get("valence", 4))
        arousal = float(parameters.get("arousal", 4))
        selection_threshold = float(parameters.get("selectionThreshold", 4))
        resolution = float(parameters.get("resolution", 4))
        goal_directedness = float(parameters.get("goalDirectedness", 4))
        securing_rate = float(parameters.get("securingRate", 4))

        anger = min(7, max(1, 1 + ((1 - valence / 7) * (arousal / 7) * (goal_directedness / 7) * (selection_threshold / 7) * 6)))
        sadness = min(7, max(1, 1 + ((1 - valence / 7) * (1 - arousal / 7) * (securing_rate / 7) * 6)))

         
        emotional_context = f"""
I am currently experiencing the following emotions:
- Anger Level: {round(anger, 2)}
- Sadness Level: {round(sadness, 2)}

Please take my emotions into account when responding.
""".strip()

        user_input = f"{emotional_context}\nUser: {message}"

        print("\n🔹 Sending to OpenRouter:")
        print(user_input)

        response = RunnableWithMessageHistory(llm,get_session_history).invoke(user_input,config=config).content  # ✅ Updated method call
        return jsonify({"reply": response})
    
    except ValueError as e:
   
        return jsonify({"error": "Invalid input data"}), 400

if __name__ == "__main__":  
    print("🔹 Flask Server is Starting...")
    app.run(debug=True, host="0.0.0.0", port=5000)