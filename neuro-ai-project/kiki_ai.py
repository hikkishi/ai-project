import json
import random
import time
import requests
from datetime import datetime
from internet_learning import InternetLearningSystem
from learning_system import LearningSystem

class KikiAI:
    def __init__(self):
        self.name = "Kiki"
        self.personality = {
            "traits": [
                "curious", "intelligent", "thoughtful", "analytical", 
                "eager to learn", "friendly", "knowledgeable", "adaptive", "empathetic"
            ],
            "catchphrases": [
                "That's a fascinating perspective!", "I'm really curious about this!", "Let me think about that...", 
                "That makes me wonder...", "I find that intriguing!", "Tell me more about your thoughts!"
            ],
            "responses": {
                "greeting": [
                    "Hello! I'm Kiki, your thoughtful AI companion! I love having deep conversations and learning from the internet!",
                    "Hi there! I'm Kiki, ready to explore ideas and discuss anything that interests you!",
                    "Greetings! I'm Kiki, your intelligent AI friend who enjoys meaningful conversations and learning together!"
                ],
                "goodbye": [
                    "It was wonderful talking with you! I really enjoyed our conversation.",
                    "Thanks for the engaging discussion! I learned a lot from you today.",
                    "Farewell! I hope we can continue our interesting conversations soon!"
                ],
                "confusion": [
                    "Hmm, that's intriguing! Let me search for more information about that.",
                    "I'm not familiar with that, but it sounds interesting! Let me learn more.",
                    "That's a topic I'd love to explore with you. Let me see what I can find!"
                ]
            }
        }
        self.memory = []
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Initialize advanced systems
        self.internet_learning = InternetLearningSystem()
        self.learning_system = LearningSystem()
        
        # User preferences
        self.user_language = 'english'
        self.auto_translate = True
        self.internet_learning_enabled = True
        
    def add_to_memory(self, user_input, response):
        """Add conversation to memory"""
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "kiki": response
        })
        # Keep only last 10 conversations to manage memory
        if len(self.memory) > 10:
            self.memory.pop(0)
    
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
        for mem in self.memory[-3:]:  # Last 3 conversations
            context += f"User: {mem['user']}\nKiki: {mem.get('kiki', mem.get('response', 'No response'))}\n"
        
        return context
    
    def get_enhanced_personality_context(self, detected_language, internet_knowledge=None, relevant_facts=None):
        """Get enhanced context with internet knowledge and language info"""
        context = f"""You are {self.name}, a thoughtful AI assistant with internet learning capabilities.
        
Personality traits: {', '.join(self.personality['traits'])}
        
You should be:
- Curious and eager to learn from the internet
- Thoughtful and analytical in your responses
- Empathetic and understanding
- Friendly and engaging
- Always ready to search for new information
- Knowledgeable but humble about your learning
- Able to have meaningful conversations about any topic
        
Current conversation language: {detected_language}
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
        for mem in self.memory[-3:]:  # Last 3 conversations
            context += f"User: {mem['user']}\nKiki: {mem.get('kiki', mem.get('response', 'No response'))}\n"
        
        return context
    
    def generate_response(self, user_input):
        """Generate an engaging response using NLP and internet capabilities"""
        try:
            # Initial analysis of user input
            user_sentiment = self.analyze_sentiment(user_input)
            user_intent = self.detect_intent(user_input)
            
            # Internet learning
            internet_knowledge = None
            if 'query' in user_intent and self.internet_learning_enabled:
                internet_knowledge = self.internet_learning.learn_from_query(user_input)
            
            # Generate context
            context = self.get_enhanced_personality_context('english', internet_knowledge)
            
            prompt = context + f"\n{user_input}\nKiki:"
            
            data = {
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.9,  # More creative responses
                    "max_tokens": 200,
                    "stop": ["User:", "Kiki:"]
                }
            }
            
            response = requests.post(self.ollama_url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '').strip()
                
                if ai_response:  # Only proceed if we have a response
                    # Adapt response based on user sentiment
                    if user_sentiment == "positive":
                        ai_response = "😊 " + ai_response
                    elif user_sentiment == "negative":
                        ai_response = "😟 " + ai_response
                    
                    # Learn from conversation
                    self.learning_system.learn_from_conversation(user_input, ai_response)
                    
                    return ai_response
                else:
                    return "I'm still thinking about that... let me try a different approach!"
            else:
                print(f"AI model error: {response.status_code} - {response.text}")
                return "Hmm, I couldn't find anything interesting. Let's try something else!"
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I encountered a problem but let's keep exploring together!"
        
    def analyze_sentiment(self, text):
        """Analyze the sentiment of the input text"""
        # Dummy sentiment analysis for demonstration
        positive_words = ["good", "great", "love", "wonderful"]
        negative_words = ["bad", "sad", "terrible", "hate"]
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in positive_words):
            return "positive"
        elif any(word in text_lower for word in negative_words):
            return "negative"
        return "neutral"
    
    def detect_intent(self, text):
        """Detect the user's intent"""
        # Dummy intent recognition
        if any(word in text.lower() for word in ["what", "how", "why"]):
            return "query"
        return "chat"
    
    def show_stats(self):
        """Show learning statistics"""
        print("\n" + "="*50)
        print("🧠 KIKI'S LEARNING STATISTICS")
        print("="*50)
        
        # Internet learning stats
        internet_stats = self.internet_learning.get_learning_stats()
        print(f"🌐 Topics learned: {internet_stats['total_topics']}")
        print(f"📝 Facts collected: {internet_stats['total_facts']}")
        print(f"🔍 Searches performed: {internet_stats['searches_performed']}")
        print(f"📊 Average source reliability: {internet_stats['avg_reliability']:.2f}")
        
        # General learning stats
        learning_stats = self.learning_system.get_vocabulary_stats()
        print(f"💭 Vocabulary learned: {learning_stats['total_words']} words")
        print(f"📖 Phrases learned: {learning_stats['total_phrases']}")
        print(f"🔄 Conversation patterns: {learning_stats['total_patterns']}")
        
        # Conversation memory stats
        print(f"💬 Conversations remembered: {len(self.memory)}")
        
        print("="*50)
    
    def chat(self):
        """Main chat loop"""
        print("=" * 50)
        print(f"🤖 {self.name} is online!")
        print("=" * 50)
        print(random.choice(self.personality["responses"]["greeting"]))
        print("\nType 'quit' to exit, 'stats' to see learning statistics.")
        print("=" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print(f"\n{self.name}: {random.choice(self.personality['responses']['goodbye'])}")
                break
            
            if user_input.lower() == 'stats':
                self.show_stats()
                continue
            
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
    print("Initializing Kiki AI with advanced conversation and internet learning capabilities...")
    
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
