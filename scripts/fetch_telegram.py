"""
Fetches messages, comments, AND emoji reactions from Telegram public channels.
Saves each channel’s data into a CSV file.
Handles different types of reactions gracefully.
"""

import os
import asyncio
import datetime
import pandas as pd
from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChannelPrivateError, ChannelInvalidError
from telethon.tl.types import ReactionEmoji  # Import ReactionEmoji for type checking
from tqdm.asyncio import tqdm

# ==========================================
# CONFIGURATION
# ==========================================
API_ID = 39059309
API_HASH = "fc852e1814d9a97a10d114f22ae7214c"

END_DATE = datetime.datetime.now()
START_DATE = END_DATE - datetime.timedelta(days=5*365)

CHANNELS = ["kafiha", "TweetyChannel", "radiofarda", "iranintlTV", "bbcpersian"]

# --- Robust Path Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ==========================================
# FETCH FUNCTION
# ==========================================
async def fetch_channel_messages(client, channel):
    print(f"\n📡 Fetching data from: {channel}")
    print(f"Time window: {START_DATE.date()} to {END_DATE.date()}")

    messages = []
    count = 0

    try:
        async for msg in client.iter_messages(channel):
            if not msg.date:
                continue

            msg_date = msg.date.replace(tzinfo=None)

            if msg_date < START_DATE:
                print(f"  ...reached the end of the time window. Stopping.")
                break

            if msg_date > END_DATE:
                continue

            text = msg.message or ""
            
            comments_text = ""
            if msg.replies and msg.replies.replies > 0:
                reply_texts = []
                try:
                    async for reply in client.iter_messages(channel, reply_to=msg.id):
                        if reply.message:
                            reply_texts.append(reply.message.replace("\n", " "))
                    comments_text = " || ".join(reply_texts)
                except Exception as e:
                    print(f"  ...could not fetch replies for msg {msg.id}: {e}")

            # === MODIFIED: Handle different reaction types ===
            emoji_reactions_str = ""
            if msg.reactions:
                reaction_parts = []
                for r in msg.reactions.results:
                    # Check if the reaction is a standard emoji reaction
                    if isinstance(r.reaction, ReactionEmoji):
                        reaction_parts.append(f"{r.reaction.emoticon}:{r.count}")
                    # You can add more checks here for other types if needed,
                    # but for now, we ignore non-emoji ones like 'ReactionPaid'.
                
                if reaction_parts:
                    emoji_reactions_str = ", ".join(reaction_parts)
            # =================================================

            messages.append(
                {
                    "msg_id": msg.id,
                    "date": msg_date,
                    "text": text.replace("\n", " "),
                    "views": getattr(msg, "views", None),
                    "forwards": getattr(msg, "forwards", None),
                    "comments": comments_text,
                    "emoji_reactions": emoji_reactions_str,
                    "channel": channel,
                }
            )
            count += 1

            if count % 100 == 0:
                print(f"  ...fetched {count} messages (latest date: {msg_date.date()})")

        if messages:
            df = pd.DataFrame(messages)
            output_path = os.path.join(DATA_DIR, f"{channel}_messages.csv")
            df.to_csv(output_path, index=False, encoding="utf-8-sig")
            print(f"✅ Saved {len(df)} messages to {output_path}")
        else:
            print(f"ℹ️ No new messages found for {channel} in the specified time window.")

    except FloodWaitError as e:
        print(f"⏳ Flood wait: sleeping for {e.seconds} seconds")
        await asyncio.sleep(e.seconds)
    except (ChannelPrivateError, ChannelInvalidError):
        print(f"⚠️ Channel '{channel}' is private, restricted, or does not exist.")
    except Exception as e:
        print(f"❌ An unexpected error occurred while fetching '{channel}': {e}")


# ==========================================
# MAIN
# ==========================================
async def main():
    async with TelegramClient("session_sentiment", API_ID, API_HASH) as client:
        for channel in tqdm(CHANNELS, desc="Processing channels"):
            await fetch_channel_messages(client, channel)
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())