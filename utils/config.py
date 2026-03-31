from pathlib import Path
import os

HOME = Path.home()

SAFE_DIRECTORIES = {
    "desktop": HOME / "Desktop",
    "documents": HOME / "OneDrive" / "Documents",
    "downloads": HOME / "Downloads",
    "jarvis": HOME / "Desktop" / "JarvisWorkspace"
}

# Gemini API Key - Add your API key here or set as environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Set GEMINI_API_KEY environment variable

ALLOWED_TOOLS = {
    "general_chat",
    "open_search",
    "open_youtube",
    "open_spotify",
    "open_linkedin",
    "open_instagram",
    "open_gmail_compose",
    "scan_large_files",
    "scan_old_files",
    "scan_temp_files",
    "open_bluetooth_settings",
    "open_display_settings",
    "open_sound_settings",
    "open_wifi_settings",
    "open_file_explorer",
    "open_folder",
    "open_notepad",
    "open_calculator",
    "open_chrome",
    "create_folder",
    "delete_folder",
    "rename_folder",
    "move_folder",
    "open_chrome_search",
    "open_edge",
    "open_firefox",
    "open_opera",
    "open_brave",
    "open_vscode",
    "open_word",
    "open_excel",
    "open_powerpoint",
    "open_paint",
    "open_cmd"
}

DANGEROUS_TOOLS = set()
ADMIN_PIN = "1234"
LOG_FILE = os.path.join("logs", "jarvis.log")