# 🤖 JARVIS - Personal AI Assistant

> Your intelligent AI assistant for learning, building projects, and staying productive.

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### 💻 Desktop Experience
- **Native App**: Fully functional desktop application using Electron
- **One-Click Launch**: Start everything with a single shortcut
- **Local Privacy**: Runs locally on your machine

### 🧠 Dual AI Engine
- **Local AI (Ollama)**: Runs offline on your hardware (Supports Llama 3, Mistral, etc.)
- **Cloud AI (OpenAI)**: Connects to GPT-4 for advanced reasoning
- **Mock Mode**: Works instantly without valid keys for testing layout

### 💬 Intelligent Conversation
- Natural language chat with context awareness
- Personalized responses based on conversation history
- Smart suggestions tailored to your needs

### 📚 Learning Mode
- Explains technical topics in simple language
- Creates customized study plans
- Generates practice questions and quizzes
- Summarizes notes and articles

### 🛠️ Project Builder Mode
- Converts ideas into actionable project plans
- Generates development roadmaps
- Suggests appropriate tech stacks
- Provides code templates and examples

### 📋 Productivity Mode
- Daily planning assistance
- Goal tracking and advice
- Time management strategies
- Task prioritization help

## 🚀 Quick Start (Desktop)

The easiest way to run JARVIS is using the desktop launcher.

1. **Locate the Launcher**: Find the **`Start_JARVIS.bat`** file in the project folder.
2. **Double Click**: Run the script.
3. **Enjoy**: The backend and desktop app will launch automatically.

_Note: If you have a desktop shortcut named **JARVIS**, you can use that too!_

## 🧪 Quick Start (Manual)

### Prerequisites
- Python 3.9+
- Node.js 18+
- [Ollama](https://ollama.com/) (for local AI)
- OpenAI API Key (optional)

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```
Server runs at `http://localhost:8000`

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run Desktop App (Dev Mode)
npm run electron-dev
```

## ⚙️ Configuration

Auto-configure your AI provider in `backend/.env`.

### Switching AI Providers

**Option A: Local AI (Ollama)** - *Private & Free*
```env
AI_PROVIDER=ollama
OLLAMA_MODEL=llama3  # or mistral
OLLAMA_BASE_URL=http://localhost:11434/v1
```
*Make sure to run `ollama pull llama3` first!*

**Option B: Cloud AI (OpenAI)** - *Powerful*
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

**Option C: Demo Mode**
If no key is found and Ollama is unreachable, JARVIS enters **Demo Mode** with simulated responses.

## 📁 Project Structure

```
peersonal-ai/
├── Start_JARVIS.bat         # One-click launcher
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Universal configuration
│   ├── .env                 # AI Provider settings
│   ├── services/
│   │   ├── ai_service.py    # Hybrid AI Service (Ollama/OpenAI)
│   │   └── memory_service.py# Conversation memory
│   └── prompts/             # Mode-specific instructions
│
└── frontend/
    ├── electron/
    │   └── main.js          # Desktop app entry point
    ├── src/
    │   ├── app/             # Next.js pages
    │   └── components/      # UI Components
    └── package.json
```

## 🛤️ Roadmap

- [x] **Phase 1: MVP** - Text-based chat with modes
- [x] **Phase 1.5: Desktop** - Electron app & Local Integration
- [ ] **Phase 2: Enhanced AI** - Memory, profiles, RAG
- [ ] **Phase 3: Automation** - Voice, system control
- [ ] **Phase 4: Platform** - User accounts, API access

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Desktop** | Electron |
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS |
| **Backend** | Python, FastAPI |
| **AI Engine** | Ollama (Llama 3) / OpenAI GPT-4 |
| **Styling** | Custom design system with glassmorphism |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

---

Made with ❤️ for students and creators
