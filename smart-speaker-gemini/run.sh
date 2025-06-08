#!/bin/bash
echo "🎙️ Starting Gemini Smart Speaker..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your GEMINI_API_KEY"
    exit 1
fi

# Check if API key is set
if grep -q "your_gemini_api_key_here" .env; then
    echo "❌ Please set your actual Gemini API key in .env file"
    echo "Get your API key from: https://makersuite.google.com/app/apikey"
    exit 1
fi

# Run the smart speaker
uv run python smart_speaker.py
