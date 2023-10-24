from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.camera import Camera
from kivy.core.window import Window
from kivy.graphics.texture import Texture
import os

class RegistrationApp(App):
    def build(self):
        self.title = "Registro y Cámara"
        self.registered = False

        self.layout = BoxLayout(orientation="vertical")

        # Crear el widget TabbedPanel
        self.tabbed_panel = TabbedPanel(do_default_tab=False)
        self.layout.add_widget(self.tabbed_panel)

        # Pestaña de Registro
        self.tab_register = TabbedPanelHeader(text="Registro")
        self.name_input = TextInput(hint_text="Nombre")
        self.email_input = TextInput(hint_text="Correo Electrónico")
        self.register_button = Button(text="Registrarse")
        self.register_button.bind(on_press=self.register)
        self.tab_register.content = BoxLayout(orientation="vertical")
        self.tab_register.content.add_widget(Label(text="Registro"))
        self.tab_register.content.add_widget(self.name_input)
        self.tab_register.content.add_widget(self.email_input)
        self.tab_register.content.add_widget(self.register_button)
        self.tabbed_panel.add_widget(self.tab_register)

        # Pestaña de Cámara
        self.tab_camera = TabbedPanelHeader(text="Cámara")
        self.camera_button = Button(text="Tomar Foto")
        self.camera_button.bind(on_press=self.take_photo)
        self.tab_camera.content = BoxLayout(orientation="vertical")
        self.tab_camera.content.add_widget(Label(text="Cámara"))
        self.tab_camera.content.add_widget(self.camera_button)
        self.tabbed_panel.add_widget(self.tab_camera)
        
        self.camera = Camera(play=True)
        self.tab_camera.content.add_widget(self.camera)

        return self.layout

    def register(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        # Aquí puedes guardar los datos de registro en una base de datos o hacer lo que desees con ellos
        print(f"Nombre: {name}, Correo Electrónico: {email}")
        self.registered = True
        self.tabbed_panel.switch_to(self.tab_camera)  # Cambiar a la pestaña de la cámara

    def take_photo(self, instance):
        if self.registered:
            image_texture = self.camera.export_as_texture()
            image_bytes = image_texture.pixels
            # Guarda la foto en un archivo (por ejemplo, en la carpeta actual)
            image_filename = "captured_photo.png"
            with open(image_filename, "wb") as f:
                f.write(image_bytes)
            print(f"Foto guardada como {image_filename}")
        else:
            print("Primero debes registrarte antes de tomar una foto.")

if __name__ == "__main__":
    Window.clearcolor = (1, 1, 1, 1)  # Fondo blanco
    RegistrationApp().run()
