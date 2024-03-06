import asyncio


def generator(d):
    try:
        len(d)
    except TypeError:
        cache = []
        for i in d:
            yield i
            cache.append(i)
        d = cache
    while d:
        yield from d


class AppSelector:
    def __init__(self, apps: list) -> None:
        self._apps = apps
        self._id = 0

    def prev(self):
        self._id = (self._id - 1) % len(self._apps)
        return self._apps[self._id]

    def next(self):
        self._id = (self._id + 1) % len(self._apps)
        return self._apps[self._id]

    def current(self):
        return self._apps[self._id]

    def select(self, app):
        self._id = self._apps.index(app)

    def index(self, id):
        self._id = id % len(self._apps)
        return self._apps[self._id]


class AppBase:
    def __init__(self) -> None:
        self._task = None

    def on_install(self):
        pass

    def on_launch(self):
        pass

    def on_view(self):
        pass

    def on_ready(self):
        self._task = asyncio.create_task(self.on_run())

    async def on_run(self):
        while True:
            await asyncio.sleep_ms(500)

    def on_hide(self):
        self._task.cancel()

    def on_exit(self):
        pass

    def on_uninstall(self):
        pass

    def install(self):
        self.on_install()

    def start(self):
        self.on_launch()
        self.on_view()
        self.on_ready()

    def pause(self):
        self.on_hide()

    def resume(self):
        self.on_ready()

    def stop(self):
        self.on_hide()
        self.on_exit()

    def uninstall(self):
        self.on_uninstall()
