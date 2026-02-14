"""
Advanced search utilities for fighter lookup
"""
import pandas as pd
from difflib import SequenceMatcher, get_close_matches
from typing import List, Tuple
import re


class FighterSearch:
    """Advanced fighter search with multiple matching strategies"""
    
    def __init__(self, fighters_df: pd.DataFrame):
        self.fighters_df = fighters_df
        
    def search(self, query: str, max_results: int = 10) -> pd.DataFrame:
        """
        Multi-strategy search for fighters
        
        Strategies (in order):
        1. Exact match (first name, last name, or nickname)
        2. Partial match (contains query)
        3. Fuzzy match (similar names)
        4. Token match (any word matches)
        """
        if not query or not query.strip():
            return pd.DataFrame()
        
        query = query.strip()
        query_lower = query.lower()
        
        # Strategy 1: Exact match
        exact_matches = self._exact_match(query_lower)
        if len(exact_matches) > 0:
            return exact_matches.head(max_results)
        
        # Strategy 2: Partial match (contains)
        partial_matches = self._partial_match(query_lower)
        if len(partial_matches) > 0:
            return partial_matches.head(max_results)
        
        # Strategy 3: Fuzzy match
        fuzzy_matches = self._fuzzy_match(query_lower, threshold=0.6)
        if len(fuzzy_matches) > 0:
            return fuzzy_matches.head(max_results)
        
        # Strategy 4: Token match (any word)
        token_matches = self._token_match(query_lower)
        if len(token_matches) > 0:
            return token_matches.head(max_results)
        
        # Strategy 5: Very loose fuzzy match
        loose_matches = self._fuzzy_match(query_lower, threshold=0.4)
        return loose_matches.head(max_results)
    
    def _exact_match(self, query: str) -> pd.DataFrame:
        """Exact match on first name, last name, or nickname"""
        return self.fighters_df[
            (self.fighters_df['First Name'].str.lower() == query) |
            (self.fighters_df['Last Name'].str.lower() == query) |
            (self.fighters_df['Nickname'].str.lower() == query)
        ]
    
    def _partial_match(self, query: str) -> pd.DataFrame:
        """Partial match - query is contained in any name field"""
        return self.fighters_df[
            self.fighters_df['First Name'].str.lower().str.contains(query, na=False, regex=False) |
            self.fighters_df['Last Name'].str.lower().str.contains(query, na=False, regex=False) |
            self.fighters_df['Nickname'].str.lower().str.contains(query, na=False, regex=False)
        ]
    
    def _fuzzy_match(self, query: str, threshold: float = 0.6) -> pd.DataFrame:
        """Fuzzy match using sequence matching"""
        matches = []
        
        for idx, row in self.fighters_df.iterrows():
            # Check similarity with each name component
            first_name = str(row['First Name']).lower()
            last_name = str(row['Last Name']).lower()
            nickname = str(row['Nickname']).lower()
            full_name = str(row['Full Name']).lower()
            
            # Calculate similarity scores
            scores = [
                SequenceMatcher(None, query, first_name).ratio(),
                SequenceMatcher(None, query, last_name).ratio(),
                SequenceMatcher(None, query, nickname).ratio(),
                SequenceMatcher(None, query, full_name).ratio(),
            ]
            
            max_score = max(scores)
            
            if max_score >= threshold:
                matches.append((idx, max_score))
        
        if matches:
            # Sort by score descending
            matches.sort(key=lambda x: x[1], reverse=True)
            indices = [m[0] for m in matches]
            return self.fighters_df.loc[indices]
        
        return pd.DataFrame()
    
    def _token_match(self, query: str) -> pd.DataFrame:
        """Match individual tokens/words"""
        tokens = query.split()
        if not tokens:
            return pd.DataFrame()
        
        # Find fighters where any token matches
        mask = pd.Series([False] * len(self.fighters_df))
        
        for token in tokens:
            if len(token) >= 3:  # Only match tokens with 3+ characters
                mask |= (
                    self.fighters_df['First Name'].str.lower().str.contains(token, na=False, regex=False) |
                    self.fighters_df['Last Name'].str.lower().str.contains(token, na=False, regex=False) |
                    self.fighters_df['Nickname'].str.lower().str.contains(token, na=False, regex=False)
                )
        
        return self.fighters_df[mask]
    
    def get_suggestions(self, query: str, n: int = 5) -> List[str]:
        """Get name suggestions based on query"""
        if not query or not query.strip():
            return []
        
        query = query.strip().lower()
        
        # Get all unique names
        all_names = set()
        all_names.update(self.fighters_df['First Name'].dropna().str.lower().tolist())
        all_names.update(self.fighters_df['Last Name'].dropna().str.lower().tolist())
        all_names.update(self.fighters_df['Nickname'].dropna().str.lower().tolist())
        all_names.update(self.fighters_df['Full Name'].dropna().str.lower().tolist())
        
        # Get close matches
        suggestions = get_close_matches(query, all_names, n=n, cutoff=0.3)
        
        return suggestions


def highlight_match(text: str, query: str) -> str:
    """Highlight matching parts of text"""
    if not query or not text:
        return text
    
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f"**{m.group()}**", text)
