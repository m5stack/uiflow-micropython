# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from collections import deque
import lvgl as lv
import asyncio
import gc


class AppBase:
    """Base class for all apps"""

    def __init__(self, app_name: str, app_panel: lv.obj):
        self._task = None
        self._app_name = app_name
        self._app_panel = app_panel

    async def main(self):
        """Override this to implement app logic"""
        raise NotImplementedError("App must implement main()")

    def on_cleanup(self):
        """Override this to clean up"""
        pass

    def get_app_name(self) -> str:
        return self._app_name

    def get_app_panel(self) -> lv.obj:
        return self._app_panel

    async def on_open(self):
        # print(self._app_name, "on open")
        self._task = asyncio.create_task(self.main())

    async def on_close(self):
        # print(self._app_name, "on close")
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        self.on_cleanup()


class AppManager:
    """Single App Manager"""

    _event_queue = deque([], 1)
    _installed_apps = {}
    _current_app = None
    _current_app_name = None
    _app_panel = None

    @staticmethod
    def set_app_panel(app_panel: lv.obj):
        AppManager._app_panel = app_panel

    @staticmethod
    def install_app(app_name: str, app_class):
        AppManager._installed_apps[app_name] = app_class

    @staticmethod
    def uninstall_app(app_name: str):
        if app_name == AppManager._current_app_name:
            AppManager._event_queue.append({"close_app": app_name})
        AppManager._installed_apps.pop(app_name, None)

    @staticmethod
    def open_app(app_name: str):
        if app_name == AppManager._current_app_name:
            return
        AppManager._event_queue.append({"open_app": app_name})

    @staticmethod
    def close_app(app_name: str):
        AppManager._event_queue.append({"close_app": AppManager._current_app_name})

    @staticmethod
    async def update():
        # Consume events
        while AppManager._event_queue:
            event = AppManager._event_queue.popleft()
            # Handle open app
            if "open_app" in event:
                app_name = event["open_app"]
                # Check installed list
                if app_name in AppManager._installed_apps:
                    # Close current app
                    if AppManager._current_app:
                        await AppManager._current_app.on_close()
                        AppManager._cleanup()
                    # Create new app
                    AppManager._current_app = AppManager._installed_apps[app_name](
                        app_name, AppManager._app_panel
                    )
                    await AppManager._current_app.on_open()
                    # Update current app name
                    AppManager._current_app_name = app_name
                else:
                    print("open app failed: app not found:", app_name)
            # Handle close app
            elif "close_app" in event:
                if AppManager._current_app:
                    await AppManager._current_app.on_close()
                    AppManager._current_app = None
                    AppManager._current_app_name = None
                    AppManager._cleanup()

    @staticmethod
    def _cleanup():
        # Clean up children widgets
        if AppManager._app_panel:
            AppManager._app_panel.clean()
        gc.collect()
