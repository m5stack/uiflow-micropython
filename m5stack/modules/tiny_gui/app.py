import M5

try:
    from unit import KeyCode
except ImportError:

    class KeyCode:
        KEYCODE_UNKNOWN = 0x00
        KEYCODE_BACKSPACE = 0x08
        KEYCODE_TAB = 0x09
        KEYCODE_ENTER = 0x0D
        KEYCODE_ESC = 0x1B
        KEYCODE_SPACE = 0x20
        KEYCODE_DEL = 0x7F

        KEYCODE_LEFT = 180
        KEYCODE_UP = 181
        KEYCODE_DOWN = 182
        KEYCODE_RIGHT = 183


class KeyEvent:
    key = 0
    status = False


DEBUG = False


class AppBase:
    def __init__(self, icos: dict, data=None) -> None:
        self.id = 0
        self.icos = icos
        self.descriptor = self.icos.get(False)
        self.x = 0
        self.y = 80
        self.w = 320
        self.h = 160

    def registered(self):
        """
        注册到 AppManage 之后，由 AppManage 调用
        """
        desc = self.icos.get(False)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)

    def mount(self):
        """
        应用加载，由 AppManage 调用
        """
        self._load_view()

    def _load_view(self):
        desc = self.icos.get(True)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)
        M5.Lcd.fillRect(self.x, self.y, self.w, self.h, 0x000000)

    def ready(self):
        pass

    def handle(self, x, y):
        DEBUG and print("Touch X: ", x)
        DEBUG and print("Touch Y: ", y)

    def handle_input(self, event: KeyEvent):
        DEBUG and print("keyboard value: %d" % event.key)

    def umount(self) -> None:
        """
        应用退出的方法，由 AppManage 调用
        """
        self._disappear_view()

    def _disappear_view(self):
        desc = self.icos.get(False)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)
        # M5.Lcd.fillRect(self.x, self.y, self.w, self.h, 0x000000)

    def is_select(self, x, y):
        if x < self.x:
            return False
        if x > (self.x + self.w):
            return False
        if y < self.y:
            return False
        if y > (self.y + self.h):
            return False
        return True


def app_id_generator(n):
    for i in range(n):
        yield i


class AppManage:
    def __init__(self, app_num) -> None:
        self._apps = []
        self._last_app = None
        self._id_generator = app_id_generator(app_num)
        self._id = 0
        self.app = self
        self.focus = True

    def register_app(self, app: AppBase):
        self._apps.append(app)
        app.id = next(self._id_generator)

    def select_app(self, id):
        for app in self._apps:
            if id is app.id:
                self._load_app(app)
                break

    def mount(self):
        for app in self._apps:
            app.registered()

    def load_app(self, x, y):
        select_app = None
        for app in self._apps:
            if self._is_select(app, x, y):
                select_app = app
                break

        if select_app is not None:
            # Handle app switching
            if self._last_app is not select_app and self._last_app is not None:
                # destroy old app
                self._last_app.umount()

            if self._last_app is not select_app:
                # load app
                select_app.mount()
                self._last_app = select_app
                self._id = select_app.id
        else:
            # Handle the functionality of the app
            if self._last_app is not None:
                self._last_app.handle(x, y)

    def _load_app(self, new_app: AppBase):
        if new_app is not None:
            # Handle app switching
            if self._last_app is not new_app and self._last_app is not None:
                # destroy old app
                self._last_app.umount()

            if self._last_app is not new_app:
                # load app
                new_app.mount()
                self._last_app = new_app
                self._id = new_app.id

    def handle_input(self, event: KeyEvent):
        # if self.focus == True:
        #     if key == KeyCode.KEYCODE_DOWN or key == KeyCode.KEYCODE_ENTER:
        #         self.focus = False
        # else:
        #     self.app.handle_input(key)

        if self.app == self:
            if event.key in (KeyCode.KEYCODE_DOWN, KeyCode.KEYCODE_ENTER):
                self.app = self._last_app
                event.status = True
            if event.key is KeyCode.KEYCODE_RIGHT:
                id = (self._id + 1) % len(self._apps)
                self.select_app(id)
                event.status = True
            if KeyCode.KEYCODE_LEFT == event.key:
                id = len(self._apps) - 1 if (self._id - 1 < 0) else (self._id - 1)
                self.select_app(id)
                event.status = True
        else:
            self.app.handle_input(event)

        if event.status is False and event.key is KeyCode.KEYCODE_ESC:
            event.status = True
            self.app = self
            self._last_app.umount()
            self._last_app.mount()
            return

    @staticmethod
    def _is_select(app: AppBase, x, y):
        descriptor = app.descriptor
        if x < descriptor.x:
            return False
        if x > (descriptor.x + descriptor.w):
            return False
        if y < descriptor.y:
            return False
        if y > (descriptor.y + descriptor.h):
            return False
        return True
