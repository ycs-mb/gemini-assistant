#!/bin/bash
echo "🎙️ Starting Gemini Smart Speaker..."

# Detect if running on Raspberry Pi
is_raspberry_pi=false
if [ -f /proc/device-tree/model ]; then
    if grep -qi "raspberry pi" /proc/device-tree/model; then
        is_raspberry_pi=true
        echo "📍 Detected Raspberry Pi platform"
    fi
fi

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

# Install platform-specific dependencies on Raspberry Pi
if [ "$is_raspberry_pi" = true ]; then
    echo "🔧 Checking Raspberry Pi dependencies..."
    
    # Check and install system packages
    for pkg in python3-dev portaudio19-dev espeak alsa-utils; do
        if ! dpkg -l | grep -q "^ii  $pkg "; then
            echo "📦 Installing $pkg..."
            sudo apt-get update && sudo apt-get install -y $pkg
        fi
    done
    
    # Configure audio
    echo "🔊 Configuring audio..."
    amixer sset 'Master' 75%
    
    # Test audio setup
    echo "🎵 Testing audio output..."
    speaker-test -t sine -f 440 -l 1 >/dev/null 2>&1
fi

# Run the smart speaker
echo "🚀 Starting smart speaker..."
uv run python smart_speaker.py
