# Virtual Voice Assistant
Friday is a lightweight Python-based personal voice assistant that listens for a wake word, speaks responses, and optionally uses webcam face embeddings for a simple authentication flow.

This README explains repository layout, how to set up and run the project, and the typical execution flow (clone → install → register/authenticate → run).

Project structure
- `main.py` — application entry point. Calls `wakeup()` from `fridayAssistant.py`.
- `fridayAssistant.py` — assistant core logic: TTS/STT helpers, wake-word loop, command handlers, utility features.
- `config.py` — (required) minimal configuration: `WAKE_WORD` and `SHUT_DOWN` strings. See "Create config.py" below.
- `register_face.py` — capture a single face embedding from the webcam and save it as a .npy file in `face_db/`.
- `authenticate.py` — read saved embeddings and try to match the current webcam face; returns authentication status and the matched user name.
- `requirements.txt` — Python dependencies used by the project.
- `face_db/` — directory containing saved NumPy face embeddings (.npy). Example files: `ujwal.npy`, `gaurav.npy`.

Minimum required file layout (example):

- face_db/
	- ujwal.npy
	- gaurav.npy
- authenticate.py
- fridayAssistant.py
- main.py
- register_face.py
- requirements.txt

Quick start

1. Clone the repository:

```bash
git clone <repo-url>
cd Virtual_Voice_Assistant
```

2. Create and activate a Python virtual environment (recommended):

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Create config.py (required)

The repository requires a small `config.py` containing at least two string constants used by the assistant:

```python
# config.py
WAKE_WORD = "friday"
SHUT_DOWN = "turn off assistant"
```

Place `config.py` in the project root next to `main.py`.

Registering a face (optional, for authentication)

1. Ensure your webcam is working and allowed for the Python process.
2. Run:

```bash
python register_face.py
```

3. When the camera window appears, press `s` (lowercase) while your face is visible. The script will save a NumPy embedding to `face_db/<name>.npy` where `<name>` is the value you pass into `register_face()` when calling the function (the example script may accept a name parameter or you can modify it to prompt for one).

Notes about `register_face.py`:
- The script uses `insightface` to detect the face and compute an embedding.
- Exactly one face must be visible when you press `s` — otherwise the script will prompt you to try again.

Authenticating a user

Run the authentication utility to check the live camera feed against saved embeddings:

```bash
python authenticate.py
```

What to expect:
- The camera window shows bounding boxes and a label (matched user or "Unknown" with the similarity score).
- On successful match (similarity above threshold), the script prints and returns the authenticated user name.

Running the assistant

Start the assistant using the project entrypoint:

```bash
python main.py
```

Execution flow (high-level)
- `main.py` imports and calls `wakeup()` from `fridayAssistant.py`.
- `fridayAssistant.wakeup()` speaks the startup message then enters a loop listening for the configured `WAKE_WORD`.
- When wake-word is detected, the assistant may run an authentication step (if enabled in the code) by calling functions from `authenticate.py`.
- If authentication succeeds (or authentication is not required), the assistant continues to accept voice commands and executes built-in handlers.

Important runtime notes
- Microphone: `SpeechRecognition` requires a working microphone and (for some OSes) `pyaudio` installed. On Windows installing `pyaudio` may require a prebuilt wheel matching your Python version.
- Camera: `insightface` / `onnxruntime` require a functioning camera and the appropriate binary dependencies. On Windows, ensure the app has Camera permission.
- Performance: Face detection and embedding inference may be slow on CPUs without ONNX GPU support. Consider installing `onnxruntime-gpu` if you have a compatible GPU.

Troubleshooting
- If the camera cannot be opened, check other apps using the camera and Windows privacy settings.
- If `pyttsx3` fails to initialize, ensure you have a working TTS backend installed (on Windows the default SAPI5 should be available).
- For speech recognition network errors, the default recognizer uses Google Web Speech API which requires internet access.

Security and privacy
- Stored face embeddings in `face_db/` are NumPy arrays — treat them as sensitive biometric-related data and do not share them publicly.

Extending and customization
- `fridayAssistant.py` contains many helper functions and optional integrations (sketching, screenshots, small utilities). You can extend the command handlers to add more functionality.
- The wake-word and shutdown phrase are controlled in `config.py` — change them to personalize the assistant.

Next steps (suggested)
- Create the `config.py` file with your preferred wake word and shutdown phrase.
- Run `python register_face.py` to add at least one user embedding (optional but required for face authentication).
- Run `python authenticate.py` to verify the saved face(s).
- Launch the assistant: `python main.py`.

If you'd like, I can add a sample `config.py` to the repository and/or improve `register_face.py` to accept a name from the command line. Tell me which you prefer.

License
- This repository is intended for learning and experimentation.

