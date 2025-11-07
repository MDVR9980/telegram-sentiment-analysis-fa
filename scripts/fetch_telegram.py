"""
fetch_telegram.py
-----------------
Fetches messages from Telegram public channels within a 5-year time window.
Saves each channel’s data into a CSV file.

Usage:
    python fetch_telegram.py

Dependencies:
    pip install telethon pandas tqdm
"""

import os
import asyncio
import datetime
import pandas as pd
from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChannelPrivateError, ChannelInvalidError
from tqdm.asyncio import tqdm

# ==========================================
# CONFIGURATION
# ==========================================
API_ID = 39059309
API_HASH = "fc852e1814d9a97a10d114f22ae7214c"

START_DATE = datetime.datetime(2020, 11, 7)
END_DATE = datetime.datetime(2025, 11, 7)

CHANNELS = ["kafiha", "TweetyChannel", "radiofarda", "iranintlTV", "bbcpersian"]

MAX_MESSAGES = 10000  # prevent getting stuck forever
DATA_DIR = "../data"
os.makedirs(DATA_DIR, exist_ok=True)


# ==========================================
# FETCH FUNCTION
# ==========================================
async def fetch_channel_messages(client, channel):
    print(f"\n📡 Fetching messages from: {channel}")

    messages = []
    count = 0

    try:
        async for msg in client.iter_messages(channel, limit=MAX_MESSAGES):
            if not msg.date:
                continue

            msg_date = msg.date.replace(tzinfo=None)
            if msg_date < START_DATE:
                break
            if msg_date > END_DATE:
                continue

            text = msg.message or ""
            messages.append(
                {
                    "msg_id": msg.id,
                    "date": msg_date,
                    "text": text.replace("\n", " "),
                    "views": getattr(msg, "views", None),
                    "forwards": getattr(msg, "forwards", None),
                    "replies_to": getattr(msg, "reply_to_msg_id", None),
                    "channel": channel,
                }
            )
            count += 1

            if count % 500 == 0:
                print(f"  ...fetched {count} messages")

        # Save to CSV
        df = pd.DataFrame(messages)
        output_path = os.path.join(DATA_DIR, f"{channel}_messages.csv")
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"✅ Saved {len(df)} messages to {output_path}")

    except FloodWaitError as e:
        print(f"⏳ Flood wait: sleeping for {e.seconds} seconds")
        await asyncio.sleep(e.seconds)
    except ChannelPrivateError:
        print(f"⚠️ Channel {channel} is private or restricted.")
    except ChannelInvalidError:
        print(f"⚠️ Channel {channel} does not exist or invalid username.")
    except Exception as e:
        print(f"❌ Error fetching {channel}: {e}")


# ==========================================
# MAIN
# ==========================================
async def main():
    async with TelegramClient("session_sentiment", API_ID, API_HASH) as client:
        for channel in tqdm(CHANNELS, desc="Processing channels"):
            await fetch_channel_messages(client, channel)
            await asyncio.sleep(2)  # polite delay between channels


if __name__ == "__main__":
    asyncio.run(main())
