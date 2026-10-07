from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import time
import os

# ==========================================
# RENDER ENVIRONMENT VARIABLES SE UTHAYEGA
# ==========================================
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# ==========================================
# SETTINGS
# ==========================================
INACTIVITY_MINUTES = 2
is_away = True
last_activity = time.time()

# ==========================================
# OFFLINE MESSAGE
# ==========================================
AWAY_MESSAGE = """╔══════════════════════╗
   💤  OFFLINE MODE  💤
╚══════════════════════╝

Hey there! 👋

I'm currently **offline** right now —
away from my phone, busy with something. 😅

Your message has been received,
and I'll reply as soon as I'm back online. ✅

━━━━━━━━━━━━━━━━━━━━━━
⏳ *Please wait a little while*
━━━━━━━━━━━━━━━━━━━━━━

— Sent automatically 🤖"""

# ==========================================
# BOT SETUP
# ==========================================
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ==========================================
# AUTO-REPLY
# ==========================================
@client.on(events.NewMessage(incoming=True))
async def auto_reply_handler(event):
    global last_activity
    try:
        if event.is_private and is_away:
            me = await client.get_me()
            if event.sender_id == me.id:
                return
            minutes_inactive = (time.time() - last_activity) / 60
            if minutes_inactive >= INACTIVITY_MINUTES:
                await event.reply(AWAY_MESSAGE)
                print(f"📩 Reply sent")
    except Exception as e:
        print(f"⚠️ Error: {e}")

# ==========================================
# ACTIVITY TRACKER
# ==========================================
@client.on(events.NewMessage(outgoing=True))
async def activity_tracker(event):
    global last_activity
    last_activity = time.time()

# ==========================================
# COMMANDS
# ==========================================
@client.on(events.NewMessage(pattern=r'^/stop$'))
async def stop_handler(event):
    global is_away
    if event.is_private and event.out:
        is_away = False
        await event.reply("✅ Auto-reply OFF")

@client.on(events.NewMessage(pattern=r'^/start$'))
async def start_handler(event):
    global is_away
    if event.is_private and event.out:
        is_away = True
        await event.reply("🤖 Auto-reply ON")

# ==========================================
# MAIN
# ==========================================
async def main():
    await client.start()
    me = await client.get_me()
    print("=" * 55)
    print("✅ BOT RUNNING ON RENDER!")
    print(f"👤 {me.first_name}")
    print("=" * 55)
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())