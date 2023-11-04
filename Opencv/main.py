from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Para el file chooser
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.filechooser import FileChooserListView

from deteccionMano import CameraScreen
from PantallalogGr import LoginScreen
from PantallaLog import LoginScreen2

class IndexScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.title = "INDEX"

            # Fondo de pantalla
            self.background_color = (0.2, 0.6, 1, 1)  # Color de fondo azul claro

            layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
            
            label = Label(
                text="¡Bienvenido a tu Aplicación!",
                size_hint_y=None,
                height=50,
                color=(1, 1, 1, 1)  # Color de texto blanco
            )
            layout.add_widget(label)

            buttonsLayout = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint=(None, None), height=100)

            files_button = Button(
                text="Galería",
                size=(150, 50),
                background_color=(0.1, 0.4, 0.7, 1)  # Color de fondo azul oscuro
            )
            files_button.bind(on_press=self.go_to_files)
            buttonsLayout.add_widget(files_button)

            camera_button = Button(
                text="Cámara",
                size=(150, 50),
                background_color=(0.8, 0.2, 0.2, 1)  # Color de fondo rojo oscuro
            )
            camera_button.bind(on_press=self.go_to_camera)
            buttonsLayout.add_widget(camera_button)

            layout.add_widget(buttonsLayout)

            self.add_widget(layout)
            
    
        def go_to_camera(self, instance):
            # Crear una instancia de la aplicación de la cámara y mostrar la vista de la cámara
            #self.manager.current = "camera"

            # Agregar la instancia de la pantalla de la cámara al ScreenManager
            if "camera" not in self.manager.screen_names:
                self.manager.add_widget(CameraScreen(name="camera"))
            # Cambiar a la pantalla de la cámara
            self.manager.current = "camera"

        def go_to_files(self, instance):
            self.manager.current = "files"

        # Actualiza el titulo
        def on_pre_enter(self):
            App.get_running_app().title = self.title


class FileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Files Screen" 
        layout = BoxLayout(orientation='vertical')

        # Agregar el FileChooserListView a la pantalla de "Files"
        self.file_chooser = FileChooserListView(path='.', filters=['*.jpg', '*.png', '*.mp4'])
        layout.add_widget(self.file_chooser)

        # Widget para mostrar fotos o videos
        self.media_widget = BoxLayout(orientation='vertical')
        layout.add_widget(self.media_widget)

        # Botón para regresar a la pantalla de índice
        files_button = Button(text="<< Back", size_hint=(None, None), size = (100, 50))
        files_button.bind(on_press=self.go_to_index)
        layout.add_widget(files_button)

        self.add_widget(layout)

        # Vincular la selección de archivos en el FileChooser con la función load_media
        self.file_chooser.bind(selection=self.load_media)


    def load_media(self, instance, value):
        self.media_widget.clear_widgets()  # Limpiar cualquier contenido anterior

        selected = value  # Acceder a la selección de archivos desde el evento
        if selected:
            selected_file = selected[0]

            # Verificar si el archivo seleccionado es una imagen o un video
            if selected_file.lower().endswith(('.jpg', '.png')):
                # Si es una imagen, mostrar la imagen en un ImageView
                image_widget = Image(source=selected_file)
                self.media_widget.add_widget(image_widget)
            elif selected_file.lower().endswith('.mp4'):
                # Si es un video, reproducir el video en el MediaPlayer
                video_player = VideoPlayer(source=selected_file, state='play')
                self.media_widget.add_widget(video_player)

    def go_to_index(self, instance):
        self.manager.current = "index"

    # Actualiza el titulo
    def on_pre_enter(self):
        App.get_running_app().title = self.title


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        #sm.add_widget(LoginScreen(name="login")) # Skip the LogIn
        sm.add_widget(LoginScreen2(name="login"))
        sm.add_widget(IndexScreen(name="index"))
        #sm.add_widget(CameraScreen(name="camera"))
        sm.add_widget(FileScreen(name="files"))
        return sm


if __name__ == '__main__':
    MyApp().run()
