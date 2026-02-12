# Tomoka AI

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

### Basic LLM Features
- **Personality-driven Responses**: A small set of templates gives the assistant a friendly tone
- **Memory System**: Remembers recent conversation snippets locally
- **Status & Health**: Use the `status` command to get reachability and simple stats
- **Local LLM Support**: Optional Ollama integration if you configure it

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

3. **Start the assistant**:
   ```bash
   python end_project.py
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

3. **Run the assistant**:
   ```bash
   python end_project.py
   ```

## Usage

### Basic Chat
```
You: Hello Tomoka!
Tomoka: Hello! I'm Tomoka, your multilingual assistant. I can try to chat in many languages and look up simple facts.

You: ¿Hablas español?
Tomoka: ¡Hola! Puedo responder en español si lo prefieres (intento de traducción).
```

### Learning from the Internet
```
You: What is quantum computing?
Kiki: Searching the internet for: quantum computing
Kiki: Quantum computing is a revolutionary technology that uses quantum mechanical phenomena...
```

### View Status & Health
```
You: status
TOMOKA'S STATUS
==================================================
Name: Tomoka
LLM reachable: yes/no (depends on local setup)
Internet: reachable/unreachable
Vocabulary words: N
Learned topics: N
Cached translations: N
Memory entries: N
==================================================
```

##  Project Structure

```
Project/
├── end_project.py           # Main assistant runner (start here)
├── multilingual_system.py   # Multilingual support
├── internet_learning.py     # Internet learning system
├── learning_system.py       # General learning system
├── setup.py                 # Optional setup script
├── README.md                # This file
└── data/                    # Learning data storage
   ├── languages.json
   ├── translations.json
   ├── internet_knowledge.json
   ├── learned_facts.json
   └── search_history.json
```

## System Components

### 1. Main assistant (Tomoka)
The central assistant coordinates the systems:
- Personality context and simple prompt templates
- Basic response generation via a local LLM (if configured)
- Memory management (local JSON)
- Optional internet lookups

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
   Ollama server is not running!
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
- `status`: View current status and simple stats
- Type in any language to chat (the assistant will attempt to detect language)
- Ask questions to trigger internet learning (if enabled)

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

