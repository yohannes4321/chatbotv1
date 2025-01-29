# Emotion-Based Chatbot API

This is a Flask-based API that integrates with **Google AI Generative Language (Gemini-1.5-pro)** and LangChain to provide an emotion-aware chatbot. It analyzes emotions based on user inputs and generates responses accordingly.

---

## 📌 Features
- **Emotion Analysis**: Calculates anger and sadness levels based on emotional parameters.
- **Conversational AI**: Uses `ChatGoogleGenerativeAI` from LangChain for AI-powered chat.
- **Session-Based Memory**: Stores chat history per session using `InMemoryChatMessageHistory`.
- **CORS Enabled**: Allows frontend communication via CORS.

---

## 🚀 Getting Started
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yohannes4321/chatbotv1.git
cd chatbotv1
```

### 2️⃣ Create a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the root directory and add:
```ini
api_key=your-google-ai-api-key
```

### 5️⃣ Run the Flask Server
```bash
python app.py
```

---
1. Core Flow of the Application
User sends a message (via /send-message endpoint).
The system calculates emotional context based on user-provided values (valence, arousal, etc.).
It constructs a prompt that includes the user's emotions.
The prompt is sent to LangChain, which interacts with the Gemini LLM (or OpenRouter, if modified).
The model generates a response that considers emotional factors.
The response is returned to the user.
2. Emotion Calculation in Detail
Your system calculates emotions using six input parameters:

Valence: How positive or negative the user feels.
Arousal: How excited or calm they are.
Selection Threshold: How picky they are about responses.
Resolution: How quickly they resolve emotions.
Goal Directedness: How focused they are on a task.
Securing Rate: How safe they feel.
Using these inputs, it calculates:

Anger → Higher when valence is low, but arousal, goal-directedness, and selection threshold are high.
Sadness → Higher when valence and arousal are both low but securing rate is low.
Mathematical formulas:

python
Copy
Edit
anger = min(7, max(1, 1 + ((1 - valence / 7) * (arousal / 7) * (goal_directedness / 7) * (selection_threshold / 7) * 6)))
sadness = min(7, max(1, 1 + ((1 - valence / 7) * (1 - arousal / 7) * (securing_rate / 7) * 6)))
Each emotion is scaled from 1 to 7, ensuring values remain within a human-like range.

3. How the Prompt Works
The final prompt sent to the LLM includes the computed emotions like this:

mathematica
Copy
Edit
I am currently experiencing the following emotions:
- Anger Level: 3.5
- Sadness Level: 2.7

Please take my emotions into account when responding.

User: How can I improve my mental health?
The LLM interprets these emotions and adjusts its response accordingly.

Example:

If anger is high, the AI might respond in a calm and soothing manner.
If sadness is high, the AI might offer motivational support instead of logic-heavy answers.
4. LangChain Memory System
Why Use Memory?
By default, chat models treat every request independently. LangChain stores past messages, so the AI can reference earlier conversations.

How It Works in Your Code
A store dictionary maintains chat sessions, indexed by session_id.
If a session is new, it initializes InMemoryChatMessageHistory().
When a user sends a message, it fetches the session's history to provide context.
RunnableWithMessageHistory() ensures the LLM remembers previous messages.
Example:

python
Copy
Edit
def get_session_history(session_id:str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()
    return store[session_id]
5. LLM Processing & Response Generation
How the LLM Generates Responses
It receives the user’s message + emotional state.
It uses the memory system to check past conversation history.
The model adjusts its tone & word choice based on emotions.
It generates a context-aware response and sends it back.
What Happens Internally?
Your LLM (ChatGoogleGenerativeAI) runs in temperature = 0.5 mode:

Lower temperature (e.g., 0.2) → More factual, precise answers.
Higher temperature (e.g., 0.8) → More creative, varied responses.
Your setting (0.5) balances factuality with creativity.
6. Example Conversation with Emotion Adjustment
User Input 1 (Neutral)
User: "Tell me a joke."
Emotion: Valence=4, Arousal=3 (neutral mood)
AI Response:
"Sure! Why don’t scientists trust atoms? Because they make up everything!"

User Input 2 (Angry Mood)
User: "Why do people always disappoint me?"
Emotion: Valence=2, Arousal=6 (high anger)
AI Response:
"I understand how frustrating it can feel when expectations aren’t met. It might help to focus on self-care and setting healthy boundaries."

User Input 3 (Sad Mood)
User: "I feel like giving up on everything."
Emotion: Valence=1, Arousal=1, Securing Rate=1 (deep sadness)
AI Response:
"I’m really sorry you feel this way. You are not alone, and talking to a friend or professional might help. I’m here to listen."

7. Why This Works Well
Memory Preservation → The AI remembers past messages for better context.
Emotional Adaptation → Adjusts responses based on anger, sadness, etc.
Configurable AI Model → You can tweak temperature for more creativity.
Scalable & Extensible → Can be expanded to handle more emotions & behaviors.


## 🔥 API Endpoints

### ➤ Calculate Emotions
**Endpoint:** `/calculate-emotions` (POST)

**Request Body:**
```json
{
  "valence": 4,
  "arousal": 4,
  "selectionThreshold": 4,
  "resolution": 4,
  "goalDirectedness": 4,
  "securingRate": 4
}
```

**Response:**
```json
{
  "anger": 3.5,
  "sadness": 2.1
}
```

---

### ➤ Send Message
**Endpoint:** `/send-message` (POST)

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "parameters": {
    "valence": 5,
    "arousal": 3,
    "selectionThreshold": 4,
    "resolution": 4,
    "goalDirectedness": 4,
    "securingRate": 4
  }
}
```

**Response:**
```json
{
  "reply": "I'm doing very sad  ! How can I assist you today?"
}
{
  "reply": "I'm doing very Angry ! How can I assist you today?"
}
```

---

## 🛠️ Project Structure
```
📂 emotion-chatbot
│── app.py                 # Flask application
│── requirements.txt       # Dependencies
│── .env                   # Environment variables
│── README.md              # Documentation
```

---

## 📌 Technologies Used
- **Flask** (Backend API)
- **LangChain** (AI Chat Integration)
- **Google AI Generative Language** (Gemini Model)
- **Flask-CORS** (CORS Support)
- **dotenv** (Environment Variables Management)

---

 

 

## 📧 Contact
For questions or suggestions, email: **alemuyohannes960@gmail.com**

