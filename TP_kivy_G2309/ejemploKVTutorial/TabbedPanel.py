from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle

Builder.load_string("""
<MyTabbedPanel>:
    do_default_tab: False

    TabbedPanelItem:
        text: 'Pestaña 1'
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Botón 1'
            Button:
                text: 'Botón 2'
            Image:
                source: 'UTNLogo.png'
            Image:
                source: 'KV.png'
                        
    TabbedPanelItem:
        text: 'Pestaña 2'
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Botón 3'
            Button:
                text: 'Botón 4'
            Image:
                source: 'UTNLogo.png'
            Image:
                source: 'KV.png'
            
    TabbedPanelItem:
        text: 'Pestaña 3'
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Botón 5'
            Button:
                text: 'Botón 6'
            PageLayout:
                
                BoxLayout:
                    orientation: 'vertical'
                    Image:
                        source: 'UTNLogo.png'
                    Image:
                        source: 'KV.png'
                BoxLayout:
                    orientation: 'vertical'
                    Image:
                        source: 'PyLogo.png'
                    Image:
                        source: 'Ubuntu.png'
                
    TabbedPanelItem:
        text: 'Pestaña 4'
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Botón 7'
                size_hint: .50, .50
            Button:
                text: 'Presione aqui'
                size_hint: .50, .50
                on_release: app.show_popup()
            Image:
                source: 'UTNLogo.png'
            Image:
                source: 'KV.png'
""")

class MyTabbedPanel(TabbedPanel):
    pass



class TabbedPanelApp(App):
    def build(self):
        return MyTabbedPanel()
    
    def show_popup(self):
        popup_layout = BoxLayout(orientation='vertical')
        
        popup_label = Label(text='TP aprobado', color=(1, 1, 1, 1))  # Texto en color blanco
        
        popup_layout.add_widget(popup_label)

        popup = Popup(title='Gracias!', content=Label(text='TP aprobado'), size_hint=(None, None), size=(200, 200))
        popup.open()
        self.set_popup_background_color(popup)

    def set_popup_background_color(self, popup):
        with popup.canvas.before:
            Color(0, 1, 0, 1)  # Color de fondo del Popup (verde)
            Rectangle(pos=popup.pos, size=popup.size)

if __name__ == '__main__':
    TabbedPanelApp().run()
