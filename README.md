# 🇮🇷 Persian Sentiment Analysis on Telegram (5-Year Historical Study)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![NLP](https://img.shields.io/badge/NLP-Llama3-orange?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Backend-Ollama-white?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-green?style=for-the-badge)

## 📋 Project Overview

This project involves a comprehensive **Natural Language Processing (NLP)** analysis of Persian social media sentiment over a 5-year historical period (**1399–1404 SH** / **2020–2025 AD**).

The primary objective is to analyze public mood trends on **Telegram**, utilizing **Large Language Models (LLMs)** locally. By leveraging **Meta's Llama 3 (8B)** via **Ollama**, this project classifies thousands of posts into precise emotional categories, handling the linguistic nuances of the Persian language (Farsi), including slang, sarcasm, and cultural context.

### 🎯 Key Objectives
*   **Historical Data Mining:** Extracting 5 years of messages, reactions, and metadata from 5 major public channels using `Telethon`.
*   **Persian NLP Pipeline:** Modular preprocessing using `Hazm` and Regex for text normalization.
*   **LLM-Based Classification:** Using a **custom-engineered Persian System Prompt** to detect complex sentiments (e.g., distinguishing "Dark Humor" from "Sadness").
*   **Visual Analytics:** Generating time-series trends and "Hope vs. Despair" statistical ratios.

---

## 📂 Repository Structure

The project follows a **modular architecture** to ensure maintainability and scalability.

```text
t-sentiment-analysis-fa/
│
├── data/                      # Data Storage
│   ├── processed/             # Cleaned data, Checkpoints, and Final Results
│   ├── kafiha_messages.csv    # Raw Data (Channel 1)
│   ├── bbcpersian_messages.csv# Raw Data (Channel 2)
│   └── ...                    # Other channel datasets
│
├── scripts/                   # Source Code Modules
│   ├── __init__.py
│   └── preprocessor.py        # Core Logic: Text Cleaning & Normalization Class
│
├── notebooks/                 # Jupyter Notebooks for Execution
│   ├── sentiment_analysis.ipynb       # 🧪 Test Notebook (Rapid prototyping on 10 samples)
│   └── full_analysis_pipeline.ipynb   # 🚀 Production Notebook (Full dataset + Checkpointing)
│
├── results/                   # Output Visualizations & Reports
│   ├── trend_plot.png         # 5-Year Sentiment Trend Line
│   └── mood_bar.png           # Channel comparison bar charts
│
├── requirements.txt           # Python Dependencies
└── README.md                  # Project Documentation

## 🛠️ Methodology & Tech Stack

### 1. Data Collection (Scraping)
We utilized the **Telethon API** to scrape historical data. The scraper fetches:
*   **Text Content:** The body of the message.
*   **Metadata:** Timestamp (exact date/time), Views, and Forward counts.
*   **Reactions:** Emoji reactions (e.g., 👍, 😢, ❤️) which provide critical context for sentiment verification.

### 2. Preprocessing (The `scripts/preprocessor.py` Module)
Raw social media text is noisy. We implemented a robust cleaning pipeline:
*   **HTML & URL Removal:** Stripping `<tags>` and `http://` links.
*   **Noise Reduction:** Removing numbers (as per assignment requirement) and non-Persian symbols.
*   **Normalization:** Using the **Hazm** library to standardize Persian characters (e.g., converting Arabic 'ي' and 'ك' to Persian 'ی' and 'ک', and handling zero-width spaces).

### 3. Sentiment Classification (The "Brain")
We use **Llama 3** running locally. The core innovation lies in the **Prompt Engineering**:

*   **The Challenge:** Persian social media often uses "Dark Humor" (طنز تلخ) where a funny text actually implies sadness or anger regarding economic situations.
*   **The Solution:** A **Native Persian System Prompt** was designed to instruct the model to interpret these nuances.

**Taxonomy (Labels):**
*   **خوشحال (Happy):** Joy, success, pure humor.
*   **ناراحت (Sad):** Grief, dark humor, complaints about life.
*   **عصبانی (Angry):** Rage, protest, harsh criticism.
*   **مضطرب (Anxious):** Panic, immediate stress.
*   **نگران (Worried):** Fear of the future, uncertainty.
*   **خنثی (Neutral):** News, advertisements, factual statements.

---

## 🚀 Installation & Usage Guide

### Prerequisites
*   **Python 3.9+**
*   **Ollama:** Download and install from [ollama.com](https://ollama.com).
*   **Hardware:** A GPU with at least 4GB VRAM is recommended (e.g., GTX 1650), though it runs on CPU/RAM with slower inference.

### Step 1: Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/t-sentiment-analysis-fa.git
cd t-sentiment-analysis-fa
pip install -r requirements.txt

### Step 2: Setup the Model
Launch the Ollama server and pull the Llama 3 model:

```bash
# Open a terminal and run:
ollama serve

# In a separate terminal:
ollama pull llama3

### Step 3: Run the Analysis

#### 🅰️ Option A: Quick Test (Local Machine)
To verify the pipeline works on a small subset (10 posts):
1.  Launch Jupyter:
    ```bash
    jupyter notebook
    ```
2.  Open `notebooks/sentiment_analysis.ipynb`.
3.  Run all cells. The result will be saved in `data/processed/test_results.csv`.

#### 🅱️ Option B: Full Production Run (Server/University Lab)
To process the entire 5-year dataset:
1.  Open `notebooks/full_analysis_pipeline.ipynb`.
2.  Run the notebook.

> **Note:** This notebook includes a **Checkpoint System**. If the process is interrupted (e.g., power outage), simply restart the cell, and it will automatically resume from the last saved batch.

---

## 📊 Results & Visualization

The pipeline generates two key types of insights in the `results/` directory:

### 1. Time-Series Trend Analysis
A line chart tracking the fluctuation of sentiments (Happy vs. Sad/Angry) over 5 years. This highlights correlations between real-world events (e.g., elections, economic shifts) and online public mood.

### 2. Hope vs. Despair Ratio
A statistical breakdown per channel, grouping sentiments into:
*   **Positive/Hope:** `['خوشحال']`
*   **Negative/Despair:** `['ناراحت', 'عصبانی', 'نگران', 'مضطرب']`
*   **Neutral:** `['خنثی']`

---

## ⚙️ Configuration

You can modify the `notebooks` to change the configuration:

```python
MODEL_NAME = "llama3"   # You can switch to "llama2" or "mistral" if downloaded
BATCH_SIZE = 100        # Adjust batch saving interval
SOURCES = [...]         # Add or remove target channels

## 📜 License
This project is created for the **Advanced NLP Course (Fall 2025)**.