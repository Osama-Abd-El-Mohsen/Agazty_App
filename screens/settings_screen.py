from kivy.factory import Factory as F
from utils import load_kv_path
from kivy.clock import Clock
load_kv_path("screens/settings_screen.kv")


class SettingsScreen(F.Screen):
    def on_pre_enter(self, *args):
        pass