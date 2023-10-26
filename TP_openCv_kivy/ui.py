from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class UI(BoxLayout):
    def __init__(self, app, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.app = app

        # Crear el widget TabbedPanel
        self.tabbed_panel = TabbedPanel(do_default_tab=False)
        self.add_widget(self.tabbed_panel)

        # Pestaña de Registro
        self.tab_register = TabbedPanelHeader(text="Registro")
        self.register_content = BoxLayout(orientation="vertical")
        self.name_input = TextInput(hint_text="Nombre")
        self.register_button = Button(text="Registrarse")
        self.register_button.bind(on_press=self.app.register)
        self.register_content.add_widget(Label(text="Registro"))
        self.register_content.add_widget(self.name_input)
        self.register_content.add_widget(self.register_button)
        self.tab_register.content = self.register_content
        self.camera = Camera(play=True)
        self.register_content.add_widget(self.camera)
        self.tabbed_panel.add_widget(self.tab_register)

        # Agregar una nueva pestaña para mostrar fotos y videos guardados
        self.tab_gallery = TabbedPanelHeader(text="Galería")
        self.gallery_content = BoxLayout(orientation="vertical")
        self.gallery_images = GridLayout(cols=3)
        self.gallery_content.add_widget(Label(text="Fotos y Videos Guardados"))
        self.gallery_content.add_widget(ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100), do_scroll_x=False))
        self.gallery_content.children[1].add_widget(self.gallery_images)
        self.tab_gallery.content = self.gallery_content
        self.tabbed_panel.add_widget(self.tab_gallery)
