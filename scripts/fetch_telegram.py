"""
Fetches messages AND their comments from Telegram public channels within a specified time window.
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
    print(f"\n📡 Fetching messages and comments from: {channel}")
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
            
            # === NEW: Fetch replies (comments) for each message ===
            reactions_text = ""
            if msg.replies and msg.replies.replies > 0:
                reply_texts = []
                # Iterate through all comments/replies of the current message
                try:
                    async for reply in client.iter_messages(channel, reply_to=msg.id):
                        if reply.message:
                            # We replace newlines here as well for consistency
                            reply_texts.append(reply.message.replace("\n", " "))
                    # Join all comments with a separator
                    reactions_text = " || ".join(reply_texts)
                except Exception as e:
                    print(f"  ...could not fetch replies for msg {msg.id}: {e}")
            # =======================================================

            messages.append(
                {
                    "msg_id": msg.id,
                    "date": msg_date,
                    "text": text.replace("\n", " "),
                    "views": getattr(msg, "views", None),
                    "forwards": getattr(msg, "forwards", None),
                    "replies_to": getattr(msg, "reply_to_msg_id", None),
                    "reactions": reactions_text,  # Added new column for comments
                    "channel": channel,
                }
            )
            count += 1

            if count % 100 == 0:  # Reduced frequency of updates as it's slower now
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
            await asyncio.sleep(10)  # Increased delay to be more polite to Telegram API


if __name__ == "__main__":
    asyncio.run(main())