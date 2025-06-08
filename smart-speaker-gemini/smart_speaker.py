#!/usr/bin/env python3
"""
Smart Speaker with Google Gemini Integration
macOS Voice Assistant Prototype
"""

DEBUG = True  # Set to False to disable debug logs

import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import threading
import time
import os
import pygame
import json
from datetime import datetime
from dotenv import dotenv_values
import sys
import math  # Needed for play_beep

class GeminiSmartSpeaker:
    def __init__(self):
        self.debug_enabled = DEBUG
        self.log("Initializing Gemini Smart Speaker...")
        
        # Load environment variables
        env_vars = dotenv_values(".env")
        self.log("Environment variables loaded")
        
        # Initialize Gemini AI
        api_key = env_vars.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.log("Gemini API configured")
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.log("Speech recognition initialized")
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.configure_tts()
        
        # Initialize pygame for sound effects
        pygame.mixer.init()
        self.log("Pygame mixer initialized")
        
        # Wake word settings
        self.wake_words = ["hey assistant", "hello gemini", "smart speaker", "hey speaker"]
        self.listening = False
        self.conversation_history = []
        self.log(f"Wake words set: {self.wake_words}")
        
        # Configure microphone
        self.setup_microphone()
        
        print("✅ Gemini Smart Speaker initialized successfully!")

    def log(self, message):
        if self.debug_enabled:
            print(f"[DEBUG] {message}")

    def configure_tts(self):
        """Configure text-to-speech settings"""
        self.log("Configuring TTS engine...")
        voices = self.tts_engine.getProperty('voices')
        
        # Try to find a good voice (prefer female voices for assistant)
        preferred_voices = ['Samantha', 'Victoria', 'Fiona', 'Moira']
        selected_voice = None
        
        for voice in voices:
            for preferred in preferred_voices:
                if preferred.lower() in voice.name.lower():
                    selected_voice = voice
                    break
            if selected_voice:
                break
        
        if not selected_voice and voices:
            selected_voice = voices[0]  # Use first available voice
        
        if selected_voice:
            self.tts_engine.setProperty('voice', selected_voice.id)
            print(f"🎙️ Using voice: {selected_voice.name}")
            self.log(f"TTS voice set to {selected_voice.name}")
        
        # Set speech rate and volume
        self.tts_engine.setProperty('rate', 180)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        self.log("TTS rate and volume configured.")

    def setup_microphone(self):
        """Setup and calibrate microphone"""
        self.log("Setting up microphone...")
        print("🎤 Setting up microphone...")
        
        # List available microphones
        print("\nAvailable microphones:")
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  {i}: {microphone_name}")
        self.log("Microphone list printed.")
        
        # Adjust for ambient noise
        print("\n🔧 Adjusting for ambient noise... Please stay quiet for 2 seconds.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        self.log("Ambient noise adjusted.")
        
        # Set recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        print("✅ Microphone setup complete!")
        self.log("Microphone setup complete with thresholds configured.")

    def speak(self, text):
        """Convert text to speech"""
        self.log(f"Speaking text: {text}")
        print(f"🗣️ Speaking: {text}")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.log("Finished speaking.")
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            self.log(f"TTS error: {e}")

    def play_beep(self, frequency=800, duration=0.1):
        """Play a beep sound to indicate listening"""
        self.log("Playing beep sound.")
        try:
            sample_rate = 2200
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * math.sin(frequency * 2 * math.pi * i / sample_rate)
                arr.append(int(wave))
            # Note: This is a simplified beep - in practice you might want to use
            # a pre-recorded sound file or a more sophisticated audio generation
            print("🔔 *beep*")
            self.log("Beep played.")
        except Exception as e:
            print("🔔 *beep*")  # Fallback to text indication
            self.log(f"Beep generation error: {e}")

    def listen_for_wake_word(self):
        """Continuously listen for wake word"""
        self.log("Listening for wake word...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
            self.log("Audio captured for wake word recognition.")
            
            try:
                text = self.recognizer.recognize_google(audio).lower()
                self.log(f"Recognized text: {text}")
                print(f"👂 Heard: {text}")
                
                for wake_word in self.wake_words:
                    if wake_word in text:
                        self.log(f"Wake word '{wake_word}' detected in '{text}'")
                        print(f"🎯 Wake word detected: '{wake_word}' in '{text}'")
                        return True
            except sr.UnknownValueError:
                self.log("Google Speech Recognition could not understand audio.")
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                self.log(f"Speech recognition request error: {e}")
        except sr.WaitTimeoutError:
            self.log("Microphone wait timeout for wake word.")
        except Exception as e:
            print(f"❌ Listening error: {e}")
            self.log(f"Error in listen_for_wake_word: {e}")
            
        return False

    def listen_for_command(self):
        """Listen for user command after wake word"""
        self.log("Listening for command after wake word.")
        print("🎤 Listening for your command...")
        self.play_beep()
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=15)
            self.log("Audio captured for command recognition.")
            
            try:
                command = self.recognizer.recognize_google(audio)
                print(f"📝 Command: {command}")
                self.log(f"Recognized command: {command}")
                return command
            except sr.UnknownValueError:
                self.log("Could not understand command audio.")
                print("❓ Could not understand the command")
                self.speak("I'm sorry, I didn't understand that. Could you please repeat?")
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                self.log(f"Speech recognition request error while listening for command: {e}")
                self.speak("I'm having trouble with speech recognition right now.")
        except sr.WaitTimeoutError:
            self.log("Command listening timed out.")
            print("⏰ Listening timeout")
            self.speak("I didn't hear anything. Try saying the wake word again.")
        except Exception as e:
            print(f"❌ Command listening error: {e}")
            self.log(f"Error in listen_for_command: {e}")
            
        return None

    def get_gemini_response(self, user_input):
        """Get response from Google Gemini"""
        self.log(f"Getting Gemini response for input: {user_input}")
        try:
            print("🤖 Getting Gemini response...")
            conversation_context = ""
            if self.conversation_history:
                conversation_context = "\n".join([
                    f"User: {item['user']}\nAssistant: {item['assistant']}" 
                    for item in self.conversation_history[-3:]
                ])
                self.log("Prepared conversation context.")
            
            prompt = f"""You are a helpful voice assistant in a smart speaker, similar to Google Home or Alexa. 
            Keep your responses concise and conversational, typically 1-2 sentences unless asked for detailed information.
            Be friendly, natural, and helpful.
            
            Previous conversation:
            {conversation_context}
            
            Current user input: {user_input}
            
            Please provide a helpful response:"""
            self.log("Prompt created for Gemini response.")
            
            response = self.model.generate_content(prompt)
            assistant_response = response.text
            self.log(f"Gemini response received: {assistant_response}")
            print(assistant_response)
            
            self.conversation_history.append({
                'user': user_input,
                'assistant': assistant_response,
                'timestamp': datetime.now().isoformat()
            })
            
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
                self.log("Conversation history trimmed.")
            return assistant_response
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            self.log(f"Error in get_gemini_response: {e}")
            return "I'm sorry, I'm having trouble connecting to my brain right now. Please try again."

    def handle_special_commands(self, command):
        """Handle special commands like time, system commands, etc."""
        self.log(f"Checking special commands for: {command}")
        command_lower = command.lower()
        
        if any(phrase in command_lower for phrase in ["what time is it", "current time", "time now"]):
            current_time = datetime.now().strftime("%I:%M %p")
            self.log("Returning time command response.")
            return f"The current time is {current_time}"
        
        elif any(phrase in command_lower for phrase in ["what day is it", "what's the date", "today's date"]):
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            self.log("Returning date command response.")
            return f"Today is {current_date}"
        
        elif any(phrase in command_lower for phrase in ["stop listening", "goodbye", "shut down", "quit"]):
            self.log("Stop listening command detected.")
            return "STOP_LISTENING"
        
        elif any(phrase in command_lower for phrase in ["clear conversation", "reset conversation", "start over"]):
            self.conversation_history = []
            self.log("Conversation history cleared by special command.")
            return "Conversation history cleared. How can I help you?"
        
        elif any(phrase in command_lower for phrase in ["lower volume", "speak quieter"]):
            current_volume = self.tts_engine.getProperty('volume')
            new_volume = max(0.1, current_volume - 0.2)
            self.tts_engine.setProperty('volume', new_volume)
            self.log(f"Volume lowered to {new_volume}")
            return f"Volume lowered to {int(new_volume * 100)}%"
        
        elif any(phrase in command_lower for phrase in ["raise volume", "speak louder"]):
            current_volume = self.tts_engine.getProperty('volume')
            new_volume = min(1.0, current_volume + 0.2)
            self.tts_engine.setProperty('volume', new_volume)
            self.log(f"Volume raised to {new_volume}")
            return f"Volume raised to {int(new_volume * 100)}%"
        
        self.log("No special command detected.")
        return None

    def run(self):
        """Main loop for the smart speaker"""
        self.log("Smart speaker main loop started.")
        print("\n" + "="*50)
        print("🎙️ GEMINI SMART SPEAKER READY!")
        print("="*50)
        print(f"Wake words: {', '.join(self.wake_words)}")
        print("Say 'goodbye' or 'stop listening' to exit")
        print("Press Ctrl+C to force quit")
        print("="*50 + "\n")
        
        self.speak("Hello! I'm your Gemini smart speaker. I'm ready to help!")
        
        try:
            while True:
                if self.listen_for_wake_word():
                    self.log("Wake word detected; switching to command mode.")
                    command = self.listen_for_command()
                    
                    if command:
                        special_response = self.handle_special_commands(command)
                        
                        if special_response == "STOP_LISTENING":
                            self.speak("Goodbye! Have a great day!")
                            self.log("Stop listening command issued; exiting main loop.")
                            break
                        elif special_response:
                            self.speak(special_response)
                        else:
                            self.log(f"Sending command to Gemini: {command}")
                            print("🤖 Processing command with Gemini...", command)
                            response = self.get_gemini_response(command)
                            self.speak(response)
                    
                    time.sleep(0.5)
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.log("KeyboardInterrupt caught; shutting down.")
            print("\n🛑 Shutting down smart speaker...")
            self.speak("Goodbye!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.log(f"Unexpected error in run loop: {e}")
            self.speak("I encountered an error and need to shut down.")

def main():
    """Main function"""
    print("🚀 Starting Gemini Smart Speaker...")
    env_vars = dotenv_values(".env")
    api_key = env_vars.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found!")
        print("Please set your Gemini API key in the .env file")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        return
    
    try:
        
        speaker = GeminiSmartSpeaker()
        speaker.log("Starting main speaker loop.")
        speaker.run()
    except Exception as e:
        print(f"❌ Failed to start smart speaker: {e}")

if __name__ == "__main__":
    main()