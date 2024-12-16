from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.screenmanager import WipeTransition, ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.storage.jsonstore import JsonStore
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy import platform
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock

if platform != "android":
    Window.size = (406, 762)
    Window.always_on_top = True
Window.clearcolor = [16/255, 19/255, 24/255, 1]

start_time = datetime(2024, 10, 1)
end_time   = datetime(2025, 12, 1)
now_time   = datetime.now()


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

class MainApp(MDApp):
    ########### Full Time ###########
    full_time = end_time-start_time

    ######### Remaining Time ########
    Remaining_time = end_time-now_time

    ###### Completed Time in % ######
    completed_time = full_time - Remaining_time
    completed_time_in_per = round(100 - (Remaining_time / full_time * 100),2)
    
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

    def go_setting_page(self):
        self.root.transition = WipeTransition()
        self.root.current = 'Settings Screen'

    def dofaa_menu(self,item):
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in ['10','1','4']
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()

    def menu_callback(self, text_item):
        global dofaa_month
        self.screen_manager.get_screen('Settings Screen').ids['drop_text'] = text_item
        dofaa_month = text_item
        self.save_to_JSON()

    def load_from_JSON(self):
        global dofaa_month
        dofaa_month = self.stored_data.get('dofaa')['month']
        print("="*10+"\n"+"From Main Load")
        print(dofaa_month)
        print("="*10)
    
    
    def save_to_JSON(self):
        self.stored_data.put('dofaa', month=dofaa_month)

    def build(self):
        self.stored_data = JsonStore('data.json')
        self.load_from_JSON()
        self.screen_manager = MyScreenManager()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.set_bars_colors()
        if 'Main Screen' not in self.screen_manager.screen_names:
            self.screen_manager.add_widget(self.get_screen_object_from_screen_name('Main Screen'))
        
        screen = self.screen_manager.get_screen('Main Screen').ids['progbar']
        self.screen_manager.get_screen('Main Screen').ids['completed_percentage'].text = str(self.completed_time_in_per)+' %'
        self.screen_manager.get_screen('Main Screen').ids['days_remaining'].text = str(self.Remaining_time.days) + ' days remaining'
        self.screen_manager.get_screen('Main Screen').ids['days_completed'].text = str(self.completed_time.days) + ' days completed'
        screen = self.screen_manager.get_screen('Main Screen').ids['progbar']
        screen.progress = self.completed_time_in_per
        
        return self.screen_manager


    def set_bars_colors(self):
        set_bars_colors(
            [16/255, 19/255, 24/255, 1],
            [16/255, 19/255, 24/255, 1],
            "Light" 
        )

if __name__ == "__main__":
    LabelBase.register(name="BBCairo", fn_regular="font/cairo/Cairo-Black.ttf")
    LabelBase.register(name="SBCairo", fn_regular="font/cairo/Cairo-SemiBold.ttf")
    LabelBase.register(name="MCairo", fn_regular="font/cairo/Cairo-Medium.ttf")
    LabelBase.register(name="RCairo", fn_regular="font/cairo/Cairo-Regular.ttf")
    LabelBase.register(name="BPoppins", fn_regular="font/Poppins/Poppins-Bold.ttf")
    LabelBase.register(name="MPoppins", fn_regular="font/Poppins/Poppins-Medium.ttf")

    MainApp().run()