import json
import re
from chat.local_llm import LocalLLM

class LLMRouter:
    def __init__(self, llm: LocalLLM):
        self.llm = llm

    def route(self, user_input: str) -> dict:
        text = user_input.strip().lower()

        # ---------- Direct rules for obvious commands ----------
        if text in {"hi", "hello", "hey", "how are you", "who are you"}:
            return {"tool": "general_chat", "args": {"text": user_input}}

        hardcoded_questions = {"what is ai", "what is artificial intelligence", "define ai", "who is cm of kerala", "who is the cm of kerala", "kerala cm", "who is pm of india", "who is the prime minister of india", "india pm"}
        if text in hardcoded_questions:
            return {"tool": "general_chat", "args": {"text": user_input}}

        if "open calculator" in text or text == "calculator":
            return {"tool": "open_calculator", "args": {}}

        # create folder commands
        if ("create" in text and "folder" in text) or ("make" in text and "folder" in text):
            # location preference
            target = "jarvis"
            if "desktop" in text:
                target = "desktop"
            elif "documents" in text:
                target = "documents"
            elif "downloads" in text:
                target = "downloads"
            elif "jarvisworkspace" in text or "jarvis workspace" in text or "jarviswork" in text:
                target = "jarvis"

            # parse folder name from phrases like "create folder hello" or "create new folder named hello"
            name_match = re.search(r"(?:create|make)(?: a| new)? folder(?: named| called)?\s+([\w\- ]+?)(?:\s+in\s+(?:desktop|documents|downloads|jarvisworkspace|jarvis workspace))?$", text)
            if not name_match:
                name_match = re.search(r"(?:folder\s+)([\w\- ]+?)(?:\s+in\s+(?:desktop|documents|downloads|jarvisworkspace|jarvis workspace))?$", text)
            folder_name = "NewFolder"
            if name_match:
                folder_name = name_match.group(1).strip()

            folder_name = folder_name.strip().replace("/", "").replace("\\", "")
            if not folder_name:
                folder_name = "NewFolder"

            return {"tool": "create_folder", "args": {"folder_name": folder_name, "location": target}}

        # delete folder
        if "delete" in text and "folder" in text:
            match = re.search(r"delete(?: the)? folder (\w+) in (.+)", text)
            if match:
                name = match.group(1)
                loc = match.group(2).strip().lower()
                if loc in ["jarvis workspace", "jarvisworkspace", "jarvis work"]:
                    loc = "jarvis"
                elif loc == "desktop":
                    loc = "desktop"
                elif loc == "documents":
                    loc = "documents"
                elif loc == "downloads":
                    loc = "downloads"
                return {"tool": "delete_folder", "args": {"name": name, "location": loc}}

        # rename folder
        if "rename" in text and "folder" in text:
            match = re.search(r"rename(?: the)? folder (\w+) to (\w+) in (.+)", text)
            if match:
                old_name = match.group(1)
                new_name = match.group(2)
                loc = match.group(3).strip().lower()
                if loc in ["jarvis workspace", "jarvisworkspace"]:
                    loc = "jarvis"
                elif loc == "desktop":
                    loc = "desktop"
                elif loc == "documents":
                    loc = "documents"
                elif loc == "downloads":
                    loc = "downloads"
                return {"tool": "rename_folder", "args": {"old_name": old_name, "new_name": new_name, "location": loc}}

        # move folder
        if "move" in text and "folder" in text:
            match = re.search(r"move(?: the)? folder (\w+) from (.+) to (.+)", text)
            if match:
                name = match.group(1)
                from_loc = match.group(2).strip().lower()
                to_loc = match.group(3).strip().lower()
                for loc in [from_loc, to_loc]:
                    if loc in ["jarvis workspace", "jarvisworkspace"]:
                        loc = "jarvis"
                    elif loc == "desktop":
                        loc = "desktop"
                    elif loc == "documents":
                        loc = "documents"
                    elif loc == "downloads":
                        loc = "downloads"
                return {"tool": "move_folder", "args": {"name": name, "from_location": from_loc, "to_location": to_loc}}

        # go to browser and search
        if "go to" in text and "and search" in text:
            match = re.search(r"go to (\w+) and search (.+)", text)
            if match:
                browser = match.group(1).lower()
                query = match.group(2).strip()
                if browser == "chrome":
                    return {"tool": "open_chrome_search", "args": {"query": query}}
                elif browser == "edge":
                    return {"tool": "open_edge_search", "args": {"query": query}}
                elif browser == "firefox":
                    return {"tool": "open_firefox_search", "args": {"query": query}}
                elif browser == "opera":
                    return {"tool": "open_opera_search", "args": {"query": query}}
                elif browser == "brave":
                    return {"tool": "open_brave_search", "args": {"query": query}}

        if "open notepad" in text or text == "notepad":
            return {"tool": "open_notepad", "args": {}}

        if "open chrome" in text or text == "chrome":
            return {"tool": "open_chrome", "args": {}}
        if "open edge" in text or text == "edge":
            return {"tool": "open_edge", "args": {}}
        if "open firefox" in text or text == "firefox":
            return {"tool": "open_firefox", "args": {}}
        if "open opera" in text or text == "opera":
            return {"tool": "open_opera", "args": {}}
        if "open brave" in text or text == "brave":
            return {"tool": "open_brave", "args": {}}
        if "open vscode" in text or text == "vscode":
            return {"tool": "open_vscode", "args": {}}
        if "open word" in text or text == "word" or text == "Ms Word" or text == "ms word":
            return {"tool": "open_word", "args": {}}
        if "open excel" in text or text == "excel":
            return {"tool": "open_excel", "args": {}}
        if "open powerpoint" in text or text == "powerpoint":
            return {"tool": "open_powerpoint", "args": {}}
        if "open paint" in text or text == "paint":
            return {"tool": "open_paint", "args": {}}
        if "open cmd" in text or "command prompt" in text:
            return {"tool": "open_cmd", "args": {}}

        if "open file explorer" in text or "open explorer" in text or text == "file explorer":
            return {"tool": "open_file_explorer", "args": {}}

        if "open bluetooth settings" in text or "bluetooth settings" in text:
            return {"tool": "open_bluetooth_settings", "args": {}}

        if "open display settings" in text or "display settings" in text:
            return {"tool": "open_display_settings", "args": {}}

        if "open sound settings" in text or "sound settings" in text:
            return {"tool": "open_sound_settings", "args": {}}

        if "open wifi settings" in text or "wifi settings" in text or "wi-fi settings" in text:
            return {"tool": "open_wifi_settings", "args": {}}

        if "open linkedin" in text:
            return {"tool": "open_linkedin", "args": {}}
        if "open gmail" in text or "compose email" in text or "compose mail" in text or "open email" in text:
            return {"tool": "open_gmail_compose", "args": {}}

        if "open instagram" in text:
            return {"tool": "open_instagram", "args": {}}

        if "youtube" in text or "play" in text and "youtube" in text:
            query = (
                text.replace("play", "")
                .replace("on youtube", "")
                .replace("in","")
                .replace("open","")
                .replace("youtube", "")
                .strip()
            )
            return {"tool": "open_youtube", "args": {"query": query }}

        if "spotify" in text or "open spotify" in text or ("play" in text and "music" in text):
            query = (
                text.replace("play", "")
                .replace("open","")
                .replace("on spotify", "")
                .replace("spotify", "")
                .strip()
            )
            return {"tool": "open_spotify", "args": {"query": query or "music"}}

        if "large files" in text or "big files" in text:
            location = "downloads"
            if "desktop" in text:
                location = "desktop"
            elif "documents" in text:
                location = "documents"
            return {"tool": "scan_large_files", "args": {"location": location, "min_size_mb": 100}}

        if "old files" in text or "unused files" in text:
            location = "downloads"
            if "desktop" in text:
                location = "desktop"
            elif "documents" in text:
                location = "documents"
            return {"tool": "scan_old_files", "args": {"location": location, "older_than_days": 90}}

        if "temp files" in text or "junk files" in text:
            location = "downloads"
            if "desktop" in text:
                location = "desktop"
            elif "documents" in text:
                location = "documents"
            return {"tool": "scan_temp_files", "args": {"location": location}}
        
        if text.startswith("open folder "):
            folder = user_input[len("open folder "):].strip()
            return {"tool": "open_folder", "args": {"path": folder}}

        if text in {"open documents", "open document folder", "open documents folder"}:
            return {"tool": "open_folder", "args": {"path": "documents"}}

        if text in {"open desktop", "open desktop folder"}:
            return {"tool": "open_folder", "args": {"path": "desktop"}}

        if text in {"open downloads", "open downloads folder"}:
            return {"tool": "open_folder", "args": {"path": "downloads"}}

        if text in {"open jarvis folder", "open jarvis", "open workspace"}:
            return {"tool": "open_folder", "args": {"path": "jarvis"}}

        if "weather" in text:
            if "weather in" in text:
                city = text.split("weather in")[-1].strip()
                query = f"weather in {city}"
            else:
                query = "weather today"
            return {"tool": "open_search", "args": {"query": query}}

        if text.startswith("browse ") or text.startswith("search "):
            query = text.replace("browse", "").replace("search", "").strip()
            return {"tool": "open_search", "args": {"query": query}}

        # fallback to general chat
        return {"tool": "general_chat", "args": {"text": user_input}}