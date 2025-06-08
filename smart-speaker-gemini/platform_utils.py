#!/usr/bin/env python3
"""Platform-specific utilities for the smart speaker"""
import platform
import pyttsx3
import speech_recognition as sr
import sys

class PlatformAudio:
    def __init__(self):
        self.system = platform.system().lower()
        self.is_raspberry_pi = self._is_raspberry_pi()
        
    def _is_raspberry_pi(self):
        """Check if running on Raspberry Pi"""
        try:
            with open('/proc/device-tree/model', 'r') as f:
                return 'raspberry pi' in f.read().lower()
        except:
            return False

    def init_text_to_speech(self):
        """Initialize text-to-speech engine based on platform"""
        if self.is_raspberry_pi:
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
            # macOS or other systems
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
            if self.is_raspberry_pi:
                # On Raspberry Pi, we might need to specify the device index
                # List available audio devices
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
            sys.exit(1)