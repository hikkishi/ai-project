"""Learning system: vocabulary, patterns and simple response caching.

This module is intentionally simple: it records word frequencies and
keeps lightweight dynamic responses for quick replies.
"""

from __future__ import annotations

import difflib
import json
import os
import re
from collections import defaultdict
from datetime import datetime
import pickle
from typing import List, Optional, Dict

class LearningSystem:
    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = data_dir
        self.vocabulary_file = os.path.join(data_dir, "vocabulary.json")
        self.patterns_file = os.path.join(data_dir, "patterns.json")
        self.responses_file = os.path.join(data_dir, "learned_responses.json")
        self.context_file = os.path.join(data_dir, "context_associations.pkl")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize data structures
        self.vocabulary = self.load_vocabulary()
        self.patterns = self.load_patterns()
        self.learned_responses = self.load_responses()
        self.context_associations = self.load_context_associations()
        
        # Learning parameters
        self.min_pattern_frequency = 2
        self.max_vocabulary_size = 10000
        
    def load_vocabulary(self) -> Dict:
        """Load vocabulary from file."""
        if os.path.exists(self.vocabulary_file):
            with open(self.vocabulary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert frequency back to defaultdict
                if 'frequency' in data:
                    frequency_dict = defaultdict(int)
                    frequency_dict.update(data['frequency'])
                    data['frequency'] = frequency_dict
                else:
                    data['frequency'] = defaultdict(int)
                return data
        return {
            "words": {},
            "phrases": {},
            "sentiment": {},
            "frequency": defaultdict(int)
        }
    
    def load_patterns(self) -> Dict:
        """Load conversation patterns from file."""
        if os.path.exists(self.patterns_file):
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "input_patterns": {},
            "response_patterns": {},
            "trigger_words": {}
        }
    
    def load_responses(self) -> Dict:
        """Load learned responses from file."""
        if os.path.exists(self.responses_file):
            with open(self.responses_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "categories": {},
            "dynamic_responses": [],
            "context_responses": {}
        }
    
    def load_context_associations(self):
        """Load context associations from pickle file."""
        if os.path.exists(self.context_file):
            with open(self.context_file, 'rb') as f:
                return pickle.load(f)
        return defaultdict(lambda: defaultdict(int))
    
    def save_all_data(self) -> None:
        """Save all learning data to files."""
        # Convert defaultdict to regular dict for JSON serialization
        vocab_to_save = dict(self.vocabulary)
        vocab_to_save["frequency"] = dict(self.vocabulary["frequency"])
        
        with open(self.vocabulary_file, 'w', encoding='utf-8') as f:
            json.dump(vocab_to_save, f, ensure_ascii=False, indent=2)
        
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, ensure_ascii=False, indent=2)
        
        with open(self.responses_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_responses, f, ensure_ascii=False, indent=2)
        
        with open(self.context_file, 'wb') as f:
            pickle.dump(dict(self.context_associations), f)
    
    def learn_from_conversation(self, user_input: str, ai_response: str, context: Optional[str] = None) -> None:
        """Learn from a conversation exchange."""
        # Learn vocabulary
        self._learn_vocabulary(user_input)
        self._learn_vocabulary(ai_response)
        
        # Learn patterns
        self._learn_patterns(user_input, ai_response)
        
        # Learn context associations
        if context:
            self._learn_context_associations(user_input, ai_response, context)
        
        # Update response database
        self._update_response_database(user_input, ai_response)
        
        # Save periodically
        self.save_all_data()
    
    def _learn_vocabulary(self, text: str) -> None:
        """Learn new words and phrases from text."""
        # Clean and tokenize text
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Learn individual words
        for word in words:
            if len(word) > 2:  # Ignore very short words
                self.vocabulary["frequency"][word] += 1
                
                # Track word in vocabulary
                if word not in self.vocabulary["words"]:
                    self.vocabulary["words"][word] = {
                        "first_seen": datetime.now().isoformat(),
                        "contexts": []
                    }
        
        # Learn phrases (2-4 word combinations)
        for i in range(len(words) - 1):
            for j in range(2, min(5, len(words) - i + 1)):
                phrase = " ".join(words[i:i+j])
                if phrase not in self.vocabulary["phrases"]:
                    self.vocabulary["phrases"][phrase] = {
                        "frequency": 0,
                        "contexts": []
                    }
                self.vocabulary["phrases"][phrase]["frequency"] += 1
    
    def _learn_patterns(self, user_input: str, ai_response: str) -> None:
        """Learn conversation patterns."""
        # Extract key patterns from user input
        user_patterns = self._extract_patterns(user_input)
        response_patterns = self._extract_patterns(ai_response)
        
        # Associate input patterns with response patterns
        for user_pattern in user_patterns:
            if user_pattern not in self.patterns["input_patterns"]:
                self.patterns["input_patterns"][user_pattern] = []
            
            for response_pattern in response_patterns:
                if response_pattern not in self.patterns["input_patterns"][user_pattern]:
                    self.patterns["input_patterns"][user_pattern].append(response_pattern)
    
    def _extract_patterns(self, text: str) -> List[str]:
        """Extract patterns from text."""
        patterns = []
        
        # Question patterns
        if text.strip().endswith('?'):
            patterns.append("question")
        
        # Greeting patterns
        greeting_words = ["hello", "hi", "hey", "greetings", "good morning", "good evening"]
        if any(word in text.lower() for word in greeting_words):
            patterns.append("greeting")
        
        # Goodbye patterns
        goodbye_words = ["bye", "goodbye", "see you", "farewell", "take care"]
        if any(word in text.lower() for word in goodbye_words):
            patterns.append("goodbye")
        
        # Sentiment patterns
        positive_words = ["good", "great", "awesome", "wonderful", "amazing", "love", "like"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "horrible"]
        
        if any(word in text.lower() for word in positive_words):
            patterns.append("positive")
        if any(word in text.lower() for word in negative_words):
            patterns.append("negative")
        
        # Length patterns
        if len(text.split()) > 20:
            patterns.append("long_text")
        elif len(text.split()) < 3:
            patterns.append("short_text")
        
        return patterns
    
    def _learn_context_associations(self, user_input: str, ai_response: str, context: str) -> None:
        """Learn associations between context and responses."""
        # Extract keywords from context
        context_keywords = re.findall(r'\b\w+\b', context.lower())
        response_keywords = re.findall(r'\b\w+\b', ai_response.lower())
        
        # Build associations
        for ctx_word in context_keywords:
            for resp_word in response_keywords:
                self.context_associations[ctx_word][resp_word] += 1
    
    def _update_response_database(self, user_input, ai_response):
        """Update the response database with new responses"""
        # Categorize the response
        category = self._categorize_input(user_input)
        
        if category not in self.learned_responses["categories"]:
            self.learned_responses["categories"][category] = []
        
        # Add response if it's not already there
        if ai_response not in self.learned_responses["categories"][category]:
            self.learned_responses["categories"][category].append(ai_response)
        
        # Add to dynamic responses
        self.learned_responses["dynamic_responses"].append({
            "input": user_input,
            "response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "category": category
        })
        
        # Keep only recent dynamic responses
        if len(self.learned_responses["dynamic_responses"]) > 1000:
            self.learned_responses["dynamic_responses"] = self.learned_responses["dynamic_responses"][-1000:]
    
    def _categorize_input(self, text):
        """Categorize input text"""
        text_lower = text.lower()
        
        # Check for question words
        question_words = ["what", "how", "why", "when", "where", "who", "which"]
        if any(word in text_lower for word in question_words):
            return "question"
        
        # Check for greetings
        greeting_words = ["hello", "hi", "hey", "greetings"]
        if any(word in text_lower for word in greeting_words):
            return "greeting"
        
        # Check for goodbyes
        goodbye_words = ["bye", "goodbye", "see you", "farewell"]
        if any(word in text_lower for word in goodbye_words):
            return "goodbye"
        
        # Check for compliments
        compliment_words = ["good", "great", "awesome", "wonderful", "amazing"]
        if any(word in text_lower for word in compliment_words):
            return "compliment"
        
        # Check for complaints
        complaint_words = ["bad", "terrible", "awful", "horrible"]
        if any(word in text_lower for word in complaint_words):
            return "complaint"
        
        return "general"
    
    def get_learned_response(self, user_input, context=None):
        """Get a learned response based on input and context"""
        # Check for exact or similar responses
        category = self._categorize_input(user_input)
        
        # Prefer category-matched canned responses first
        if category in self.learned_responses["categories"]:
            responses = self.learned_responses["categories"][category]
            if responses:
                import random
                return random.choice(responses)

        # Improved similarity matching using SequenceMatcher + Jaccard
        input_text = user_input.lower()
        input_words = set(re.findall(r'\b\w+\b', input_text))

        best_match = None
        best_score = 0.0

        for resp_data in self.learned_responses.get("dynamic_responses", []):
            resp_input = resp_data.get("input", "").lower()
            resp_text = resp_input
            # String similarity
            seq_ratio = difflib.SequenceMatcher(None, input_text, resp_text).ratio()

            # Jaccard on word sets
            resp_words = set(re.findall(r'\b\w+\b', resp_text))
            union = input_words.union(resp_words)
            jaccard = 0.0
            if union:
                jaccard = len(input_words.intersection(resp_words)) / len(union)

            # Combine signals (weights chosen conservatively)
            score = 0.6 * seq_ratio + 0.4 * jaccard

            if score > best_score and score > 0.45:  # Tunable threshold
                best_score = score
                best_match = resp_data.get("response")

        return best_match
    
    def get_vocabulary_stats(self):
        """Get statistics about learned vocabulary"""
        return {
            "total_words": len(self.vocabulary["words"]),
            "total_phrases": len(self.vocabulary["phrases"]),
            "most_common_words": sorted(
                self.vocabulary["frequency"].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10],
            "total_patterns": len(self.patterns["input_patterns"]),
            "total_responses": len(self.learned_responses["dynamic_responses"])
        }

    def add_word_with_translations(self, word: str, target_languages: Optional[List[str]] = None, multilingual=None):
        """Add a word to vocabulary and optionally fetch translations.

        - `multilingual` can be an instance of `MultilingualSystem` or omitted.
        - `target_languages` list of language keys from `MultilingualSystem`.
        """
        if not word or not word.strip():
            return None

        if target_languages is None:
            target_languages = ["spanish", "french", "german"]

        # Lazy import to avoid circular imports at module load
        if multilingual is None:
            try:
                from multilingual_system import MultilingualSystem
                multilingual = MultilingualSystem()
            except Exception:
                multilingual = None

        translations = {}
        if multilingual:
            for lang in target_languages:
                try:
                    translations[lang] = multilingual.translate_text(word, lang, source_language="english")
                except Exception:
                    translations[lang] = None

        # Ensure vocabulary structures
        if word not in self.vocabulary["words"]:
            self.vocabulary["words"][word] = {
                "first_seen": datetime.now().isoformat(),
                "contexts": [],
                "translations": {}
            }

        # Merge translations and bump frequency
        self.vocabulary["words"][word].setdefault("translations", {}).update({k: v for k, v in translations.items() if v})
        self.vocabulary["frequency"][word] += 1
        self.save_all_data()

        return {
            "word": word,
            "translations": translations
        }

    def enrich_word_from_wikipedia(self, word: str, internet_learning=None):
        """Attach a short definition/summary to a vocabulary word using Wikipedia.

        - `internet_learning` can be an instance of `InternetLearningSystem` or omitted.
        """
        if not word or not word.strip():
            return None

        if internet_learning is None:
            try:
                from internet_learning import InternetLearningSystem
                internet_learning = InternetLearningSystem()
            except Exception:
                internet_learning = None

        definition = None
        if internet_learning:
            try:
                results = internet_learning.search_wikipedia(word)
                if results:
                    # Use the extract/content as definition
                    definition = results[0].get("content") or results[0].get("title")
            except Exception:
                definition = None

        # Ensure the word exists
        if word not in self.vocabulary["words"]:
            self.vocabulary["words"][word] = {
                "first_seen": datetime.now().isoformat(),
                "contexts": [],
                "translations": {}
            }

        if definition:
            self.vocabulary["words"][word]["definition"] = definition
            self.save_all_data()

        return definition
