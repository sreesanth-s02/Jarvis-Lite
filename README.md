# Jarvis-Lite

> A lightweight offline voice assistant built with Python that listens for voice commands and performs useful desktop and web actions on Windows.

---

## Overview

Jarvis-Lite is a Python-based voice assistant designed to perform real-time tasks through spoken commands on Windows systems. The project includes modular components for voice handling, command routing, task dispatching, storage management, and offline speech recognition. It's built as a practical tool to automate desktop and web-based workflows through natural voice interaction.

> **Platform Support:** Currently supported and tested on Windows only.

---

## Features

- Voice-based assistant workflow powered by microphone input and offline speech recognition.
- Modular command architecture using folders like `commands/`, `router/`, and `dispatcher/`.
- Local storage and settings handling through `storage_manager/` and `settings_control/`.
- Offline speech model integration using `vosk-model-small-en-us-0.15` inside `models/`.
- Utility and support modules for social actions, logs, chat flow, and voice processing.
- Desktop application framework for easy integration and GUI support.

---

## Project Structure

```bash
Jarvis-Lite/
│
├── app.py                          # Main application entry point
├── main.py                         # Core runtime bootstrap
├── check.py                        # Environment and setup checks
├── mic_text.py                     # Microphone-to-text conversion helper
├── raw_mic_test.py                 # Raw microphone input testing
├── requirements.txt                # Python dependencies
│
├── chat/                           # Chat and dialogue logic
├── commands/                       # Command handlers and voice skills
├── dispatcher/                     # Central event dispatcher
├── logs/                           # Runtime logs and debugging
├── models/                         # Speech recognition models
│   └── vosk-model-small-en-us-0.15/
├── router/                         # Intent routing and command selection
├── settings_control/               # User configuration and preferences
├── social_actions/                 # Notifications and user interactions
├── storage_manager/                # Local data persistence
├── utils/                          # Shared utilities and helpers
└── voice/                          # Voice I/O pipeline and processing
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sreesanth-s02/Jarvis-Lite.git
cd Jarvis-Lite
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment (Windows)

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Assistant (Windows)

To start the assistant, run:

```bash
python app.py
```

This command launches the Jarvis-Lite voice assistant application.

---

## Example Voice Commands

Jarvis-Lite is designed to handle a variety of voice commands:

- Open notepad
- Open calculator
- Open bluetooth settings
- Play "Summertime Sadness" on YouTube
- Browse Ajith Kumar

These examples represent the kinds of desktop application launches and browser-based searches the assistant can perform.

---

## How It Works

Jarvis-Lite operates through a clean modular architecture where each component has a specific responsibility:

```text
Voice Input → Speech Recognition → Command Routing → Action Execution
```

### Core Workflow

1. **Voice Input:** Microphone stream is captured and processed.
2. **Speech Recognition:** Audio is converted to text using the offline Vosk model.
3. **Command Routing:** The router analyzes text and maps it to corresponding command handlers.
4. **Action Execution:** The appropriate command module executes the requested action (opening apps, searching web, etc.).
5. **Feedback:** Results are logged and optionally returned to the user via social actions.

---

## Important Files

- `app.py` — Main application entry point used to start the assistant.
- `main.py` — Core runtime and assistant bootstrap logic.
- `check.py` — Environment validation and microphone setup checks.
- `mic_text.py` — Handles microphone-to-text conversion and audio processing.
- `raw_mic_test.py` — Low-level microphone testing utility for debugging.
- `requirements.txt` — Lists all Python package dependencies.

---

## Tech Stack

### Core Technologies

- **Python 3.9+** — Primary programming language.
- **Vosk** — Offline speech recognition engine (vosk-model-small-en-us-0.15).
- **PyAudio** — Microphone input handling.
- **Windows OS APIs** — For desktop automation and application launching.

### Architecture

- **Modular Design:** Separate modules for commands, routing, dispatching, and storage.
- **Event-Driven:** Central dispatcher for coordinating voice events and command execution.
- **Configuration-Based:** User preferences and settings managed through `settings_control/`.
- **Persistent Storage:** Local file-based storage via `storage_manager/`.

---

## Work Done by Contributors

### Sreesanth S (sreesanth-s02)
### Eraianbu Damodharan (Eraianbu-Damodharan)

---

## Future Scope & Enhancements

### Phase 2: AI-Powered Features

- **AI-Generated Email Content**
  - Voice command like "Send email to [recipient]"
  - AI analyzes context and auto-generates professional email content
  - User can review and approve before sending
  - Integration with SMTP and email clients (Gmail, Outlook)

- **Intelligent Document Generation**
  - "Generate a Word document with [topic]"
  - AI creates formatted `.docx` files with relevant content
  - Support for templates and custom formatting
  - Export to PDF and other formats

- **Cross-Device File Transfer**
  - Voice command: "Send file to my phone"
  - Automatic file detection and transfer via local network
  - Support for Bluetooth, WiFi Direct, or cloud sync
  - Progress tracking and notifications

### Phase 3: Advanced NLU & Integration

- Improved natural language understanding for more flexible command phrasing.
- Multi-language support beyond English.
- Integration with smart home devices and IoT systems.
- Cloud backup and sync capabilities for settings and logs.

### Phase 4: User Interface & Experience

- Desktop GUI with real-time command visualization.
- System tray widget and always-on status indicator.
- Voice feedback and audio response system.
- Command history and analytics dashboard.

### Phase 5: Extended Capabilities

- Web API server for remote command execution.
- Mobile companion app for remote control.
- Custom wake-word training and detection.
- Plugin marketplace for community-created commands.
- Integration with productivity tools (Slack, Teams, Trello, etc.).

---

## Possible Improvements (Current Phase)

- Add more built-in voice commands for common tasks.
- Enhance error handling and user feedback mechanisms.
- Implement configuration file (JSON/YAML) for easy customization.
- Add unit tests for command modules.
- Improve logging and debugging tools.
- Create command templates for easy extension by developers.

---

## Installation & Dependency Notes

### System Requirements

- Windows 10 or later.
- Python 3.9 or higher.
- Working microphone and speakers.
- Internet connection for initial setup (downloading models).

### Audio Driver Setup

Ensure your microphone is properly configured in Windows audio settings. Test with `raw_mic_test.py` before running the full assistant.

---

## Offline Speech Recognition

This project uses the `vosk-model-small-en-us-0.15` model for offline speech recognition. This approach:

- Works without internet connectivity after initial download.
- Provides faster response times compared to cloud APIs.
- Ensures user privacy by keeping audio processing local.
- Reduces dependency on external services.

---

## Troubleshooting

### Microphone Not Detected

Run `check.py` to diagnose audio input issues:

```bash
python check.py
```

### Audio Recognition Issues

- Ensure you're in a quiet environment.
- Check microphone levels in Windows sound settings.
- Re-test with `raw_mic_test.py` to verify input.

### Command Not Recognized

- Speak clearly and at a normal pace.
- Check the router configuration to ensure your command phrase is registered.
- Review logs in `logs/` directory for debugging information.

---

## Sample Interaction

```text
User: Open notepad
Jarvis-Lite: Opening Notepad...

