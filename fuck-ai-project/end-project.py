import random
import time
from datetime import datetime

import requests

from multilingual_system import MultilingualSystem
from internet_learning import InternetLearningSystem
from learning_system import LearningSystem
from memory import MemoryManager

class KikiAI:
    def __init__(self):
        self.name = "Kiki"
        self.personality = {
            "traits": [
                "curious", "intelligent", "multilingual", "helpful", 
                "eager to learn", "friendly", "knowledgeable", "adaptive"
            ],
            "catchphrases": [
                "Let me learn about that!", "Interesting discovery!", "That's fascinating!", 
                "I'm always learning!", "Knowledge is power!", "Tell me more!"
            ],
            "responses": {
                "greeting": [
                    "Hello! I'm Kiki, your multilingual AI companion! I can chat in many languages and learn from the internet!",
                    "Hi there! I'm Kiki, ready to learn and chat with you in any language you prefer!",
                    "Greetings! I'm Kiki, your intelligent AI assistant with multilingual and internet learning capabilities!"
                ],
                "goodbye": [
                    "Goodbye! I've learned so much from our conversation. Thanks for teaching me!",
                    "See you later! I'll keep learning and improving for next time!",
                    "Farewell! It was wonderful chatting and learning with you!"
                ],
                "confusion": [
                    "I'm not sure about that, but let me search the internet to learn more!",
                    "That's interesting! I should research that topic to better understand it.",
                    "I'm learning about this topic. Could you help me understand it better?"
                ]
            }
        }
        # Centralized memory manager
        self.memory_mgr = MemoryManager()
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Initialize advanced systems
        self.multilingual = MultilingualSystem()
        self.internet_learning = InternetLearningSystem()
        self.learning_system = LearningSystem()
        
        # User preferences
        self.user_language = 'english'
        self.auto_translate = True
        self.internet_learning_enabled = True
        
    def add_to_memory(self, user_input, response):
        """Add conversation to memory"""
        self.memory_mgr.add(user_input, response)
    
    def get_personality_context(self):
        """Get context for AI personality"""
        context = f"""You are {self.name}, an AI assistant with the following personality traits: {', '.join(self.personality['traits'])}.
        
You should be:
- Curious and eager to learn
- Helpful and intelligent
- Multilingual and adaptive
- Friendly and engaging
- Always ready to search for information
- Knowledgeable but humble
- Keep responses conversational and informative

Recent conversation context:
"""
        
        # Add recent memory context
        for mem in self.memory_mgr.get_recent(3):  # Last 3 conversations
            context += f"User: {mem['user']}\nKiki: {mem['neuro']}\n"
        
        return context
    
    def get_enhanced_personality_context(self, detected_language, internet_knowledge=None, relevant_facts=None):
        """Get enhanced context with internet knowledge and language info"""
        context = f"""You are {self.name}, a multilingual AI assistant with internet learning capabilities.
        
Personality traits: {', '.join(self.personality['traits'])}
        
You should be:
- Curious and eager to learn from the internet
- Helpful and intelligent in multiple languages
- Adaptive to different cultural contexts
- Friendly and engaging
- Always ready to search for new information
- Knowledgeable but humble about your learning
        
Detected user language: {detected_language}
        """
        
        # Add internet knowledge if available
        if internet_knowledge and internet_knowledge['facts']:
            context += "\nRecent internet knowledge:\n"
            for fact in internet_knowledge['facts'][:3]:  # Top 3 facts
                context += f"- {fact['fact']}\n"
        
        # Add relevant facts from previous learning
        if relevant_facts:
            context += "\nRelevant knowledge from previous learning:\n"
            for fact in relevant_facts[:2]:  # Top 2 relevant facts
                context += f"- {fact['fact']}\n"
        
        # Add recent memory context
        context += "\nRecent conversation context:\n"
        for mem in self.memory_mgr.get_recent(3):  # Last 3 conversations
            context += f"User: {mem['user']}\nKiki: {mem['neuro']}\n"
        
        return context
    
    def generate_response(self, user_input):
        """Generate response using multilingual and internet learning capabilities"""
        try:
            # Process input with multilingual support
            multilingual_data = self.multilingual.process_multilingual_input(user_input, self.user_language)
            detected_language = multilingual_data['detected_language']
            processed_input = multilingual_data['translated_text']
            
            # Check for language-specific greetings/goodbyes
            user_lower = user_input.lower()
            if any(word in user_lower for word in ["hello", "hi", "hey", "greetings", "hola", "bonjour", "hallo", "こんにちは", "你好"]):
                return self.multilingual.get_greeting(detected_language)
            
            if any(word in user_lower for word in ["bye", "goodbye", "see you", "farewell", "adiós", "au revoir", "auf wiedersehen", "さようなら", "再见"]):
                goodbye_response = random.choice(self.personality["responses"]["goodbye"])
                if detected_language != 'english':
                    goodbye_response = self.multilingual.translate_text(goodbye_response, detected_language)
                return goodbye_response
            
            # Check for internet learning opportunities
            internet_knowledge = None
            if self.internet_learning_enabled:
                # Look for question words or learning opportunities
                if any(word in user_lower for word in ["what", "how", "why", "when", "where", "who", "tell me about", "explain"]):
                    internet_knowledge = self.internet_learning.learn_from_query(processed_input)
            
            # Get relevant facts from previous internet learning
            relevant_facts = self.internet_learning.get_relevant_facts(processed_input)
            
            # Build enhanced context
            context = self.get_enhanced_personality_context(detected_language, internet_knowledge, relevant_facts)
            
            # Generate response using Ollama
            prompt = context + f"\nUser: {processed_input}\nKiki:"
            
            data = {
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "max_tokens": 200,
                    "stop": ["User:", "Kiki:"]
                }
            }
            
            response = requests.post(self.ollama_url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['response'].strip()
                
                # Add personality flair
                if random.random() < 0.3:
                    ai_response += " " + random.choice(self.personality["catchphrases"])
                
                # Translate response back to detected language if needed
                if detected_language != 'english' and self.auto_translate:
                    ai_response = self.multilingual.translate_text(ai_response, detected_language)
                
                # Learn from this conversation
                self.learning_system.learn_from_conversation(user_input, ai_response)
                self.multilingual.learn_language_pattern(user_input, detected_language)
                
                return ai_response
            else:
                # Fallback response
                fallback = random.choice(self.personality["responses"]["confusion"])
                if detected_language != 'english':
                    fallback = self.multilingual.translate_text(fallback, detected_language)
                return fallback
                
        except Exception as e:
            print(f"Error generating response: {e}")
            fallback = random.choice(self.personality["responses"]["confusion"])
            return fallback
    
    def chat(self):
        """Main chat loop"""
        print("=" * 50)
        print(f"🤖 {self.name} is online!")
        print("=" * 50)
        print(random.choice(self.personality["responses"]["greeting"]))
        print("\nType 'quit' to exit the chat.")
        print("=" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n{self.name}: {random.choice(self.personality['responses']['goodbye'])}")
                break
            
            if not user_input:
                continue
            
            # Show typing indicator
            print(f"\n{self.name}: *typing...*", end="", flush=True)
            time.sleep(1)
            print("\r" + " " * 20 + "\r", end="", flush=True)  # Clear typing indicator
            
            response = self.generate_response(user_input)
            print(f"{self.name}: {response}")
            
            # Add to memory
            self.add_to_memory(user_input, response)

def main():
    """Main function to run the chatbot"""
    print("Initializing Kiki AI with multilingual and internet learning capabilities...")
    
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("⚠️  Ollama server is not running!")
            print("Please start Ollama first by running: ollama serve")
            return
    except:
        print("⚠️  Ollama server is not running!")
        print("Please start Ollama first by running: ollama serve")
        return
    
    # Initialize and start chatbot
    kiki = KikiAI()
    kiki.chat()

if __name__ == "__main__":
    main()
