from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivy.uix.scrollview import ScrollView

from app import config
from app.database import init_db
from app.screens.cariler_screen import CarilerScreen
from app.screens.dashboard_screen import DashboardScreen
from app.screens.islemler_screen import IslemlerScreen
from app.screens.kasalar_screen import KasalarScreen
from app.screens.kategoriler_screen import KategorilerScreen
from app.screens.raporlar_screen import RaporlarScreen
from app.screens.yedek_screen import YedekScreen
from app.widgets import BG, PRIMARY, PRIMARY_LIGHT, WHITE, ACCENT, RoundedBox, btn, label


class AppScreenManager(ScreenManager):
    def app_refresh_all(self):
        for screen in self.screens:
            if hasattr(screen, "reload"):
                try:
                    screen.reload()
                except Exception:
                    pass


class YNBOnMuhasebeMobileApp(App):
    title = config.APP_NAME
    icon = str(config.ICON_PATH)

    def build(self):
        config.set_data_dir(Path(self.user_data_dir))
        init_db()

        Window.clearcolor = BG
        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(self._header())

        self.manager = AppScreenManager(transition=NoTransition())
        self.manager.add_widget(DashboardScreen(name="dashboard"))
        self.manager.add_widget(IslemlerScreen(name="islemler"))
        self.manager.add_widget(CarilerScreen(name="cariler"))
        self.manager.add_widget(KasalarScreen(name="kasalar"))
        self.manager.add_widget(KategorilerScreen(name="kategoriler"))
        self.manager.add_widget(RaporlarScreen(name="raporlar"))
        self.manager.add_widget(YedekScreen(name="yedek"))
        root.add_widget(self.manager)
        root.add_widget(self._nav())
        return root

    def _header(self):
        outer = BoxLayout(size_hint_y=None, height=dp(86), padding=[dp(12), dp(10), dp(12), dp(8)])
        box = RoundedBox(
            orientation="horizontal",
            padding=[dp(12), dp(8), dp(12), dp(8)],
            spacing=dp(10),
            bg_color=PRIMARY,
            border_color=PRIMARY,
            radius=22,
        )
        if config.LOGO_PATH.exists():
            box.add_widget(Image(source=str(config.LOGO_PATH), size_hint_x=None, width=dp(52), allow_stretch=True))
        title_box = BoxLayout(orientation="vertical", spacing=dp(1))
        title_box.add_widget(label("YNB Ön Muhasebe", size=18, bold=True, color=WHITE, height=30))
        title_box.add_widget(label("Gelir • Gider • Cari • Kasa Takibi", size=12, color=(0.80, 0.87, 1, 1), height=24))
        box.add_widget(title_box)
        outer.add_widget(box)
        return outer

    def _nav(self):
        outer = BoxLayout(size_hint_y=None, height=dp(72), padding=[dp(8), dp(8), dp(8), dp(8)])
        shell = RoundedBox(orientation="vertical", bg_color=WHITE, border_color=(0.86, 0.89, 0.94, 1), radius=24, padding=[dp(8), dp(6), dp(8), dp(6)])
        scroll = ScrollView(do_scroll_x=True, do_scroll_y=False)
        row = BoxLayout(orientation="horizontal", spacing=dp(7), size_hint_x=None)
        row.bind(minimum_width=row.setter("width"))
        items = [
            ("Ana", "dashboard"),
            ("İşlem", "islemler"),
            ("Cari", "cariler"),
            ("Kasa", "kasalar"),
            ("Kategori", "kategoriler"),
            ("Rapor", "raporlar"),
            ("Yedek", "yedek"),
        ]
        for text, screen in items:
            b = btn(text, lambda _b, s=screen: self.go(s), bg=PRIMARY_LIGHT, fg=WHITE, height=44)
            b.size_hint_x = None
            b.width = dp(94)
            row.add_widget(b)
        scroll.add_widget(row)
        shell.add_widget(scroll)
        outer.add_widget(shell)
        return outer

    def go(self, screen_name):
        self.manager.current = screen_name


if __name__ == "__main__":
    YNBOnMuhasebeMobileApp().run()
