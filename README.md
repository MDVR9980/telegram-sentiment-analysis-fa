# 🇮🇷 Persian Sentiment Analysis on Telegram (5-Year Historical Study)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![Model](https://img.shields.io/badge/Model-Google_Gemma_3_(27B)-purple?style=for-the-badge)
![Backend](https://img.shields.io/badge/Backend-Ollama-white?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-green?style=for-the-badge)

## 📋 Project Overview

This project involves a comprehensive **Natural Language Processing (NLP)** analysis of Persian social media sentiment over a 5-year historical period (**1399–1404 SH** / **2020–2025 AD**).

The primary objective is to analyze public mood trends on **Telegram**, utilizing **Large Language Models (LLMs)** locally. By leveraging **Google's Gemma 3 (27B)** via **Ollama**, this project classifies nearly **1 million posts** into precise emotional categories, handling the linguistic nuances of the Persian language (Farsi), including slang, sarcasm, and cultural context.

### 🎯 Key Objectives

-   **Historical Data Mining:** Extracting 5 years of messages, reactions, and metadata from 5 major public channels using `Telethon`.
-   **Persian NLP Pipeline:** Modular preprocessing using `Hazm` and Regex for text normalization.
-   **LLM-Based Classification:** Using a custom-engineered Persian System Prompt with **Gemma 3** for distinguishing deep cultural emotions (e.g., "Bittersweet Humor" or "Sarcasm").
-   **Visual Analytics:** Generating time-series trends and "Hope vs. Despair" statistical ratios.

## 📂 Repository Structure

    telegram-sentiment-analysis-fa/
    │
    ├── data/                      
    │   ├── processed/             
    │   │   ├── master_cleaned_dataset.csv      # Preprocessed text data (~900MB)
    │   │   ├── final_sentiment_results.csv     # LLM inference results (~446MB)
    │   │   └── test_results.csv                # Initial validation batch
    │   │
    │   ├── bbcpersian_messages.csv             # Raw Data
    │   ├── iranintlTV_messages.csv             # Raw Data
    │   ├── kafiha_messages.csv                 # Raw Data
    │   ├── radiofarda_messages.csv             # Raw Data
    │   └── TweetyChannel_messages.csv          # Raw Data
    │
    ├── scripts/                   
    │   ├── fetch_telegram.py                   # Scraper script (Telethon)
    │   ├── preprocessor.py                     # Cleaning pipeline (Hazm)
    │   └── __init__.py
    │
    ├── notebooks/                 
    │   ├── sentiment_analysis.ipynb            # Initial testing & validation
    │   └── full_analysis_pipeline.ipynb        # Main analysis pipeline (Viz & Stats)
    │
    ├── results/                   
    │   ├── final_mood_barchart.png             # Channel comparison chart
    │   ├── final_trend_analysis.png            # 5-Year time series plot
    │   ├── final_mood_statistics.csv           # Aggregated stats
    │   └── table_sentiments_yearly.csv         # Yearly breakdown
    │
    ├── VahhabRajaee_4041419041_p1.pdf          # Final Project Report (PDF)
    ├── pytorch_model.bin                       # Model artifacts/adapters
    ├── requirements.txt                        # Project dependencies
    └── README.md                               # Documentation

## 🛠️ Methodology & Tech Stack

### 1. Data Collection (Scraping)
**Script:** `scripts/fetch_telegram.py`

Using the **Telethon API**, the scraper collects historical data from 5 major channels:
*   Message text content
*   Metadata: Timestamp, View count, Forward count
*   Reactions (e.g., 👍, 😢, ❤️) to gauge immediate audience response.

### 2. Preprocessing
**Script:** `scripts/preprocessor.py`

A robust Persian text cleaning pipeline designed to handle informal language:
*   **Cleaning:** Removal of HTML tags, URLs, mentions (@user), and non-Persian symbols (emojis are preserved for context where applicable).
*   **Normalization:** Using **Hazm** to standardize characters (e.g., converting Arabic Ye/Kaf to Persian) and correct Zero-width non-joiners (نیم‌فاصله).

### 3. Sentiment Classification (LLM Brain)

The core analysis is powered by **Google Gemma 3 (27B)** running locally via **Ollama**.
*   **Quantization:** 4-bit (Q4_K_M) to fit within 24GB VRAM (RTX 4090).
*   **Prompt Engineering:** A specialized system prompt designed to detect nuances like "Sarcasm" (طنز تلخ) and "Hidden Anger" in Persian.

**Emotion Labels:**
*   `Happy` (خوشحال)
*   `Sad` (ناراحت)
*   `Angry` (عصبانی)
*   `Anxious` (مضطرب)
*   `Worried` (نگران)
*   `Neutral` (خنثی)

## 🚀 Installation & Usage Guide

### Step 1: Clone & Install

    git clone https://github.com/mdvr9980/telegram-sentiment-analysis-fa.git
    cd telegram-sentiment-analysis-fa
    pip install -r requirements.txt

### Step 2: Setup the Model

Ensure **Ollama** is installed. Then pull the specific model version used in the report:

    ollama serve
    ollama pull gemma3:27b

### Step 3: Run the Analysis

#### Option A: Scrape New Data
To fetch the latest messages from the configured channels:

    python scripts/fetch_telegram.py

#### Option B: Run Full Analysis Pipeline
Launch the Jupyter Notebook to process data and generate visualizations:

    jupyter notebook notebooks/full_analysis_pipeline.ipynb

## 📊 Results

All analytical outputs are saved in the `results/` directory:

*   **`final_trend_analysis.png`**: A time-series plot showing the fluctuation of emotions (Happiness, Sadness, Anger) over the 5-year period.
*   **`final_mood_barchart.png`**: A comparative analysis of sentiment distribution across different news and entertainment channels.
*   **`table_sentiments_yearly.csv`**: Detailed yearly breakdown of sentiment statistics.

## ⚙️ Configuration

To adapt the project, modify `notebooks/full_analysis_pipeline.ipynb`:

    MODEL_NAME = "gemma3:27b"  # or "llama3" for lighter tests
    BATCH_SIZE = 100           # Adjust based on VRAM
    START_YEAR = 2020
    END_YEAR = 2025

## 📜 License

**Advanced NLP Course (Fall 1404 / 2025)**
**Student:** Mohammad Davoud Vahhab Rajaee
**ID:** 4041419041