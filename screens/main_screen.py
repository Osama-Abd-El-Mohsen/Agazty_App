from kivy.factory import Factory as F
from utils import load_kv_path

load_kv_path("screens/main_screen.kv")

class MainScreen(F.Screen):
    def on_enter(self):
        if 'Settings Screen' not in self.parent.screen_names:
                self.parent.add_widget(self.get_screen_object_from_screen_name('Settings Screen'))

    def get_screen_object_from_screen_name(self, screen_name):
        screen_module_in_str = "_".join([i.lower() for i in screen_name.split()])
        screen_object_in_str = "".join(screen_name.split())
        exec(f"from screens.{screen_module_in_str} import {screen_object_in_str}")
        screen_object = eval(f"{screen_object_in_str}()")
        return screen_object