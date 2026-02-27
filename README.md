# [AVK.gg](https://discord.com/oauth2/authorize?client_id=1449812433932914970&permissions=8&scope=bot%20applications.commands)

This repository contains a featureful Discord bot (app.py) with moderation, utility, and fun commands.

Quick start:
1. Create a virtual env: python -m venv venv
2. Activate it: (Windows) venv\Scripts\activate | (macOS/Linux) source venv/bin/activate
3. Install requirements: pip install -r requirements.txt
4. Please include your bot token and user ID, along with the prefix command. Please go to `config.json`
5. Run: python app.py

Features:
- ping, say, avatar, serverinfo, userinfo
- Moderation: clear, kick, ban, unban, addrole, removerole
- Fun: 8ball, coin, roll
- Welcome message (to channel name in WELCOME_CHANNEL)
- Safe token-loading via environment variables / .env

Notes:
- Keep your bot token secret. Never commit `config.json` to git.
- The bot requires intents: Message Content & Members if you want user join/welcome and message-based commands to work. Make sure to enable them in the Discord Developer Portal.
```
free
