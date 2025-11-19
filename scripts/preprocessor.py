import re
import pandas as pd
from hazm import Normalizer

class TextPreprocessor:
    """
    Handles text cleaning and normalization for Persian social media posts.
    """

    def __init__(self):
        # Initialize the Hazm Normalizer for Persian text
        self.normalizer = Normalizer()

    def clean_text(self, text):
        """
        Cleans the input text by removing unwanted artifacts and normalizing it.
        
        Args:
            text (str): Raw text from the social media post.
            
        Returns:
            str: Cleaned and normalized text.
        """
        if not isinstance(text, str):
            return ""
        
        # 1. Remove URLs (http, https, www)
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # 2. Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # 3. Remove Emojis and Special Symbols (Keep Persian/English chars and basic punctuation)
        text = re.sub(r'[^\w\s\u0600-\u06FF]+', ' ', text)
        
        # 4. Remove Numbers (as requested in the assignment PDF)
        text = re.sub(r'\d+', '', text)
        
        # 5. Remove extra whitespaces and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 6. Persian Normalization (e.g., converting Arabic Yeh/Kaf to Persian)
        text = self.normalizer.normalize(text)
        
        return text

    def clean_reactions(self, reactions_str):
        """
        Cleans the reaction string.
        """
        if pd.isna(reactions_str) or reactions_str == "":
            return ""
        return str(reactions_str).strip()