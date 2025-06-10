# Gemini Assistant

Gemini Assistant is a prototype smart speaker powered by Google Gemini. It listens for wake words, transcribes your speech, sends it to the Gemini API and speaks the response. It includes a simple conversation history and supports a few special commands like asking for the time or adjusting volume.

## Features
- Wake word detection
- Speech recognition (SpeechRecognition + PyAudio)
- Responses generated with Google Gemini
- Text‑to‑speech with pyttsx3
- Simple command handling (time, date, quit, volume)

## Requirements
- Python 3.11+
- An API key for Google Gemini (set `GEMINI_API_KEY` in a `.env` file)
- Audio input/output working on your machine

### Linux Requirements
If you're on Linux, you'll need these additional packages:
```bash
# For audio and speech support
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev
sudo apt-get install espeak libasound2-dev
sudo apt-get install pulseaudio

# Start pulseaudio if not running
pulseaudio --start
```

## Installation
```bash
# Clone the repository
$ git clone <repo-url>
$ cd gemini-assistant/smart-speaker-gemini

# Install dependencies (requires uv or pip)
$ pip install uv
$ uv pip install -e .
# or alternatively
$ pip install google-generativeai pyaudio pygame python-dotenv pyttsx3 requests speechrecognition
```

## Usage
1. Create a `.env` file inside `smart-speaker-gemini` containing
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
2. Run the assistant:
   ```bash
   $ ./run.sh
   ```
   This script verifies the `.env` file then launches `smart_speaker.py` using `uv run`.

When the speaker prints the wake words, say one of them to start issuing commands. The assistant will speak the Gemini response. Say "goodbye" or "stop listening" to exit.

## Testing Audio
Use `test_audio.sh` to test your microphone and text-to-speech setup before running the assistant:
```bash
$ ./test_audio.sh
```

### Linux Audio Troubleshooting
If you encounter audio issues on Linux:

1. Check if your microphone is detected:
   ```bash
   arecord -l
   ```

2. Test microphone recording:
   ```bash
   arecord -d 5 test.wav
   ```

3. Make sure PulseAudio is running:
   ```bash
   pulseaudio --check
   pulseaudio --start  # if not running
   ```

4. Check audio playback:
   ```bash
   speaker-test -t wav
   ```

## Repository Layout
- `smart-speaker-gemini/smart_speaker.py` – main application code
- `smart-speaker-gemini/platform_utils.py` - platform-specific audio handling
- `smart-speaker-gemini/run.sh` – helper script to run the smart speaker
- `smart-speaker-gemini/test_audio.sh` – test your audio configuration
- `smart-speaker-gemini/pyproject.toml` – Python project definition

## License
This project is distributed for demonstration purposes only and has no specific license.
