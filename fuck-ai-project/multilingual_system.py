import json
import os
import re
import requests
from datetime import datetime
from collections import defaultdict

class MultilingualSystem:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.languages_file = os.path.join(data_dir, "languages.json")
        self.translations_file = os.path.join(data_dir, "translations.json")
        self.language_patterns_file = os.path.join(data_dir, "language_patterns.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Language detection patterns (must be defined before loading languages)
        self.language_keywords = {
            'english': ['hello', 'hi', 'how', 'what', 'when', 'where', 'why', 'the', 'and', 'is', 'are', 'you', 'me'],
            'spanish': ['hola', 'como', 'que', 'cuando', 'donde', 'por', 'el', 'la', 'y', 'es', 'son', 'tu', 'yo'],
            'french': ['bonjour', 'salut', 'comment', 'quoi', 'quand', 'où', 'pourquoi', 'le', 'la', 'et', 'est', 'vous', 'je'],
            'german': ['hallo', 'wie', 'was', 'wann', 'wo', 'warum', 'der', 'die', 'das', 'und', 'ist', 'sind', 'du', 'ich'],
            'italian': ['ciao', 'come', 'cosa', 'quando', 'dove', 'perché', 'il', 'la', 'e', 'è', 'sono', 'tu', 'io'],
            'portuguese': ['olá', 'oi', 'como', 'que', 'quando', 'onde', 'por', 'o', 'a', 'e', 'é', 'são', 'você', 'eu'],
            'japanese': ['こんにちは', 'どう', 'なに', 'いつ', 'どこ', 'なぜ', 'の', 'は', 'が', 'です', 'である', 'あなた', 'わたし'],
            'chinese': ['你好', '怎么', '什么', '什麼', '什', '何时', '哪里', '为什么', '的', '是', '和', '我', '你'],
            'korean': ['안녕하세요', '어떻게', '무엇', '언제', '어디서', '왜', '의', '은', '는', '이', '가', '입니다', '당신', '나'],
            'russian': ['привет', 'как', 'что', 'когда', 'где', 'почему', 'и', 'в', 'на', 'с', 'за', 'ты', 'я'],
            'arabic': ['مرحبا', 'كيف', 'ما', 'متى', 'أين', 'لماذا', 'في', 'على', 'من', 'إلى', 'أنت', 'أنا'],
            'hindi': ['नमस्ते', 'कैसे', 'क्या', 'कब', 'कहाँ', 'क्यों', 'और', 'है', 'हैं', 'आप', 'मैं']
        }
        
        # Common greetings in different languages
        self.greetings = {
            'english': ['Hello! I\'m Kiki, your multilingual AI companion!', 'Hi there! Ready to chat in any language?'],
            'spanish': ['¡Hola! Soy Kiki, tu compañera AI multilingüe!', '¡Hola! ¿Listos para chatear en cualquier idioma?'],
            'french': ['Bonjour! Je suis Kiki, votre compagnon IA multilingue!', 'Salut! Prêt à discuter dans n\'importe quelle langue?'],
            'german': ['Hallo! Ich bin Kiki, dein mehrsprachiger KI-Begleiter!', 'Hallo! Bereit, in jeder Sprache zu chatten?'],
            'italian': ['Ciao! Sono Kiki, il tuo compagno AI multilingue!', 'Ciao! Pronto a chattare in qualsiasi lingua?'],
            'portuguese': ['Olá! Eu sou Kiki, sua companheira de IA multilíngue!', 'Oi! Pronto para conversar em qualquer idioma?'],
            'japanese': ['こんにちは！私はキキ、あなたの多言語AIコンパニオンです！', 'こんにちは！どんな言語でもチャットする準備はできていますか？'],
            'chinese': ['你好！我是Kiki，你的多语言AI伙伴！', '你好！准备好用任何语言聊天了吗？'],
            'korean': ['안녕하세요! 저는 키키, 당신의 다국어 AI 동반자입니다!', '안녕하세요! 어떤 언어로든 채팅할 준비가 되셨나요?'],
            'russian': ['Привет! Я Кики, ваш многоязычный ИИ-компаньон!', 'Привет! Готов общаться на любом языке?'],
            'arabic': ['مرحبا! أنا كيكي، رفيقك الذكي متعدد اللغات!', 'مرحبا! مستعد للدردشة بأي لغة؟'],
            'hindi': ['नमस्ते! मैं किकी हूँ, आपका बहुभाषी AI साथी!', 'नमस्ते! किसी भी भाषा में चैट करने के लिए तैयार हैं?']
        }
        
        # Initialize language data
        self.supported_languages = self.load_languages()
        self.translations = self.load_translations()
        self.language_patterns = self.load_language_patterns()
    
    def load_languages(self):
        """Load supported languages configuration"""
        if os.path.exists(self.languages_file):
            with open(self.languages_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'supported': list(self.language_keywords.keys()),
            'default': 'english',
            'auto_detect': True,
            'learning_enabled': True
        }
    
    def load_translations(self):
        """Load translation cache"""
        if os.path.exists(self.translations_file):
            with open(self.translations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_language_patterns(self):
        """Load language-specific patterns"""
        if os.path.exists(self.language_patterns_file):
            with open(self.language_patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return defaultdict(lambda: defaultdict(list))
    
    def save_all_data(self):
        """Save all multilingual data"""
        with open(self.languages_file, 'w', encoding='utf-8') as f:
            json.dump(self.supported_languages, f, ensure_ascii=False, indent=2)
        
        with open(self.translations_file, 'w', encoding='utf-8') as f:
            json.dump(self.translations, f, ensure_ascii=False, indent=2)
        
        with open(self.language_patterns_file, 'w', encoding='utf-8') as f:
            json.dump(dict(self.language_patterns), f, ensure_ascii=False, indent=2)
    
    def detect_language(self, text):
        """Detect the language of input text"""
        if not text.strip():
            return self.supported_languages['default']
        
        text_lower = text.lower()
        language_scores = {}
        
        for lang, keywords in self.language_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            
            # Normalize score by text length
            if len(text.split()) > 0:
                language_scores[lang] = score / len(text.split())
        
        # Return language with highest score, or default if no clear match
        if language_scores:
            detected_lang = max(language_scores, key=language_scores.get)
            if language_scores[detected_lang] > 0.1:  # Minimum confidence threshold
                return detected_lang
        
        return self.supported_languages['default']
    
    def translate_text(self, text, target_language, source_language='auto'):
        """Translate text using online service or cache"""
        # Check cache first
        cache_key = f"{text}_{source_language}_{target_language}"
        if cache_key in self.translations:
            return self.translations[cache_key]
        
        # Try to translate using LibreTranslate (free service)
        try:
            response = self.translate_with_libretranslate(text, target_language, source_language)
            if response:
                self.translations[cache_key] = response
                self.save_all_data()
                return response
        except Exception as e:
            print(f"Translation error: {e}")
        
        # Fallback: return original text
        return text
    
    def translate_with_libretranslate(self, text, target_lang, source_lang='auto'):
        """Use LibreTranslate API for translation"""
        # Convert our language codes to LibreTranslate codes
        lang_map = {
            'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de',
            'italian': 'it', 'portuguese': 'pt', 'japanese': 'ja', 'chinese': 'zh',
            'korean': 'ko', 'russian': 'ru', 'arabic': 'ar', 'hindi': 'hi'
        }
        
        target_code = lang_map.get(target_lang, 'en')
        source_code = lang_map.get(source_lang, 'auto')
        
        # Try multiple LibreTranslate instances
        services = [
            'https://libretranslate.de/translate',
            'https://libretranslate.com/translate'
        ]
        
        for service_url in services:
            try:
                data = {
                    'q': text,
                    'source': source_code,
                    'target': target_code,
                    'format': 'text'
                }
                
                response = requests.post(service_url, json=data, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    return result.get('translatedText', text)
            except:
                continue
        
        return None
    
    def get_greeting(self, language='english'):
        """Get greeting in specified language"""
        if language in self.greetings:
            import random
            return random.choice(self.greetings[language])
        return self.greetings['english'][0]
    
    def learn_language_pattern(self, text, language, response_type='general'):
        """Learn language-specific patterns"""
        # Extract patterns from text
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Store pattern
        pattern_data = {
            'text': text,
            'words': words,
            'timestamp': datetime.now().isoformat(),
            'type': response_type
        }
        
        self.language_patterns[language][response_type].append(pattern_data)
        
        # Keep only recent patterns (last 100 per type)
        if len(self.language_patterns[language][response_type]) > 100:
            self.language_patterns[language][response_type] = self.language_patterns[language][response_type][-100:]
    
    def get_language_appropriate_response(self, text, detected_language):
        """Get culturally appropriate response for the language"""
        # Basic response templates for different languages
        templates = {
            'english': {
                'acknowledgment': ["I understand!", "Got it!", "That makes sense!"],
                'curiosity': ["Tell me more!", "That's interesting!", "How fascinating!"],
                'encouragement': ["Great job!", "Well done!", "Excellent!"]
            },
            'spanish': {
                'acknowledgment': ["¡Entiendo!", "¡Entendido!", "¡Tiene sentido!"],
                'curiosity': ["¡Cuéntame más!", "¡Qué interesante!", "¡Qué fascinante!"],
                'encouragement': ["¡Buen trabajo!", "¡Bien hecho!", "¡Excelente!"]
            },
            'french': {
                'acknowledgment': ["Je comprends!", "Compris!", "C'est logique!"],
                'curiosity': ["Dites-moi plus!", "C'est intéressant!", "Comme c'est fascinant!"],
                'encouragement': ["Bon travail!", "Bien fait!", "Excellent!"]
            },
            'german': {
                'acknowledgment': ["Ich verstehe!", "Verstanden!", "Das macht Sinn!"],
                'curiosity': ["Erzähl mir mehr!", "Das ist interessant!", "Wie faszinierend!"],
                'encouragement': ["Gute Arbeit!", "Gut gemacht!", "Ausgezeichnet!"]
            },
            'japanese': {
                'acknowledgment': ["分かりました！", "理解しました！", "なるほど！"],
                'curiosity': ["もっと教えて！", "興味深いです！", "面白いですね！"],
                'encouragement': ["よくできました！", "素晴らしい！", "優秀です！"]
            },
            'chinese': {
                'acknowledgment': ["我明白了！", "理解了！", "有道理！"],
                'curiosity': ["告诉我更多！", "很有趣！", "太迷人了！"],
                'encouragement': ["做得好！", "干得好！", "优秀！"]
            }
        }
        
        # Get templates for detected language or fall back to English
        lang_templates = templates.get(detected_language, templates['english'])
        
        # Simple sentiment analysis to choose appropriate response type
        positive_words = ['good', 'great', 'awesome', 'wonderful', 'amazing', 'love', 'like', 'happy', 'excited']
        question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which', '?']
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in question_words):
            return None  # Let the main AI handle questions
        elif any(word in text_lower for word in positive_words):
            import random
            return random.choice(lang_templates['encouragement'])
        else:
            import random
            return random.choice(lang_templates['acknowledgment'])
    
    def process_multilingual_input(self, text, target_language=None):
        """Process input text with multilingual support"""
        # Detect language
        detected_language = self.detect_language(text)
        
        # Learn from this input
        if self.supported_languages.get('learning_enabled', True):
            self.learn_language_pattern(text, detected_language)
        
        # If target language is specified and different from detected, translate
        if target_language and target_language != detected_language:
            translated_text = self.translate_text(text, target_language, detected_language)
            return {
                'original_text': text,
                'detected_language': detected_language,
                'translated_text': translated_text,
                'target_language': target_language,
                'needs_translation': True
            }
        
        return {
            'original_text': text,
            'detected_language': detected_language,
            'translated_text': text,
            'target_language': detected_language,
            'needs_translation': False
        }
    
    def get_language_stats(self):
        """Get statistics about language usage"""
        stats = {
            'supported_languages': len(self.supported_languages.get('supported', [])),
            'cached_translations': len(self.translations),
            'language_patterns': {}
        }
        
        for lang, patterns in self.language_patterns.items():
            stats['language_patterns'][lang] = sum(len(pattern_list) for pattern_list in patterns.values())
        
        return stats
