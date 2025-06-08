#!/bin/bash

# Detect platform
is_raspberry_pi=false
if [ -f /proc/device-tree/model ]; then
    if grep -qi "raspberry pi" /proc/device-tree/model; then
        is_raspberry_pi=true
        echo "📍 Running on Raspberry Pi"
    fi
fi

echo "🎤 Testing audio setup..."

# Platform-specific audio checks
if [ "$is_raspberry_pi" = true ]; then
    echo "Checking audio hardware..."
    # List audio devices
    arecord -l
    aplay -l
    
    # Check if USB microphone is connected
    if arecord -l | grep -q "USB"; then
        echo "✅ USB microphone detected"
    else
        echo "⚠️ No USB microphone detected. Please connect a USB microphone."
    fi
    
    # Test speaker output
    echo "Testing speaker output... (you should hear a tone)"
    speaker-test -t sine -f 440 -l 1 >/dev/null 2>&1
    
    # Check audio levels
    echo "Current audio levels:"
    amixer sget 'Master'
fi

# Test microphone using Python
echo "Testing microphone... (will record for 3 seconds)"
python3 -c "
import speech_recognition as sr
import sys
from platform_utils import PlatformAudio

try:
    platform = PlatformAudio()
    r = sr.Recognizer()
    microphone = platform.init_microphone(r)
    
    with microphone as source:
        print('\\nAdjusting for ambient noise...')
        r.adjust_for_ambient_noise(source)
        
        print('Say something...')
        audio = r.listen(source, timeout=3)
        
        print('Recognizing...')
        text = r.recognize_google(audio)
        print(f'You said: {text}')
        
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
"

# Test text-to-speech
echo "Testing text-to-speech..."
python3 -c "
from platform_utils import PlatformAudio
import sys

try:
    platform = PlatformAudio()
    engine = platform.init_text_to_speech()
    engine.say('Audio test successful! Your smart speaker is ready.')
    engine.runAndWait()
    print('✅ Text-to-speech working!')
except Exception as e:
    print(f'❌ TTS Error: {e}')
    sys.exit(1)
"

echo "✅ Audio test complete!"