User: Open calculator
Jarvis-Lite: Opening Calculator...

User: Open bluetooth settings
Jarvis-Lite: Opening Bluetooth Settings...

User: Play summertime sadness in youtube
Jarvis-Lite: Playing "Summertime Sadness" on YouTube...

User: Browse Ajith Kumar
Jarvis-Lite: Searching for Ajith Kumar in browser...
```

---

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request.

### Contribution Guidelines

- Keep changes focused and well-documented.
- Add or update documentation for new features.
- Test thoroughly before submitting a PR.
- Follow existing code style and structure.

---

## License

This project does not currently have a license file. If you plan to use this project or contribute, we recommend adding a license such as MIT, Apache-2.0, or GPL-3.0. You can add a `LICENSE` file to the repository root.

---

## Contact & Support

For issues, feature requests, or questions:

- Open an issue on GitHub: https://github.com/sreesanth-s02/Jarvis-Lite/issues
- Contact contributors directly through GitHub profiles.

---

## Roadmap

- **Q2 2026:** Phase 2 implementation (AI email generation, document generation).
- **Q3 2026:** Phase 3 (cross-device file transfer, cloud integration).
- **Q4 2026:** Phase 4 (GUI redesign, enhanced UX).
- **2027:** Phase 5 (API server, mobile app, plugin marketplace).

---

## Acknowledgments

Special thanks to:

- The **Vosk** project for providing offline speech recognition.
- **Python** community for excellent libraries and frameworks.
- All contributors and early testers providing valuable feedback.

---

**Last Updated:** March 31, 2026 | **Repository:** https://github.com/sreesanth-s02/Jarvis-Lite
