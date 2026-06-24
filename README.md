# 🎙️ AI Refund Voice Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge\&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_Workflows-green?style=for-the-badge)
![LiveKit](https://img.shields.io/badge/LiveKit-Voice_AI-purple?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-Policy_Reasoning-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

<br>

<a href="#-features">
  <img src="https://img.shields.io/badge/Features-View-success?style=for-the-badge" />
</a>

<a href="#-installation">
  <img src="https://img.shields.io/badge/Installation-Guide-blue?style=for-the-badge" />
</a>

<a href="#-architecture">
  <img src="https://img.shields.io/badge/Architecture-Overview-purple?style=for-the-badge" />
</a>

<a href="#-future-improvements">
  <img src="https://img.shields.io/badge/Roadmap-Future_Work-orange?style=for-the-badge" />
</a>

</div>

---
<img width="1886" height="908" alt="image" src="https://github.com/user-attachments/assets/d2f768f5-38f8-4927-8584-8a19dc966c8d" />

## 📖 Overview

AI Refund Voice Agent is an intelligent customer support system capable of handling refund and return requests through natural voice conversations.

The system combines:

* Voice AI
* Agentic workflows
* Tool calling
* Retrieval-Augmented Generation (RAG)
* CRM integration

to automate refund eligibility decisions while strictly following company policies.

Instead of hardcoded logic, the agent retrieves customer order information, consults policy documents, reasons about the request, and generates customer-friendly responses.

---

## ✨ Features

### 🎤 Voice-First Experience

* Real-time Speech-to-Text using Deepgram
* Natural Text-to-Speech responses
* Conversational customer support experience

### 🤖 Agentic Workflow

* Built using LangGraph
* Multi-step reasoning
* Tool calling support
* Stateful conversations

### 📦 CRM Integration

* Order lookup using SQLite CRM database
* Customer order verification
* Product information retrieval

### 📚 Policy-Aware Decisions

* Retrieval-Augmented Generation (RAG)
* Chroma Vector Database
* Semantic search over refund policies
* Policy-grounded decisions

### 🔒 Reliable Decision Making

The agent never:

* Hallucinates order data
* Makes decisions without CRM validation
* Makes decisions without policy validation

---

## 🏗️ System Architecture

```text
Customer Voice
      │
      ▼
 Deepgram STT
      │
      ▼
 LangGraph Agent
      │
      ├── CRM Lookup Tool
      │
      ├── Policy RAG Tool
      │
      ▼
 Final Response
      │
      ▼
 Deepgram TTS
      │
      ▼
 Customer
```

## 📂 Project Structure

```bash
project/
│
├── agent.py
│
├── workflow/
│   ├── graph.py
│   ├── nodes.py
│   ├── llm.py
│   ├── prompt.py
│   ├── state.py
│
├── tools/
│   ├── crm_lookup.py
│   ├── rag_tool.py
│   └── extract_id.py
│
├── scripts/
│   └── policy_rag.py
│
├── db/
│   └── crm.db
│
├── chroma_db/
│
├── .env
├── requirements.txt
└── README.md
```

## 🛠️ Tech Stack

### AI & Agent Framework

* LangGraph
* LangChain
* Cohere LLM

### Voice Stack

* LiveKit Agents
* Deepgram STT
* Deepgram TTS

### RAG Stack

* ChromaDB
* Embedding Models
* Semantic Retrieval

### Backend

* Python
* SQLite
* AsyncIO

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/ai-refund-voice-agent.git

cd ai-refund-voice-agent
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
COHERE_API_KEY=your_key

GROQ_API_KEY = your_key

DEEPGRAM_API_KEY=your_key

LIVEKIT_URL=your_url

LIVEKIT_API_KEY=your_key

LIVEKIT_API_SECRET=your_secret
```

---

## 🚀 Running the Project

### Start Voice Agent

```bash
python agent.py
```

or

```bash
python agent.py dev
```

depending on your LiveKit setup.

### Join Room

Open your frontend client and connect to the configured LiveKit room.

---

## 🧠 Workflow

### Step 1

User requests a refund.

### Step 2

Agent asks for Order ID.

### Step 3

CRM Lookup Tool retrieves order details.

### Step 4

Policy RAG Tool retrieves relevant refund rules.

### Step 5

Agent evaluates:

* Order information
* Product condition
* Refund policy

### Step 6

Customer receives final decision.

---

## ⚡ Challenges Faced

### 1. Voice Recognition Errors

Users often speak order IDs as:

```text
o r d one double zero two
```

instead of:

```text
ORD1002
```

Solution:

* Implemented normalization layer
* Structured extraction workflow

---

### 2. Tool Output Leakage

The voice agent initially read:

* CRM records
* Policy documents
* Internal reasoning

instead of only the final answer.

Solution:

* Improved prompting
* Added response filtering
* Isolated final customer-facing responses

---

### 3. Multi-Step Tool Calling

The agent needed to:

```text
Extract ID
→ CRM Lookup
→ Policy Retrieval
→ Decision
```

while maintaining conversation state.

Solution:

* LangGraph state machine
* Conditional routing
* Tool execution loop

---

## 📈 Future Improvements

### Planned Enhancements

* Email notifications
* Refund ticket generation
* Human escalation workflow
* Multi-language support
* Sentiment analysis
* CRM API integration
* PostgreSQL persistence
* Analytics dashboard
* Deployment using Docker
* Production monitoring

---

## 🎯 Key Learnings

This project provided hands-on experience with:

* Agentic AI systems
* Voice AI pipelines
* Retrieval-Augmented Generation
* Tool calling architectures
* Stateful workflows
* Production debugging
* Real-time conversational systems

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

<div align="center">

Built with ❤️ using LangGraph, LiveKit, Deepgram, and RAG

</div>
