"""
fetch_telegram.py
-----------------
This script fetches messages from public Telegram channels
within a 5-year time window and saves them into CSV files.

Dependencies:
- telethon
- pandas
- asyncio
"""

import asyncio
from telethon import TelegramClient
import pandas as pd
import datetime
from tqdm import tqdm

# ==========================================
# CONFIGURATION
# ==========================================
API_ID = 39059309  # replace with your actual api_id
API_HASH = "fc852e1814d9a97a10d114f22ae7214c"  # replace with your actual api_hash

# 5-year time range
START_DATE = datetime.datetime(2020, 11, 7)
END_DATE = datetime.datetime(2025, 11, 7)

# List of public Telegram channels (usernames, without @)
CHANNELS = [
    "bbcpersian",  # News (international)
    "radiofarda",  # Persian media
    "iranintl",  # News & politics
    "mehrnewsagency",  # Local Iranian news
    "funnyiran",  # Example entertainment channel
]


# ==========================================
# FUNCTION TO FETCH MESSAGES
# ==========================================
async def fetch_channel_messages(client, channel):
    """
    Fetch all messages from a Telegram channel within the given date range.
    """
    print(f"Fetching messages from: {channel}")

    messages = []
    async for msg in client.iter_messages(channel):
        if not msg.date:
            continue

        msg_date = msg.date.replace(tzinfo=None)
        if msg_date < START_DATE:
            break  # stop when reaching older messages
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

    # Save results to CSV
    df = pd.DataFrame(messages)
    output_path = f"../data/{channel}_messages.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} messages to {output_path}")


# ==========================================
# MAIN ASYNC FUNCTION
# ==========================================
async def main():
    async with TelegramClient("session_sentiment", API_ID, API_HASH) as client:
        for channel in tqdm(CHANNELS, desc="Processing channels"):
            try:
                await fetch_channel_messages(client, channel)
            except Exception as e:
                print(f"Error fetching {channel}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
