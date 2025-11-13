"""
Fetches messages from Telegram public channels within a specified time window.
Saves each channel’s data into a CSV file.

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

# Set the time window to the last 5 years
END_DATE = datetime.datetime.now()
START_DATE = END_DATE - datetime.timedelta(days=5*365)

CHANNELS = ["kafiha", "TweetyChannel", "radiofarda", "iranintlTV", "bbcpersian"]

DATA_DIR = "../data"
os.makedirs(DATA_DIR, exist_ok=True)


# ==========================================
# FETCH FUNCTION
# ==========================================
async def fetch_channel_messages(client, channel):
    print(f"\n📡 Fetching messages from: {channel}")
    print(f"Time window: {START_DATE.date()} to {END_DATE.date()}")

    messages = []
    count = 0

    try:
        # We remove the 'limit' parameter to fetch all available messages
        # The loop will naturally stop based on the date check below
        async for msg in client.iter_messages(channel):
            # Skip messages without a date attribute
            if not msg.date:
                continue

            # Ensure the date is timezone-unaware for consistent comparison
            msg_date = msg.date.replace(tzinfo=None)

            # If a message is older than our start date, we stop fetching for this channel
            if msg_date < START_DATE:
                print(f"  ...reached the end of the time window. Stopping.")
                break

            # Skip messages that are newer than our end date (if any)
            if msg_date > END_DATE:
                continue

            # Append valid messages to our list
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

            # Progress update every 500 messages
            if count % 500 == 0:
                print(f"  ...fetched {count} messages (latest date: {msg_date.date()})")

        # Save to CSV if any messages were collected
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
            await asyncio.sleep(5)  # A slightly longer polite delay to avoid flood waits


if __name__ == "__main__":
    asyncio.run(main())