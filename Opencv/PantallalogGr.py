from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        login_button = Button(text="Login")
        login_button.bind(on_press=self.go_to_index)
        self.add_widget(login_button)

    def go_to_index(self, instance):
        self.manager.current = "main"