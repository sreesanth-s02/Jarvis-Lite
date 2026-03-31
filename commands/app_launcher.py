import os
import webbrowser
from utils.window_focus import launch_and_focus, focus_existing_process


APP_MAP = {
    "notepad": {
        "processes": ["notepad.exe"],
        "command": "notepad.exe",
        "message": "Opening Notepad"
    },
    "calculator": {
        "processes": ["calculatorapp.exe", "calc.exe"],
        "command": "calc.exe",
        "message": "Opening Calculator"
    },
    "chrome": {
        "processes": ["chrome.exe"],
        "command": "start chrome",
        "message": "Opening Chrome"
    },
    "explorer": {
        "processes": ["explorer.exe"],
        "command": "explorer",
        "message": "Opening File Explorer"
    },
    "paint": {
        "processes": ["mspaint.exe"],
        "command": "mspaint.exe",
        "message": "Opening Paint"
    },
    "cmd": {
        "processes": ["cmd.exe"],
        "command": "start cmd",
        "message": "Opening Command Prompt"
    },
    "edge": {
        "processes": ["msedge.exe"],
        "command": "start msedge",
        "message": "Opening Edge"
    },
    "brave": {
        "processes": ["brave.exe"],
        "command": "start brave",
        "message": "Opening Brave"
    },
    "firefox": {
        "processes": ["firefox.exe"],
        "command": "start firefox",
        "message": "Opening Firefox"
    },
    "opera": {
        "processes": ["opera.exe"],
        "command": "start opera",
        "message": "Opening Opera"
    },
    "excel": {
        "processes": ["excel.exe"],
        "command": "start excel",
        "message": "Opening Excel"
    },
    "word": {
        "processes": ["winword.exe"],
        "command": "start winword",
        "message": "Opening Word"
    },
    "powerpoint": {
        "processes": ["powerpnt.exe"],
        "command": "start powerpnt",
        "message": "Opening PowerPoint"
    },
    "vscode": {
        "processes": ["Code.exe"],
        "command": "start code",
        "message": "Opening VSCode"
    },
    "gmail": {
        "processes": ["chrome.exe", "msedge.exe", "firefox.exe", "opera.exe"],
        "command": "start chrome",
        "message": "Opening Gmail"
    },  
}


def open_desktop_app(app_key):
    app = APP_MAP.get(app_key)
    if not app:
        return f"Unknown app: {app_key}"

    if focus_existing_process(app["processes"], timeout=4):
        return f"Bringing {app_key.title()} to front"

    return launch_and_focus(
        app["command"],
        app["message"],
        process_names=app["processes"],
        launch_delay=0.8,
        focus_timeout=12,
    )


def open_web(url, message="Opening website"):
    try:
        webbrowser.open(url)
        return message
    except Exception as e:
        return f"Error: {e}"


def open_settings():
    try:
        os.system("start ms-settings:")
        return "Opening Settings"
    except Exception as e:
        return f"Error: {e}"