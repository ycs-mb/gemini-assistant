#!/bin/bash
echo "🎤 Testing audio setup..."

# Test microphone
echo "Testing microphone... (will record for 3 seconds)"
python3 -c "
import speech_recognition as sr
import sys

try:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Available microphones:')
        for i, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f'  {i}: {name}')
        
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
import pyttsx3
import sys

try:
    engine = pyttsx3.init()
    engine.say('Audio test successful! Your smart speaker is ready.')
    engine.runAndWait()
    print('✅ Text-to-speech working!')
except Exception as e:
    print(f'❌ TTS Error: {e}')
    sys.exit(1)
"

echo "✅ Audio test complete!"
