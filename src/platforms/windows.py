import win32gui
from psutil import process_iter

class Windows:
    def run_command(self, sim_name: str, host_game: bool) -> list[str]:
        command = ["cmd", "/k", "Dominions5.exe", "--simpgui", "--nosteam"]

        if host_game:
            return command + ["-waxscog", "-T", sim_name]

        return command + ["--res", "960", "720", "-waxscod", sim_name]

    def get_app_window(self) -> tuple[int, int]:
        hwnd = 0
        while hwnd == 0:
            hwnd = win32gui.FindWindow(None, "Dominions 5")

        x, y = win32gui.ClientToScreen(hwnd, (0, 0))

        return x, y

    def kill_process(self, pid: int) -> None:
        for p in process_iter():
            if p.pid == pid:
                p.kill()
            if p.name() == "Dominions5.exe":
                p.kill()
        