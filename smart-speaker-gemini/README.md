# Gemini Smart Speaker

A voice-controlled smart speaker powered by Google's Gemini AI. Works on both macOS and Raspberry Pi.

## Features

- 🎙️ Voice activation with customizable wake words
- 🤖 Powered by Google's Gemini AI
- 🔊 Text-to-speech responses
- 💬 Conversation memory
- 🎛️ Volume control commands
- ⚡ Platform-specific optimizations for macOS and Raspberry Pi

## Prerequisites

### macOS
- Python 3.11 or higher
- UV package manager
- Microphone access permissions

### Raspberry Pi
- Raspberry Pi OS (Bullseye or newer)
- Python 3.11 or higher
- UV package manager
- USB microphone or equivalent
- Speakers/audio output device

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd smart-speaker-gemini
```

2. Create a .env file with your Gemini API key:
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

3. Make the scripts executable:
```bash
chmod +x run.sh test_audio.sh
```

4. Run the setup script:
```bash
./run.sh
```

The script will automatically detect your platform and install the necessary dependencies.

## Hardware Setup (Raspberry Pi)

1. Connect a USB microphone
2. Connect speakers or headphones
3. Run the audio test script to verify your setup:
```bash
./test_audio.sh
```

## Usage

1. Start the smart speaker:
```bash
./run.sh
```

2. Say one of the wake words:
   - "hey assistant"
   - "hello gemini"
   - "smart speaker"
   - "hey speaker"

3. After the beep, speak your command or question

### Special Commands

- "what time is it" - Get current time
- "what day is it" - Get current date
- "speak louder/quieter" - Adjust volume
- "clear conversation" - Reset conversation history
- "goodbye" or "stop listening" - Exit the program

## Troubleshooting

### Raspberry Pi

1. No audio output:
   - Check audio output: `aplay -l`
   - Test speakers: `speaker-test -t sine`
   - Adjust volume: `alsamixer`

2. Microphone issues:
   - Check input devices: `arecord -l`
   - Test recording: `arecord -d 5 test.wav`
   - Verify USB microphone is detected

### macOS

1. Microphone access:
   - Grant microphone permissions in System Preferences
   - Verify input device in Sound preferences

2. Audio output issues:
   - Check default output device
   - Verify system volume

## Project Structure

- `smart_speaker.py` - Main application logic
- `platform_utils.py` - Platform-specific audio handling
- `run.sh` - Platform-aware startup script
- `test_audio.sh` - Audio setup verification
- `.env` - Configuration file for API keys

## Contributing

Feel free to submit issues and enhancement requests!