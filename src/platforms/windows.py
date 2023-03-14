import win32gui


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
