#!/usr/bin/env python3
"""Platform-specific utilities for the smart speaker"""
import platform
import pyttsx3
import speech_recognition as sr
import sys
import subprocess
import os

class PlatformAudio:
    def __init__(self):
        self.system = platform.system().lower()
        self.is_raspberry_pi = self._is_raspberry_pi()
        self.is_linux = self.system == 'linux'
        
    def _is_raspberry_pi(self):
        """Check if running on Raspberry Pi"""
        try:
            with open('/proc/device-tree/model', 'r') as f:
                return 'raspberry pi' in f.read().lower()
        except:
            return False

    def _ensure_linux_audio_deps(self):
        """Ensure required Linux audio packages are installed"""
        if not self.is_linux:
            return

        try:
            # Check for espeak
            espeak_result = subprocess.run(['which', 'espeak'], capture_output=True)
            if espeak_result.returncode != 0:
                print("⚠️ espeak not found. Please install it:")
                print("sudo apt-get install espeak")
                sys.exit(1)

            # Check for ALSA utils if needed
            if not os.path.exists('/usr/include/alsa/asoundlib.h'):
                print("⚠️ ALSA development files not found. Please install:")
                print("sudo apt-get install libasound2-dev")
                sys.exit(1)

            # Check if pulseaudio is running
            pulse_result = subprocess.run(['pulseaudio', '--check'])
            if pulse_result.returncode != 0:
                print("⚠️ Starting PulseAudio...")
                subprocess.run(['pulseaudio', '--start'])

        except Exception as e:
            print(f"⚠️ Error checking audio dependencies: {e}")

    def init_text_to_speech(self):
        """Initialize text-to-speech engine based on platform"""
        if self.is_linux:
            self._ensure_linux_audio_deps()
            
            # Use espeak on Linux
            engine = pyttsx3.init('espeak')
            engine.setProperty('rate', 150)  # Slower rate for clearer speech
            engine.setProperty('volume', 0.9)
            
            # Try to find English voice
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
                    
        elif self.is_raspberry_pi:
            engine = pyttsx3.init('espeak')  # Use espeak on Raspberry Pi
            engine.setProperty('rate', 150)  # Slower rate for clearer speech
            engine.setProperty('volume', 0.9)
            
            # Try to find English voice
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        else:
            # macOS or Windows
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # Try to find preferred voice
            preferred_voices = ['Samantha', 'Victoria', 'Fiona', 'Moira']
            for voice in voices:
                if any(name.lower() in voice.name.lower() for name in preferred_voices):
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 0.9)
            
        return engine

    def init_microphone(self, recognizer):
        """Initialize and configure microphone based on platform"""
        try:
            if self.is_linux:
                self._ensure_linux_audio_deps()
                
            if self.is_raspberry_pi or self.is_linux:
                # On Linux systems, we might need to specify the device index
                print("\nAvailable microphones:")
                for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
                    print(f"  {i}: {microphone_name}")
                
                # Try to find USB microphone first
                device_index = None
                for i, name in enumerate(sr.Microphone.list_microphone_names()):
                    if 'usb' in name.lower():
                        device_index = i
                        print(f"Selected USB microphone: {name}")
                        break
                
                if device_index is None:
                    # Try to find a default input device
                    for i, name in enumerate(sr.Microphone.list_microphone_names()):
                        if any(x in name.lower() for x in ['input', 'mic', 'default']):
                            device_index = i
                            print(f"Selected input device: {name}")
                            break
                
                microphone = sr.Microphone(device_index=device_index)
            else:
                # Default microphone for other platforms
                microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with microphone as source:
                print("\n🔧 Adjusting for ambient noise... Please stay quiet.")
                recognizer.adjust_for_ambient_noise(source, duration=2)
            
            # Configure recognition settings
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8
            
            print("✅ Microphone setup complete!")
            return microphone
            
        except Exception as e:
            print(f"❌ Error initializing microphone: {e}")
            if self.is_linux:
                print("\nTroubleshooting tips for Linux:")
                print("1. Make sure you have the required packages:")
                print("   sudo apt-get install python3-pyaudio portaudio19-dev")
                print("2. Check if your microphone is detected:")
                print("   arecord -l")
                print("3. Test microphone recording:")
                print("   arecord -d 5 test.wav")
            sys.exit(1)