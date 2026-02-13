import pandas as pd
import re
from typing import Dict, Any


class UFCQuestionAnswering:
    def __init__(self, fighters_df, events_df):
        self.fighters_df = fighters_df
        self.events_df = events_df
        self.valid_questions = [
            "Who has the most wins?",
            "Who has the highest win rate?",
            "What is [fighter name]'s record?",
            "How many fights has [fighter name] had?",
            "Who won the fight between [fighter1] and [fighter2]?",
            "What is the average height of fighters?",
            "Who has the longest reach?",
            "How many events have been held?",
            "What are the most common weight classes?",
            "Who has the most knockouts?",
            "List top 10 fighters by wins",
            "Show me fighters from [weight class]",
            "What is [fighter name]'s stance?",
            "Compare [fighter1] vs [fighter2]",
        ]
        
    def is_valid_question(self, question: str) -> bool:
        """Check if question is related to UFC data"""
        keywords = [
            'fighter', 'fight', 'win', 'loss', 'record', 'ufc', 'event',
            'knockout', 'submission', 'weight', 'height', 'reach', 'stance',
            'champion', 'match', 'bout', 'round', 'ko', 'tko'
        ]
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in keywords)
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer UFC-related questions"""
        if not self.is_valid_question(question):
            return {
                'type': 'error',
                'message': '❌ Out of context question! Please ask questions related to UFC fighters, fights, or events.',
                'suggestions': self.valid_questions[:5]
            }
        
        question_lower = question.lower()
        
        # Most wins
        if 'most wins' in question_lower or 'highest wins' in question_lower:
            top_fighter = self.fighters_df.nlargest(1, 'Wins').iloc[0]
            return {
                'type': 'answer',
                'message': f"🏆 {top_fighter['First Name']} {top_fighter['Last Name']} has the most wins with {top_fighter['Wins']} victories!",
                'data': self.fighters_df.nlargest(10, 'Wins')[['First Name', 'Last Name', 'Wins', 'Losses', 'Draws']]
            }
        
        # Highest win rate
        if 'win rate' in question_lower or 'best record' in question_lower:
            df = self.fighters_df.copy()
            df['total'] = pd.to_numeric(df['Wins'], errors='coerce') + pd.to_numeric(df['Losses'], errors='coerce')
            df = df[df['total'] >= 5]  # At least 5 fights
            df['win_rate'] = pd.to_numeric(df['Wins'], errors='coerce') / df['total']
            top = df.nlargest(10, 'win_rate')
            return {
                'type': 'answer',
                'message': f"📊 Top fighters by win rate (minimum 5 fights):",
                'data': top[['First Name', 'Last Name', 'Wins', 'Losses', 'win_rate']]
            }
        
        # Specific fighter record
        if 'record' in question_lower or 'stats' in question_lower:
            fighter_name = self._extract_fighter_name(question)
            if fighter_name:
                fighter = self._find_fighter(fighter_name)
                if fighter is not None:
                    return {
                        'type': 'answer',
                        'message': f"📋 {fighter['First Name']} {fighter['Last Name']}'s Record:",
                        'data': {
                            'Name': f"{fighter['First Name']} {fighter['Last Name']}",
                            'Nickname': fighter['Nickname'],
                            'Record': f"{fighter['Wins']}-{fighter['Losses']}-{fighter['Draws']}",
                            'Height': fighter['Height'],
                            'Weight': fighter['Weight'],
                            'Reach': fighter['Reach'],
                            'Stance': fighter['Stance']
                        }
                    }
        
        # Compare fighters
        if 'compare' in question_lower or 'vs' in question_lower or 'versus' in question_lower:
            fighters = self._extract_two_fighters(question)
            if len(fighters) == 2:
                f1 = self._find_fighter(fighters[0])
                f2 = self._find_fighter(fighters[1])
                if f1 is not None and f2 is not None:
                    comparison = pd.DataFrame({
                        'Attribute': ['Name', 'Record', 'Height', 'Weight', 'Reach', 'Stance'],
                        'Fighter 1': [
                            f"{f1['First Name']} {f1['Last Name']}",
                            f"{f1['Wins']}-{f1['Losses']}-{f1['Draws']}",
                            f1['Height'], f1['Weight'], f1['Reach'], f1['Stance']
                        ],
                        'Fighter 2': [
                            f"{f2['First Name']} {f2['Last Name']}",
                            f"{f2['Wins']}-{f2['Losses']}-{f2['Draws']}",
                            f2['Height'], f2['Weight'], f2['Reach'], f2['Stance']
                        ]
                    })
                    return {
                        'type': 'answer',
                        'message': '⚔️ Fighter Comparison:',
                        'data': comparison
                    }
        
        # Longest reach
        if 'longest reach' in question_lower or 'biggest reach' in question_lower:
            df = self.fighters_df.copy()
            df['reach_num'] = pd.to_numeric(df['Reach'].str.replace('"', '').str.replace('--', '0'), errors='coerce')
            top = df.nlargest(10, 'reach_num')
            return {
                'type': 'answer',
                'message': '📏 Fighters with longest reach:',
                'data': top[['First Name', 'Last Name', 'Reach', 'Height']]
            }
        
        # Total events
        if 'how many events' in question_lower or 'total events' in question_lower:
            total = self.events_df['Event Name'].nunique()
            return {
                'type': 'answer',
                'message': f"🎯 Total UFC events recorded: {total}",
                'data': None
            }
        
        # Weight classes
        if 'weight class' in question_lower:
            weight_counts = self.events_df['Weight Class'].value_counts().head(10)
            return {
                'type': 'answer',
                'message': '⚖️ Most common weight classes:',
                'data': weight_counts
            }
        
        # Top fighters
        if 'top' in question_lower and 'fighter' in question_lower:
            return {
                'type': 'answer',
                'message': '🥇 Top 10 Fighters by Total Wins:',
                'data': self.fighters_df.nlargest(10, 'Wins')[['First Name', 'Last Name', 'Wins', 'Losses', 'Draws']]
            }
        
        # Default: suggest valid questions
        return {
            'type': 'info',
            'message': '💡 I can answer questions about UFC fighters and events. Try asking:',
            'suggestions': self.valid_questions[:8]
        }
    
    def _extract_fighter_name(self, question: str) -> str:
        """Extract fighter name from question"""
        patterns = [
            r"(?:record|stats|about)\s+(?:of\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?:'s|s')",
        ]
        for pattern in patterns:
            match = re.search(pattern, question)
            if match:
                return match.group(1)
        return ""
    
    def _extract_two_fighters(self, question: str):
        """Extract two fighter names from comparison question"""
        names = re.findall(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", question)
        return names[:2] if len(names) >= 2 else []
    
    def _find_fighter(self, name: str):
        """Find fighter in dataframe"""
        name_lower = name.lower()
        for idx, row in self.fighters_df.iterrows():
            full_name = f"{row['First Name']} {row['Last Name']}".lower()
            if name_lower in full_name or full_name in name_lower:
                return row
        return None
