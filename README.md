# 🇮🇷 Persian Sentiment Analysis on Telegram (5-Year Historical Study)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![NLP](https://img.shields.io/badge/NLP-Llama3-orange?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Backend-Ollama-white?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-green?style=for-the-badge)

## 📋 Project Overview

This project involves a comprehensive **Natural Language Processing
(NLP)** analysis of Persian social media sentiment over a 5-year
historical period (**1399--1404 SH** / **2020--2025 AD**).

The primary objective is to analyze public mood trends on **Telegram**,
utilizing **Large Language Models (LLMs)** locally. By leveraging
**Meta's Llama 3 (8B)** via **Ollama**, this project classifies
thousands of posts into precise emotional categories, handling the
linguistic nuances of the Persian language (Farsi), including slang,
sarcasm, and cultural context.

### 🎯 Key Objectives

-   Historical Data Mining: Extracting 5 years of messages, reactions,
    and metadata from 5 major public channels using `Telethon`.
-   Persian NLP Pipeline: Modular preprocessing using `Hazm` and Regex
    for text normalization.
-   LLM-Based Classification: Using a custom-engineered Persian System
    Prompt for distinguishing deep cultural emotions.
-   Visual Analytics: Generating time-series trends and "Hope
    vs. Despair" statistical ratios.

## 📂 Repository Structure

    t-sentiment-analysis-fa/
    │
    ├── data/                      
    │   ├── processed/             
    │   ├── kafiha_messages.csv    
    │   ├── bbcpersian_messages.csv
    │   └── ...                    
    │
    ├── scripts/                   
    │   ├── __init__.py
    │   └── preprocessor.py        
    │
    ├── notebooks/                 
    │   ├── sentiment_analysis.ipynb       
    │   └── full_analysis_pipeline.ipynb   
    │
    ├── results/                   
    │   ├── trend_plot.png         
    │   └── mood_bar.png           
    │
    ├── requirements.txt           
    └── README.md                  

## 🛠️ Methodology & Tech Stack

### 1. Data Collection (Scraping)

Using the **Telethon API**, the scraper collects: \* Message text \*
Timestamp, views, forwards \* Reactions (👍 😢 ❤️ etc.)

### 2. Preprocessing (scripts/preprocessor.py)

A robust Persian cleaning pipeline: \* Remove HTML tags, URLs \* Remove
numbers \* Remove non-Persian symbols \* Normalize Persian characters
using **Hazm**

### 3. Sentiment Classification (LLM Brain)

Using **Llama 3 (8B)** locally via Ollama.

Emotion Labels: \* خوشحال\
\* ناراحت\
\* عصبانی\
\* مضطرب\
\* نگران\
\* خنثی

## 🚀 Installation & Usage Guide

### Step 1: Clone & Install

``` bash
git clone https://github.com/YOUR_USERNAME/t-sentiment-analysis-fa.git
cd t-sentiment-analysis-fa
pip install -r requirements.txt
```

### Step 2: Setup the Model

``` bash
ollama serve
ollama pull llama3
```

### Step 3: Run the Analysis

#### Option A: Quick Test

``` bash
jupyter notebook
```

#### Option B: Full Dataset

Run: `notebooks/full_analysis_pipeline.ipynb`

## 📊 Results

Outputs stored in `results/`: \* 5-Year Trend Plot \* Hope vs. Despair
Ratio

## ⚙️ Configuration

``` python
MODEL_NAME = "llama3"
BATCH_SIZE = 100
SOURCES = [...]
```

## 📜 License

Advanced NLP Course (Fall 2025)