import subprocess
import sys
import time

def install_requirements():
    """Install required Python packages"""
    requirements = [
        'requests',
        'colorama',  # For colored terminal output
        'urllib3',   # For URL parsing
        'hashlib',   # For generating hashes (usually built-in)
    ]
    
    print("Installing required Python packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def download_ai_model():
    """Download the AI model using Ollama"""
    print("\nDownloading AI model (this may take a few minutes)...")
    
    try:
        # Start ollama serve in background
        print("Starting Ollama service...")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait a bit for the service to start
        time.sleep(3)
        
        # Pull the model
        print("Downloading llama3.2:1b model...")
        result = subprocess.run(["ollama", "pull", "llama3.2:1b"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ AI model downloaded successfully!")
            return True
        else:
            print(f"❌ Failed to download model: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Kiki AI Project with Multilingual & Internet Learning...")
    print("=" * 50)
    
    # Install Python packages
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return
    
    # Download AI model
    if not download_ai_model():
        print("❌ Setup failed during model download")
        return
    
    print("\n✅ Setup completed successfully!")
    print("=" * 50)
    print("🎉 You can now run Kiki AI with: python kiki_ai.py")
    print("💡 Features: Multilingual chat, Internet learning, Advanced AI")
    print("=" * 50)

if __name__ == "__main__":
    main()
