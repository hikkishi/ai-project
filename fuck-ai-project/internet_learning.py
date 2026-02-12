import hashlib
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
from urllib.parse import urlparse

import requests

class InternetLearningSystem:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.knowledge_file = os.path.join(data_dir, "internet_knowledge.json")
        self.sources_file = os.path.join(data_dir, "learning_sources.json")
        self.facts_file = os.path.join(data_dir, "learned_facts.json")
        self.search_history_file = os.path.join(data_dir, "search_history.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Learning parameters
        self.max_knowledge_entries = 10000
        self.max_fact_age_days = 30
        self.min_source_reliability = 0.5
        
        # Headers for web requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Trusted sources for learning (must be defined before loading sources)
        self.trusted_sources = {
            'wikipedia.org': 0.9,
            'britannica.com': 0.9,
            'reuters.com': 0.8,
            'bbc.com': 0.8,
            'cnn.com': 0.7,
            'nationalgeographic.com': 0.8,
            'sciencedaily.com': 0.8,
            'nature.com': 0.9,
            'science.org': 0.9,
            'stackoverflow.com': 0.7,
            'github.com': 0.7
        }
        
        # Initialize data structures
        self.knowledge_base = self.load_knowledge_base()
        self.learning_sources = self.load_learning_sources()
        self.learned_facts = self.load_learned_facts()
        self.search_history = self.load_search_history()
    
    def load_knowledge_base(self):
        """Load internet knowledge base"""
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'topics': {},
            'facts': {},
            'concepts': {},
            'recent_updates': []
        }
    
    def load_learning_sources(self):
        """Load learning sources configuration"""
        if os.path.exists(self.sources_file):
            with open(self.sources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'preferred_sources': list(self.trusted_sources.keys()),
            'blocked_sources': [],
            'source_reliability': self.trusted_sources.copy(),
            'last_updated': datetime.now().isoformat()
        }
    
    def load_learned_facts(self):
        """Load learned facts from internet"""
        if os.path.exists(self.facts_file):
            with open(self.facts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_search_history(self):
        """Load search history"""
        if os.path.exists(self.search_history_file):
            with open(self.search_history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_all_data(self):
        """Save all learning data"""
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        
        with open(self.sources_file, 'w', encoding='utf-8') as f:
            json.dump(self.learning_sources, f, ensure_ascii=False, indent=2)
        
        with open(self.facts_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_facts, f, ensure_ascii=False, indent=2)
        
        with open(self.search_history_file, 'w', encoding='utf-8') as f:
            json.dump(self.search_history, f, ensure_ascii=False, indent=2)
    
    def search_internet(self, query, num_results=5):
        """Search the internet using DuckDuckGo Instant Answer API"""
        search_results = []
        
        # Record search
        self.search_history.append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results_found': 0
        })
        
        try:
            # Use DuckDuckGo Instant Answer API
            ddg_url = f"https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'pretty': 1,
                'no_html': 1,
                'skip_disambig': 1
            }
            
            response = requests.get(ddg_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract instant answer
                if data.get('Abstract'):
                    search_results.append({
                        'title': data.get('Heading', 'Unknown'),
                        'content': data.get('Abstract', ''),
                        'source': data.get('AbstractSource', 'DuckDuckGo'),
                        'url': data.get('AbstractURL', ''),
                        'reliability': self.get_source_reliability(data.get('AbstractURL', '')),
                        'type': 'instant_answer'
                    })
                
                # Extract related topics
                if data.get('RelatedTopics'):
                    for topic in data.get('RelatedTopics', [])[:3]:
                        if isinstance(topic, dict) and topic.get('Text'):
                            search_results.append({
                                'title': topic.get('Text', '')[:100],
                                'content': topic.get('Text', ''),
                                'source': 'DuckDuckGo',
                                'url': topic.get('FirstURL', ''),
                                'reliability': 0.6,
                                'type': 'related_topic'
                            })
            
            # Try Wikipedia API as backup
            if len(search_results) == 0:
                search_results.extend(self.search_wikipedia(query))
            
            # Update search history
            if self.search_history:
                self.search_history[-1]['results_found'] = len(search_results)
            
            return search_results
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def search_wikipedia(self, query, max_results=3):
        """Search Wikipedia for information"""
        results = []
        
        try:
            # Wikipedia API search
            search_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
            
            # Clean query for Wikipedia
            clean_query = query.replace(' ', '_')
            
            response = requests.get(f"{search_url}{clean_query}", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                results.append({
                    'title': data.get('title', 'Unknown'),
                    'content': data.get('extract', ''),
                    'source': 'Wikipedia',
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'reliability': 0.9,
                    'type': 'wikipedia'
                })
            
        except Exception as e:
            print(f"Wikipedia search error: {e}")
        
        return results
    
    def get_source_reliability(self, url):
        """Get reliability score for a source"""
        if not url:
            return 0.5
        
        domain = urlparse(url).netloc.lower()
        
        # Remove www. prefix
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Check against trusted sources
        for trusted_domain, reliability in self.trusted_sources.items():
            if trusted_domain in domain:
                return reliability
        
        # Check against custom reliability scores
        for source, reliability in self.learning_sources.get('source_reliability', {}).items():
            if source in domain:
                return reliability
        
        # Default reliability for unknown sources
        return 0.5
    
    def extract_facts_from_text(self, text, topic):
        """Extract facts from text content"""
        facts = []
        
        # Simple fact extraction patterns
        fact_patterns = [
            r'([A-Z][^.!?]*(?:is|are|was|were|will be|has been|have been)[^.!?]*[.!?])',
            r'([A-Z][^.!?]*(?:invented|discovered|created|founded|established)[^.!?]*[.!?])',
            r'([A-Z][^.!?]*(?:born|died|lived)[^.!?]*[.!?])',
            r'([A-Z][^.!?]*(?:\d{4}|\d{1,2}\/\d{1,2}\/\d{4})[^.!?]*[.!?])',
            r'([A-Z][^.!?]*(?:located|situated|found)[^.!?]*[.!?])'
        ]
        
        for pattern in fact_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match.strip()) > 20:  # Filter out very short matches
                    facts.append({
                        'fact': match.strip(),
                        'topic': topic,
                        'confidence': 0.7,
                        'extracted_at': datetime.now().isoformat()
                    })
        
        return facts
    
    def learn_from_search_results(self, query, results):
        """Learn from search results"""
        topic_key = self.generate_topic_key(query)
        
        # Initialize topic if not exists
        if topic_key not in self.knowledge_base['topics']:
            self.knowledge_base['topics'][topic_key] = {
                'query': query,
                'first_learned': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'facts': [],
                'sources': [],
                'reliability_score': 0.0
            }
        
        topic = self.knowledge_base['topics'][topic_key]
        total_reliability = 0
        fact_count = 0
        
        for result in results:
            # Add source
            source_info = {
                'url': result.get('url', ''),
                'title': result.get('title', ''),
                'reliability': result.get('reliability', 0.5),
                'accessed_at': datetime.now().isoformat()
            }
            
            if source_info not in topic['sources']:
                topic['sources'].append(source_info)
            
            # Extract and add facts
            content = result.get('content', '')
            if content:
                facts = self.extract_facts_from_text(content, query)
                
                for fact in facts:
                    fact['source'] = result.get('source', 'Unknown')
                    fact['source_reliability'] = result.get('reliability', 0.5)
                    
                    # Check if fact already exists
                    fact_hash = self.generate_fact_hash(fact['fact'])
                    if fact_hash not in [self.generate_fact_hash(f['fact']) for f in topic['facts']]:
                        topic['facts'].append(fact)
                        fact_count += 1
                        total_reliability += fact['source_reliability']
        
        # Update topic reliability
        if fact_count > 0:
            topic['reliability_score'] = total_reliability / fact_count
            topic['last_updated'] = datetime.now().isoformat()
            
            # Add to recent updates
            self.knowledge_base['recent_updates'].append({
                'topic': query,
                'topic_key': topic_key,
                'facts_added': fact_count,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only recent updates
            if len(self.knowledge_base['recent_updates']) > 100:
                self.knowledge_base['recent_updates'] = self.knowledge_base['recent_updates'][-100:]
    
    def generate_topic_key(self, query):
        """Generate a unique key for a topic"""
        return hashlib.md5(query.lower().encode()).hexdigest()[:16]
    
    def generate_fact_hash(self, fact):
        """Generate a hash for a fact to check duplicates"""
        return hashlib.md5(fact.lower().encode()).hexdigest()[:16]
    
    def get_knowledge_about(self, topic):
        """Get knowledge about a specific topic"""
        topic_key = self.generate_topic_key(topic)
        
        if topic_key in self.knowledge_base['topics']:
            topic_data = self.knowledge_base['topics'][topic_key]
            
            # Filter recent and reliable facts
            recent_facts = []
            for fact in topic_data['facts']:
                fact_date = datetime.fromisoformat(fact['extracted_at'])
                if (datetime.now() - fact_date).days <= self.max_fact_age_days:
                    if fact['source_reliability'] >= self.min_source_reliability:
                        recent_facts.append(fact)
            
            return {
                'topic': topic,
                'facts': recent_facts,
                'sources': topic_data['sources'],
                'reliability': topic_data['reliability_score'],
                'last_updated': topic_data['last_updated']
            }
        
        return None
    
    def learn_from_query(self, query):
        """Learn from a user query by searching the internet"""
        # Check if we already have recent knowledge
        existing_knowledge = self.get_knowledge_about(query)
        
        if existing_knowledge:
            last_updated = datetime.fromisoformat(existing_knowledge['last_updated'])
            if (datetime.now() - last_updated).days < 1:  # Updated within last day
                return existing_knowledge
        
        # Search the internet
        print(f"🔍 Searching the internet for: {query}")
        results = self.search_internet(query)
        
        if results:
            # Learn from results
            self.learn_from_search_results(query, results)
            
            # Save data
            self.save_all_data()
            
            # Return updated knowledge
            return self.get_knowledge_about(query)
        
        return None
    
    def get_relevant_facts(self, text, max_facts=3):
        """Get relevant facts based on input text"""
        words = re.findall(r'\b\w+\b', text.lower())
        relevant_facts = []
        
        for topic_key, topic_data in self.knowledge_base['topics'].items():
            topic_query = topic_data['query'].lower()
            
            # Calculate relevance score
            relevance_score = 0
            for word in words:
                if word in topic_query:
                    relevance_score += 1
            
            if relevance_score > 0:
                # Get best facts from this topic
                topic_facts = topic_data['facts'][:2]  # Top 2 facts per topic
                for fact in topic_facts:
                    fact['relevance_score'] = relevance_score
                    relevant_facts.append(fact)
        
        # Sort by relevance and return top facts
        relevant_facts.sort(key=lambda x: x['relevance_score'], reverse=True)
        return relevant_facts[:max_facts]
    
    def get_learning_stats(self):
        """Get statistics about internet learning"""
        total_facts = sum(len(topic['facts']) for topic in self.knowledge_base['topics'].values())
        total_sources = sum(len(topic['sources']) for topic in self.knowledge_base['topics'].values())
        
        return {
            'total_topics': len(self.knowledge_base['topics']),
            'total_facts': total_facts,
            'total_sources': total_sources,
            'recent_updates': len(self.knowledge_base['recent_updates']),
            'searches_performed': len(self.search_history),
            'avg_reliability': sum(topic['reliability_score'] for topic in self.knowledge_base['topics'].values()) / max(len(self.knowledge_base['topics']), 1)
        }
    
    def cleanup_old_data(self):
        """Clean up old data to manage storage"""
        cutoff_date = datetime.now() - timedelta(days=self.max_fact_age_days)
        
        for topic_key, topic_data in list(self.knowledge_base['topics'].items()):
            # Remove old facts
            topic_data['facts'] = [
                fact for fact in topic_data['facts']
                if datetime.fromisoformat(fact['extracted_at']) > cutoff_date
            ]
            
            # Remove topics with no facts
            if not topic_data['facts']:
                del self.knowledge_base['topics'][topic_key]
        
        # Keep only recent search history
        self.search_history = [
            search for search in self.search_history
            if datetime.fromisoformat(search['timestamp']) > cutoff_date
        ]
        
        self.save_all_data()
