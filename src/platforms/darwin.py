import Quartz


class Darwin:
    def run_command(self, sim_name: str, host_game: bool) -> list[str]:
        command = ["./dom5_mac", "--simpgui", "--nosteam"]

        if host_game:
            return command + ["-waxscog", "-T", sim_name]

        return command + ["--res", "960", "720", "-waxscod", sim_name]

    def get_app_window(self) -> tuple[int, int]:
        apps = Quartz.CGWindowListCopyWindowInfo(  # type: ignore
            Quartz.kCGWindowListOptionOnScreenOnly  # type: ignore
            & Quartz.kCGWindowListExcludeDesktopElements,  # type: ignore
            Quartz.kCGNullWindowID,  # type: ignore
        )

        dom_5_apps = (a for a in apps if a.get("kCGWindowOwnerName") == "dom5_mac")
        dom_5 = next(a for a in dom_5_apps if a.get("kCGWindowIsOnscreen") == 1)
        window = dom_5.get("kCGWindowBounds")

        return window["X"], window["Y"]
