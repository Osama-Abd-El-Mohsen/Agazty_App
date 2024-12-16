from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.screenmanager import WipeTransition, ScreenManager
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy import platform
from kivy.core.window import Window

if platform != "android":
    Window.size = (406, 762)
    Window.always_on_top = True
Window.clearcolor = [16/255, 19/255, 24/255, 1]

start_time = datetime(2024, 10, 1)
end_time   = datetime(2025, 12, 1)
now_time   = datetime.now()

########### Full Time ###########
full_time = end_time-start_time
print(full_time)

######### Remaining Time ########
Remaining_time = end_time-now_time
print(Remaining_time)

###### Completed Time in % ######
completed_time = full_time - Remaining_time
completed_time_in_per = round(100 - (Remaining_time / full_time * 100),2)
print(completed_time)
print(completed_time_in_per)

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.Android_back_click)

    def get_screen_object_from_screen_name(self, screen_name):
        screen_module_in_str = "_".join([i.lower() for i in screen_name.split()])
        screen_object_in_str = "".join(screen_name.split())
        exec(f"from screens.{screen_module_in_str} import {screen_object_in_str}")
        screen_object = eval(f"{screen_object_in_str}()")
        return screen_object

    def Android_back_click(self,window,key,*largs):
        if key in [27, 1001]:
            self.root.transition = WipeTransition()
            self.root.current = 'Main Screen'
            return True

    def go_main(self):
        self.root.transition = WipeTransition()
        self.root.current = 'Main Screen'

    def build(self):
        self.screen_manager = MyScreenManager()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.set_bars_colors()
        if 'Main Screen' not in self.screen_manager.screen_names:
            self.screen_manager.add_widget(self.get_screen_object_from_screen_name('Main Screen'))
        return self.screen_manager


    def set_bars_colors(self):
        set_bars_colors(
            [16/255, 19/255, 24/255, 1],
            [16/255, 19/255, 24/255, 1],
            "Light" 
        )

if __name__ == "__main__":
    MainApp().run()