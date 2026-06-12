# 🤖 AI-Powered Discord Bot

A production-ready Discord bot built with Python and `discord.py`. Features slash commands, a modular cog architecture, and AI-powered conversations via OpenAI GPT.

---

## ✨ Features

- **Slash Commands** — Modern Discord command interface (`/ping`, `/ai`, `/serverinfo`, `/avatar`, `/help`)
- **AI-Powered Chat** — Ask the bot anything using `/ai <question>` with OpenAI GPT
- **Modular Cog Architecture** — Commands auto-load from the `cogs/` folder for easy extensibility
- **Rich Embeds** — All responses use polished Discord embeds with colors and formatting
- **Error Handling** — Graceful recovery from API errors, rate limits, and permission issues
- **24/7 Deployment** — Ready for Render, Kerit Cloud, or any Python hosting

## 🛠️ Tech Stack

| Layer        | Technology          |
|--------------|---------------------|
| Language     | Python 3.12         |
| Discord SDK  | `discord.py` 2.5    |
| AI Engine    | OpenAI API (GPT-3.5)|
| Hosting      | Render / Kerit Cloud|

## 🚀 Live Demo

👉 [Invite the bot to your server](https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=274877975552&scope=bot%20applications.commands)

> Replace `YOUR_CLIENT_ID` with your bot's Application ID from the Discord Developer Portal.

---

## 🔧 Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot

# 2. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env       # Windows
# cp .env.example .env       # macOS / Linux
# Then open .env and add your DISCORD_TOKEN and OPENAI_API_KEY

# 5. Run the bot
python main.py
```

Use `/ping` in any channel the bot can see — it should respond with a latency embed. 🎉

---

## 📁 Project Structure

```
discord-bot/
├── cogs/
│   ├── __init__.py       # Package marker
│   ├── general.py        # Utility commands (ping, serverinfo, avatar, help)
│   └── ai_chat.py        # AI chat integration (/ai)
├── main.py               # Bot entry point with auto-loading cog system
├── requirements.txt      # Pinned dependencies
├── Procfile              # Render worker process definition
├── .python-version       # Python version pin for Render
├── .env.example          # Example environment file (safe to commit)
├── .gitignore            # Prevents committing secrets
├── README.md             # This file
└── LICENSE               # MIT license
```

## ☁️ Deploying to Render

1. Push your code to a **public GitHub repo** (make sure `.env` is in `.gitignore`).
2. Go to [render.com](https://render.com) → **New +** → **Background Worker**.
3. Connect your GitHub repo and configure:

   | Setting           | Value                                |
   |-------------------|--------------------------------------|
   | **Build Command** | `pip install -r requirements.txt`    |
   | **Start Command** | `python main.py`                     |
   | **Plan**          | Free                                 |

4. Add **Environment Variables** on Render:

   | Variable         | Value                       |
   |------------------|-----------------------------|
   | `DISCORD_TOKEN`  | Your Discord bot token      |
   | `OPENAI_API_KEY` | Your OpenAI API key         |

5. Click **Create Background Worker**. Done! 🚀

> **Note:** Use **Background Worker**, not Web Service. Discord bots maintain a WebSocket connection, not an HTTP server.

---

## 🔗 API Integrations

- [Discord API](https://discord.com/developers/docs)
- [OpenAI API](https://platform.openai.com/docs)

## 🧠 What I Learned

- Building modular, scalable bots with the cog pattern
- Working with Discord's slash command system and Interaction API
- Securing API keys with environment variables
- Event-driven architecture with async/await
- CI/CD via GitHub + Render auto-deploys

## 📝 License

MIT — free to use and modify.
