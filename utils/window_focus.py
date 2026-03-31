import subprocess
import time
import psutil
import ctypes

import win32gui
import win32con
import win32process
import win32com.client


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def _force_foreground(hwnd):
    try:
        if not hwnd or not win32gui.IsWindow(hwnd):
            return False

        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')

        # Restore if minimized
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.1)

        # Try normal foreground first
        try:
            win32gui.SetForegroundWindow(hwnd)
            win32gui.BringWindowToTop(hwnd)
            win32gui.SetActiveWindow(hwnd)
            time.sleep(0.1)
            if win32gui.GetForegroundWindow() == hwnd:
                return True
        except Exception:
            pass

        # Force using thread input attach
        foreground_hwnd = user32.GetForegroundWindow()
        current_thread_id = kernel32.GetCurrentThreadId()
        target_thread_id = user32.GetWindowThreadProcessId(hwnd, None)
        foreground_thread_id = user32.GetWindowThreadProcessId(foreground_hwnd, None)

        user32.AttachThreadInput(foreground_thread_id, current_thread_id, True)
        user32.AttachThreadInput(target_thread_id, current_thread_id, True)

        win32gui.BringWindowToTop(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetFocus(hwnd)
        win32gui.SetActiveWindow(hwnd)

        user32.AttachThreadInput(foreground_thread_id, current_thread_id, False)
        user32.AttachThreadInput(target_thread_id, current_thread_id, False)

        time.sleep(0.2)
        return win32gui.GetForegroundWindow() == hwnd

    except Exception:
        return False


def _find_main_window_by_pid(pid, timeout=8):
    end_time = time.time() + timeout

    while time.time() < end_time:
        found = []

        def enum_handler(hwnd, _):
            try:
                if not win32gui.IsWindowVisible(hwnd):
                    return
                if win32gui.GetWindow(hwnd, win32con.GW_OWNER) != 0:
                    return

                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                title = win32gui.GetWindowText(hwnd).strip()

                if window_pid == pid and title:
                    found.append(hwnd)
            except Exception:
                pass

        win32gui.EnumWindows(enum_handler, None)

        if found:
            return found[0]

        time.sleep(0.2)

    return None


def _find_window_by_process_names(process_names, timeout=3):
    process_names = {name.lower() for name in process_names}
    end_time = time.time() + timeout

    while time.time() < end_time:
        pids = []
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                name = (proc.info["name"] or "").lower()
                if name in process_names:
                    pids.append(proc.info["pid"])
            except Exception:
                pass

        for pid in pids:
            hwnd = _find_main_window_by_pid(pid, timeout=1)
            if hwnd:
                return hwnd

        time.sleep(0.2)

    return None


def focus_existing_process(process_names, timeout=3):
    try:
        hwnd = _find_window_by_process_names(process_names, timeout=timeout)
        if hwnd:
            return _force_foreground(hwnd)
        return False
    except Exception:
        return False


def launch_and_focus(
    command,
    success_message="Opening application",
    process_names=None,
    launch_delay=1.0,
    focus_timeout=8,
):
    try:
        subprocess.Popen(command, shell=True)
        time.sleep(launch_delay)

        hwnd = None

        if process_names:
            hwnd = _find_window_by_process_names(process_names, timeout=focus_timeout)

        if hwnd:
            _force_foreground(hwnd)
        elif process_names:
            # Some apps create the main window a little later; retry one more time.
            focus_existing_process(process_names, timeout=2)

        return success_message

    except Exception as e:
        return f"Error: {e}"