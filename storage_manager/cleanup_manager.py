from pathlib import Path
from datetime import datetime, timedelta
from utils.security import resolve_alias_path, is_path_allowed, normalize_path
import shutil
import os

class CleanupManager:
    def create_file(self, path: str) -> str:
        if not is_path_allowed(path):
            return "Access denied. Path is outside allowed directories."

        p = normalize_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)

        with open(p, "w", encoding="utf-8") as f:
            f.write("Jarvis created this file.")

        return f"File created: {p}"

    def delete_file(self, path: str) -> str:
        if not is_path_allowed(path):
            return "Access denied. Path is outside allowed directories."

        p = normalize_path(path)
        if p.exists() and p.is_file():
            send2trash(str(p))
            return f"File moved to Recycle Bin: {p}"
        return "File not found."

    def create_folder(self, path: str) -> str:
        if not is_path_allowed(path):
            return "Access denied. Path is outside allowed directories."

        p = normalize_path(path)
        p.mkdir(parents=True, exist_ok=True)
        return f"Folder created: {p}"

    def delete_folder(self, path: str) -> str:
        if not is_path_allowed(path):
            return "Access denied. Path is outside allowed directories."

        p = normalize_path(path)
        if p.exists() and p.is_dir():
            send2trash(str(p))
            return f"Folder moved to Recycle Bin: {p}"
        return "Folder not found."

    def rename_item(self, old_path: str, new_path: str) -> str:
        if not is_path_allowed(old_path) or not is_path_allowed(new_path):
            return "Access denied. Source or destination is outside allowed directories."

        old = normalize_path(old_path)
        new = normalize_path(new_path)

        if old.exists():
            old.rename(new)
            return f"Renamed to: {new}"
        return "Item not found."

    def move_item(self, source: str, destination: str) -> str:
        if not is_path_allowed(source) or not is_path_allowed(destination):
            return "Access denied. Source or destination is outside allowed directories."

        src = normalize_path(source)
        dst = normalize_path(destination)

        if src.exists():
            shutil.move(str(src), str(dst))
            return f"Moved {src} to {dst}"
        return "Source item not found."

    def list_files(self, path: str) -> str:
        if not is_path_allowed(path):
            return "Access denied. Path is outside allowed directories."

        p = normalize_path(path)
        if p.exists() and p.is_dir():
            items = [item.name for item in p.iterdir()]
            return ", ".join(items) if items else "Folder is empty."
        return "Folder not found."

    def scan_large_files(self, location: str = "downloads", min_size_mb: int = 100) -> str:
        """Find files larger than min_size_mb in the specified location."""
        try:
            target_path = Path(resolve_alias_path(location))
            
            if not target_path.exists():
                return f"Location '{location}' not found."
            
            if not is_path_allowed(str(target_path)):
                return "Access denied. Path is outside allowed directories."
            
            large_files = []
            min_size_bytes = min_size_mb * 1024 * 1024
            
            for root, dirs, files in os.walk(target_path):
                for file in files:
                    file_path = Path(root) / file
                    try:
                        file_size = file_path.stat().st_size
                        if file_size >= min_size_bytes:
                            size_mb = file_size / (1024 * 1024)
                            large_files.append((file_path.name, size_mb, str(file_path)))
                    except (OSError, PermissionError):
                        continue
            
            if not large_files:
                return f"No files larger than {min_size_mb}MB found in {location}."
            
            # Sort by size descending
            large_files.sort(key=lambda x: x[1], reverse=True)
            
            result = f"Found {len(large_files)} large files (>{min_size_mb}MB) in {location}:\n"
            for name, size, full_path in large_files[:20]:  # Show top 20
                result += f"\n• {name} ({size:.2f}MB)\n  Path: {full_path}"
            
            if len(large_files) > 20:
                result += f"\n\n... and {len(large_files) - 20} more files"
            
            return result
        
        except Exception as e:
            return f"Error scanning for large files: {str(e)}"

    def scan_old_files(self, location: str = "downloads", older_than_days: int = 90) -> str:
        """Find files older than older_than_days in the specified location."""
        try:
            target_path = Path(resolve_alias_path(location))
            
            if not target_path.exists():
                return f"Location '{location}' not found."
            
            if not is_path_allowed(str(target_path)):
                return "Access denied. Path is outside allowed directories."
            
            old_files = []
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            
            for root, dirs, files in os.walk(target_path):
                for file in files:
                    file_path = Path(root) / file
                    try:
                        file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if file_mtime < cutoff_date:
                            days_old = (datetime.now() - file_mtime).days
                            old_files.append((file_path.name, days_old, str(file_path)))
                    except (OSError, PermissionError):
                        continue
            
            if not old_files:
                return f"No files older than {older_than_days} days found in {location}."
            
            # Sort by age descending
            old_files.sort(key=lambda x: x[1], reverse=True)
            
            result = f"Found {len(old_files)} files older than {older_than_days} days in {location}:\n"
            for name, days, full_path in old_files[:20]:  # Show top 20
                result += f"\n• {name} ({days} days old)\n  Path: {full_path}"
            
            if len(old_files) > 20:
                result += f"\n\n... and {len(old_files) - 20} more files"
            
            return result
        
        except Exception as e:
            return f"Error scanning for old files: {str(e)}"

    def scan_temp_files(self, location: str = "downloads") -> str:
        """Find temporary/junk files in the specified location."""
        try:
            target_path = Path(resolve_alias_path(location))
            
            if not target_path.exists():
                return f"Location '{location}' not found."
            
            if not is_path_allowed(str(target_path)):
                return "Access denied. Path is outside allowed directories."
            
            temp_extensions = {
                '.tmp', '.temp', '.bak', '.backup', '.cache', 
                '.log', '.swp', '.swo', '~', '.thumbs',
                '.dmp', '.dump', '.crdownload', '.partial'
            }
            
            temp_files = []
            
            for root, dirs, files in os.walk(target_path):
                for file in files:
                    file_path = Path(root) / file
                    file_lower = file.lower()
                    
                    # Check if file has temp extension or starts with ~
                    is_temp = any(file_lower.endswith(ext) for ext in temp_extensions)
                    is_temp = is_temp or file_lower.startswith('~')
                    
                    if is_temp:
                        try:
                            file_size = file_path.stat().st_size
                            size_mb = file_size / (1024 * 1024)
                            temp_files.append((file_path.name, size_mb, str(file_path)))
                        except (OSError, PermissionError):
                            continue
            
            if not temp_files:
                return f"No temporary/junk files found in {location}."
            
            # Sort by size descending
            temp_files.sort(key=lambda x: x[1], reverse=True)
            
            total_size = sum(f[1] for f in temp_files)
            result = f"Found {len(temp_files)} temporary/junk files in {location} ({total_size:.2f}MB total):\n"
            for name, size, full_path in temp_files[:20]:  # Show top 20
                result += f"\n• {name} ({size:.2f}MB)\n  Path: {full_path}"
            
            if len(temp_files) > 20:
                result += f"\n\n... and {len(temp_files) - 20} more files"
            
            return result
        
        except Exception as e:
            return f"Error scanning for temp files: {str(e)}"