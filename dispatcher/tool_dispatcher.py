from utils.config import ALLOWED_TOOLS
from chat.general_chat import GeneralChat
from storage_manager.cleanup_manager import CleanupManager
from social_actions.web_actions import WebActions
from settings_control.windows_settings import WindowsSettings
from commands.system_control import SystemControl
from commands.app_launcher import open_desktop_app, open_web, open_settings
import json


class ToolDispatcher:
    def __init__(self):
        self.general_chat = GeneralChat()
        self.cleanup = CleanupManager()
        self.web = WebActions()
        self.settings = WindowsSettings()
        self.system = SystemControl()

    def dispatch(self, tool_data: dict) -> str:
        tool = tool_data.get("tool", "")
        args = tool_data.get("args", {})

        if tool not in ALLOWED_TOOLS:
            return "Blocked. That action is not allowed."

        if tool == "general_chat":
            return self.general_chat.reply(args.get("text", ""))

        if tool == "scan_large_files":
            return self.cleanup.scan_large_files(
                location=args.get("location", "downloads"),
                min_size_mb=int(args.get("min_size_mb", 100))
            )

        if tool == "scan_old_files":
            return self.cleanup.scan_old_files(
                location=args.get("location", "downloads"),
                older_than_days=int(args.get("older_than_days", 90))
            )

        if tool == "scan_temp_files":
            return self.cleanup.scan_temp_files(
                location=args.get("location", "downloads")
            )

        # Web actions
        if tool == "open_youtube":
            query = args.get("query", "").strip()
            if query:
                return open_web(
                    f"https://www.youtube.com/results?search_query={query}",
                    "Opening YouTube"
                )
            return open_web("https://www.youtube.com", "Opening YouTube")

        if tool == "open_spotify":
            query = args.get("query", "").strip()
            if query:
                return open_web(
                    f"https://open.spotify.com/search/{query}",
                    "Opening Spotify"
                )
            return open_web("https://open.spotify.com", "Opening Spotify")

        if tool == "open_linkedin":
            return open_web("https://www.linkedin.com", "Opening LinkedIn")

        if tool == "open_instagram":
            return open_web("https://www.instagram.com", "Opening Instagram")

        if tool == "open_gmail_compose":
            return self.web.open_gmail_compose(
                to=args.get("to", ""),
                subject=args.get("subject", ""),
                body=args.get("body", "")
            )

        if tool == "open_search":
            return self.web.open_search(args.get("query", ""))

        # Windows settings
        if tool == "open_bluetooth_settings":
            return self.settings.open_bluetooth_settings()

        if tool == "open_display_settings":
            return self.settings.open_display_settings()

        if tool == "open_sound_settings":
            return self.settings.open_sound_settings()

        if tool == "open_wifi_settings":
            return self.settings.open_wifi_settings()

        # Desktop/system apps
        if tool == "open_file_explorer":
            return open_desktop_app("explorer")

        if tool == "open_folder":
            return self.system.open_folder(args.get("path", ""))

        if tool == "create_folder":
            return self.system.create_folder(
                folder_name=args.get("folder_name", "NewFolder"),
                location=args.get("location", "jarvis")
            )

        if tool == "delete_folder":
            return self.system.delete_folder(
                name=args.get("name", ""),
                location=args.get("location", "jarvis")
            )

        if tool == "rename_folder":
            return self.system.rename_folder(
                old_name=args.get("old_name", ""),
                new_name=args.get("new_name", ""),
                location=args.get("location", "jarvis")
            )

        if tool == "move_folder":
            return self.system.move_folder(
                name=args.get("name", ""),
                from_location=args.get("from_location", "jarvis"),
                to_location=args.get("to_location", "jarvis")
            )

        if tool == "open_chrome_search":
            return self.system.open_chrome_with_search(args.get("query", ""))
        if tool == "open_gmail_compose":
            return self.system.open_gmail_compose(
                to=args.get("to", ""),
                subject=args.get("subject", ""),
                body=args.get("body", "")
            )

        if tool == "open_edge_search":
            return self.system.open_edge_with_search(args.get("query", ""))

        if tool == "open_firefox_search":
            return self.system.open_firefox_with_search(args.get("query", ""))

        if tool == "open_opera_search":
            return self.system.open_opera_with_search(args.get("query", ""))

        if tool == "open_brave_search":
            return self.system.open_brave_with_search(args.get("query", ""))

        if tool == "open_notepad":
            return open_desktop_app("notepad")

        if tool == "open_calculator":
            return open_desktop_app("calculator")

        if tool == "open_chrome":
            return open_desktop_app("chrome")
        if tool == "open_edge":
            return open_desktop_app("edge")
        if tool == "open_firefox":
            return open_desktop_app("firefox")
        if tool == "open_opera":
            return open_desktop_app("opera")
        if tool == "open_brave":
            return open_desktop_app("brave")
        if tool == "open_vscode":
            return open_desktop_app("vscode")
        if tool == "open_word":
            return open_desktop_app("word")
        if tool == "open_excel":
            return open_desktop_app("excel")
        if tool == "open_powerpoint":
            return open_desktop_app("powerpoint")
        if tool == "open_paint":
            return open_desktop_app("paint")
        
        return "I could not handle that action."







        return "I could not handle that action."