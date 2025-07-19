# Kiki AI 

## Features

### Multilingual Support
- **12 Languages Supported**: English, Spanish, French, German, Italian, Portuguese, Japanese, Chinese, Korean, Russian, Arabic, Hindi
- **Auto Language Detection**: Automatically detects the user's language
- **Real-time Translation**: Translates conversations between languages
- **Cultural Adaptation**: Responds appropriately for different cultural contexts

### Internet Learning
- **Real-time Web Search**: Searches the internet for current information
- **Knowledge Extraction**: Automatically extracts facts from web sources
- **Source Reliability**: Evaluates and scores information sources
- **Continuous Learning**: Builds knowledge base from conversations

### Advanced AI Features
- **Personality-driven Responses**: Curious, intelligent, and helpful personality
- **Memory System**: Remembers recent conversations
- **Learning Statistics**: Tracks learning progress and statistics
- **Ollama Integration**: Uses local AI models for privacy

## Quick Start

### Prerequisites
- Python 3.7 or higher
- [Ollama](https://ollama.ai) installed and running
- Internet connection for learning features

### Installation

1. **Clone or Download** the project to your local machine

2. **Run the Setup Script**:
   ```bash
   python setup.py
   ```
   This will:
   - Install required Python packages
   - Download the AI model (llama3.2:1b)
   - Set up the project environment

3. **Start Kiki AI**:
   ```bash
   python kiki_ai.py
   ```

### Manual Setup (Alternative)

1. **Install Dependencies**:
   ```bash
   pip install requests colorama urllib3
   ```

2. **Install and Setup Ollama**:
   ```bash
   # Start Ollama service
   ollama serve
   
   # Download the AI model
   ollama pull llama3.2:1b
   ```

3. **Run Kiki AI**:
   ```bash
   python kiki_ai.py
   ```

## Usage

### Basic Chat
```
You: Hello Kiki!
Kiki: Hello! I'm Kiki, your multilingual AI companion! I can chat in many languages and learn from the internet!

You: ¿Hablas español?
Kiki: ¡Hola! Soy Kiki, tu compañera AI multilingüe! ¡Puedo chatear en muchos idiomas y aprender de internet!
```

### Learning from the Internet
```
You: What is quantum computing?
Kiki: 🔍 Searching the internet for: quantum computing
Kiki: Quantum computing is a revolutionary technology that uses quantum mechanical phenomena...
```

### View Learning Statistics
```
You: stats
🧠 KIKI'S LEARNING STATISTICS
==================================================
📚 Languages supported: 12
🔤 Cached translations: 45
🌐 Topics learned: 8
📝 Facts collected: 127
🔍 Searches performed: 23
📊 Average source reliability: 0.78
💭 Vocabulary learned: 1,234 words
📖 Phrases learned: 567
🔄 Conversation patterns: 89
==================================================
```

## 🏗️ Project Structure

```
neuro-ai-project/
├── kiki_ai.py              # Main AI assistant
├── multilingual_system.py   # Multilingual support
├── internet_learning.py     # Internet learning system
├── learning_system.py       # General learning system
├── setup.py                 # Setup script
├── README.md               # This file
└── data/                   # Learning data storage
    ├── languages.json
    ├── translations.json
    ├── internet_knowledge.json
    ├── learned_facts.json
    └── search_history.json
```

## System Components

### 1. KikiAI (Main Class)
The central AI assistant that coordinates all systems:
- Personality management
- Response generation
- Memory management
- System integration

### 2. MultilingualSystem
Handles all language-related functionality:
- Language detection
- Translation services
- Cultural adaptation
- Language learning

### 3. InternetLearningSystem
Manages internet-based learning:
- Web search capabilities
- Information extraction
- Source reliability assessment
- Knowledge base management

### 4. LearningSystem
General learning and adaptation:
- Vocabulary learning
- Pattern recognition
- Conversation analysis
- Response improvement

## Configuration

### Language Settings
```python
# In kiki_ai.py
self.user_language = 'english'     # Default language
self.auto_translate = True         # Auto-translate responses
```

### Learning Settings
```python
# In kiki_ai.py
self.internet_learning_enabled = True  # Enable internet learning
```

### Supported Languages(12)
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Japanese (ja)
- Chinese (zh)
- Korean (ko)
- Russian (ru)
- Arabic (ar)
- Hindi (hi)

##  Troubleshooting

### Common Issues

1. **Ollama not running**:
   ```
   ⚠️ Ollama server is not running!
   Please start Ollama first by running: ollama serve
   ```
   **Solution**: Start Ollama service before running Kiki AI

2. **Model not found**:
   ```
   Error: Model llama3.2:1b not found
   ```
   **Solution**: Download the model with `ollama pull llama3.2:1b`

3. **Translation errors**:
   - Check internet connection
   - Translation service may be temporarily unavailable
   - Falls back to original language

4. **Internet learning not working**:
   - Verify internet connection
   - Check if search APIs are accessible
   - Review firewall settings

### Performance Tips

1. **Faster Responses**: Use smaller AI models
2. **Better Translation**: Ensure stable internet connection
3. **Memory Management**: Clear old data periodically
4. **Learning Accuracy**: Verify source reliability

## Commands

- `quit` or `exit`: Exit the chat
- `stats`: View learning statistics
- Type in any language to chat
- Ask questions to trigger internet learning

## Privacy & Security

- **Local AI**: Uses local Ollama models for privacy
- **Data Storage**: All learning data stored locally
- **Web Requests**: Only searches public information
- **No Personal Data**: Does not store personal information

## Future Enhancements

- Voice interaction support
- More language models
- Advanced web scraping
- Plugin system
- Mobile app integration
- Cloud synchronization

## Contributing

Feel free to contribute to Kiki AI by:
1. Adding new languages
2. Improving translation accuracy
3. Enhancing learning algorithms
4. Adding new features
5. Fixing bugs

## License

This project is open source and available under the MIT License.

## Support

For questions or support:
- Check the troubleshooting section
- Review the code documentation
- Test with different inputs
- Verify system requirements
- ask me
