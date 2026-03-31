import os
import subprocess
from utils.config import SAFE_DIRECTORIES
from utils.security import resolve_alias_path, is_path_allowed, normalize_path

class SystemControl:
    def open_file_explorer(self) -> str:
        os.startfile(os.path.expanduser("~"))
        return "Opened File Explorer."

    def open_folder(self, path: str) -> str:
        resolved = resolve_alias_path(path)

        if not is_path_allowed(resolved):
            return "Access denied. Folder is outside allowed directories."

        folder = normalize_path(resolved)

        if not folder.exists() or not folder.is_dir():
            return "Folder not found."

        os.startfile(str(folder))
        return f"Opened folder: {folder}"

    def create_folder(self, folder_name: str, location: str = "jarvis") -> str:
        if not folder_name.strip():
            return "Please provide a folder name."

        alias = location.strip().lower() if location else "jarvis"
        if alias not in SAFE_DIRECTORIES:
            alias = "jarvis"

        target_dir = resolve_alias_path(alias)
        parent = normalize_path(target_dir)

        if not is_path_allowed(str(parent)):
            return "Access denied. Folder creation location is outside allowed directories."

        if not parent.exists():
            try:
                parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                return f"Unable to create base directory: {e}"

        new_folder = parent / folder_name.strip().replace("/", "").replace("\\", "")

        if new_folder.exists():
            return f"Folder already exists: {new_folder}"

        try:
            new_folder.mkdir(parents=True, exist_ok=False)
            return f"Created folder: {new_folder}"
        except Exception as e:
            return f"Failed to create folder: {e}"

    def delete_folder(self, name: str, location: str = "jarvis") -> str:
        if not name.strip():
            return "Please provide a folder name."

        alias = location.strip().lower()
        if alias not in SAFE_DIRECTORIES:
            alias = "jarvis"

        target_dir = resolve_alias_path(alias)
        parent = normalize_path(target_dir)

        if not is_path_allowed(str(parent)):
            return "Access denied."

        folder_path = parent / name.strip().replace("/", "").replace("\\", "")

        if not folder_path.exists() or not folder_path.is_dir():
            return f"Folder {folder_path} not found."

        try:
            import shutil
            shutil.rmtree(str(folder_path))
            return f"Deleted folder: {folder_path}"
        except Exception as e:
            return f"Failed to delete folder: {e}"

    def rename_folder(self, old_name: str, new_name: str, location: str = "jarvis") -> str:
        if not old_name.strip() or not new_name.strip():
            return "Please provide old and new folder names."

        alias = location.strip().lower()
        if alias not in SAFE_DIRECTORIES:
            alias = "jarvis"

        target_dir = resolve_alias_path(alias)
        parent = normalize_path(target_dir)

        if not is_path_allowed(str(parent)):
            return "Access denied."

        old_path = parent / old_name.strip().replace("/", "").replace("\\", "")
        new_path = parent / new_name.strip().replace("/", "").replace("\\", "")

        if not old_path.exists() or not old_path.is_dir():
            return f"Folder {old_path} not found."

        if new_path.exists():
            return f"Folder {new_path} already exists."

        try:
            old_path.rename(new_path)
            return f"Renamed folder from {old_path} to {new_path}"
        except Exception as e:
            return f"Failed to rename folder: {e}"

    def move_folder(self, name: str, from_location: str, to_location: str) -> str:
        if not name.strip():
            return "Please provide a folder name."

        from_alias = from_location.strip().lower()
        to_alias = to_location.strip().lower()
        if from_alias not in SAFE_DIRECTORIES:
            from_alias = "jarvis"
        if to_alias not in SAFE_DIRECTORIES:
            to_alias = "jarvis"

        from_dir = resolve_alias_path(from_alias)
        to_dir = resolve_alias_path(to_alias)
        from_parent = normalize_path(from_dir)
        to_parent = normalize_path(to_dir)

        if not is_path_allowed(str(from_parent)) or not is_path_allowed(str(to_parent)):
            return "Access denied."

        from_path = from_parent / name.strip().replace("/", "").replace("\\", "")
        to_path = to_parent / name.strip().replace("/", "").replace("\\", "")

        if not from_path.exists() or not from_path.is_dir():
            return f"Folder {from_path} not found."

        if to_path.exists():
            return f"Folder {to_path} already exists in destination."

        try:
            import shutil
            shutil.move(str(from_path), str(to_path))
            return f"Moved folder from {from_path} to {to_path}"
        except Exception as e:
            return f"Failed to move folder: {e}"

    def open_chrome_with_search(self, query: str) -> str:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                subprocess.Popen([path, url])
                return f"Opened Chrome and searched for: {query}"
        return "Chrome not found."

    def open_edge_with_search(self, query: str) -> str:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        subprocess.Popen(["start", "msedge", url], shell=True)
        return f"Opened Edge and searched for: {query}"

    def open_firefox_with_search(self, query: str) -> str:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        subprocess.Popen(["firefox", url])
        return f"Opened Firefox and searched for: {query}"

    def open_opera_with_search(self, query: str) -> str:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        subprocess.Popen(["opera", url])
        return f"Opened Opera and searched for: {query}"

    def open_brave_with_search(self, query: str) -> str:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        subprocess.Popen(["brave", url])
        return f"Opened Brave and searched for: {query}"

    def open_notepad(self) -> str:
        subprocess.Popen(["notepad.exe"])
        return "Opened Notepad."

    def open_calculator(self) -> str:
        subprocess.Popen(["calc.exe"])
        return "Opened Calculator."

    def open_chrome(self) -> str:
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                subprocess.Popen([path])
                return "Opened Chrome."
        return "Chrome not found."