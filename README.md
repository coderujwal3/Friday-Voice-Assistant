# Virtual Voice Assistant

Friday is a Python-based voice assistant that listens for a wake word, speaks responses, and supports optional face registration/authentication.

## Project files

- `main.py` – application entry point. Calls `fridayAssistant.wakeup()`.
- `fridayAssistant.py` – assistant core logic, speech I/O, command handling, and wake-word support.
- `config.py` – configuration constants such as wake word and shutdown phrase.
- `register_face.py` – captures a face embedding from the webcam and saves it to `face_db/ujwal.npy`.
- `authenticate.py` – verifies the current webcam user against the registered face.
- `requirements.txt` – required Python packages.
- `face_db/` – stores saved face embedding data.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

> Optional: `sketchpy` is included as an extra visual feature, but it is not required for the core assistant.

## Run the assistant

Start Friday with:

```bash
python main.py
```

The assistant will launch and speak the provided startup message. By default, the wake word is defined in `config.py`:

- `WAKE_WORD = "friday"`
- `SHUT_DOWN = "shutdown"`

## Face registration and authentication

To register a face for authentication, run:

```bash
python register_face.py
```

Then press `S` when your face is detected. The face embedding is saved to `face_db/ujwal.npy`.

To verify a registered user with the webcam:

```bash
python authenticate.py
```

If authentication is successful, `authenticate()` returns `True`.

## Notes

- The assistant uses `pyttsx3` for text-to-speech and `SpeechRecognition` for voice input.
- `pyaudio` or your microphone driver must be available for audio capture.
- `insightface` and `onnxruntime` are used for face registration and authentication.
- On Windows, camera and microphone permissions must be enabled.

## License

Use this project for personal experimentation and learning.

