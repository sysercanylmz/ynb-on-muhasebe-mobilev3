from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from app.helpers import money
from app.repositories import dashboard_totals, kasa_bakiye_ozeti, list_islemler
from app.screens.base import RefreshableScreen
from app.widgets import (
    ACCENT,
    CARD_BG,
    DANGER,
    MUTED,
    PRIMARY,
    SUCCESS,
    TEXT,
    WHITE,
    RoundedBox,
    card,
    chip,
    label,
    metric_card,
    scroll_container,
    section_title,
)


class DashboardScreen(RefreshableScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll, self.content = scroll_container()
        self.add_widget(self.scroll)

    def on_pre_enter(self, *_args):
        self.reload()

    def reload(self):
        self.content.clear_widgets()
        totals = dashboard_totals()

        hero = RoundedBox(
            orientation="vertical",
            padding=[dp(16), dp(14), dp(16), dp(14)],
            spacing=dp(6),
            size_hint_y=None,
            height=dp(130),
            bg_color=PRIMARY,
            border_color=PRIMARY,
            radius=24,
        )
        hero.add_widget(label("Genel Durum", size=13, color=(0.78, 0.86, 1, 1), height=24))
        hero.add_widget(label(money(totals["kar"]), size=30, bold=True, color=WHITE, height=46))
        hero.add_widget(label("Toplam giriş - toplam çıkış", size=12, color=(0.78, 0.86, 1, 1), height=24))
        self.content.add_widget(hero)

        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        metric_items = [
            ("Toplam Giriş", money(totals["gelir"]), "Gelir + tahsilat", "green"),
            ("Toplam Çıkış", money(totals["gider"]), "Gider + ödeme", "red"),
            ("Kasa/Banka", money(totals["kasa"]), "Güncel bakiye", "blue"),
            ("Belgesiz Çıkış", money(totals["belgesiz"]), "Fişsiz/faturasız", "orange"),
        ]
        for title, value, subtitle, tone in metric_items:
            grid.add_widget(metric_card(title, value, subtitle, tone=tone))
        self.content.add_widget(grid)

        self.content.add_widget(section_title("Kasa / Banka Bakiyeleri"))
        kasa_rows = kasa_bakiye_ozeti()
        if not kasa_rows:
            self.content.add_widget(label("Henüz kasa veya banka eklenmedi.", size=14, color=MUTED, height=36))
        for row in kasa_rows:
            box = card(padding=12, spacing=6)
            top = BoxLayout(size_hint_y=None, height=dp(32), spacing=dp(8))
            top.add_widget(label(f"[b]{row['kasa_adi']}[/b]", size=15, height=32))
            badge = chip(row["kasa_tipi"], tone="dark")
            badge.size_hint_x = None
            badge.width = dp(96)
            top.add_widget(badge)
            box.add_widget(top)
            box.add_widget(label(f"Açılış: {money(row['acilis_bakiyesi'])}", size=12, color=MUTED, height=22))
            box.add_widget(label(f"Güncel: {money(row['bakiye'])}", size=20, bold=True, color=PRIMARY, height=34))
            self.content.add_widget(box)

        self.content.add_widget(section_title("Son İşlemler"))
        rows = list_islemler(limit=8)
        if not rows:
            empty = card(padding=14, spacing=4)
            empty.add_widget(label("Henüz işlem yok.", size=15, bold=True, height=28))
            empty.add_widget(label("İşlem ekranından ilk gelir veya gider kaydını ekleyebilirsin.", size=12, color=MUTED, height=28))
            self.content.add_widget(empty)
        for row in rows:
            tone = "green" if row["islem_tipi"] in ("gelir", "tahsilat") else "red"
            value_color = SUCCESS if tone == "green" else DANGER
            box = card(padding=12, spacing=5)
            top = BoxLayout(size_hint_y=None, height=dp(32), spacing=dp(8))
            top.add_widget(label(f"[b]{row['baslik']}[/b]", size=15, height=32))
            c = chip(row["islem_tipi"], tone=tone)
            c.size_hint_x = None
            c.width = dp(92)
            top.add_widget(c)
            box.add_widget(top)
            box.add_widget(label(f"{row['tarih']} • {row['belge_turu']}", size=12, color=MUTED, height=22))
            box.add_widget(label(money(row["toplam_tutar"]), size=18, bold=True, color=value_color, height=30))
            self.content.add_widget(box)
