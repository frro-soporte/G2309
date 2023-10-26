from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.filechooser import FileChooserListView

class MediaExplorerApp(App):
    def build(self):
        # Interfaz de usuario
        layout = BoxLayout(orientation='vertical')
        
        # FileChooser para seleccionar archivos de medios
        file_chooser = FileChooserListView(path='.', filters=['*.jpg', '*.png', '*.mp4'])
        
        # Widget para mostrar imágenes y videos
        media_widget = BoxLayout(orientation='horizontal')
        media = None  # Widget de medios (imagen o video)

        def load_media(instance, value):
            nonlocal media
            selected = value  # Accede a la selección de archivos desde el evento
            if selected:
                selected_file = selected[0]

                # Verifica si el archivo seleccionado es una imagen o un video
                if selected_file.lower().endswith(('.jpg', '.png')):
                    # Si es una imagen, muestra la imagen
                    if media is not None:
                        media_widget.remove_widget(media)
                    media = Image(source=selected_file)
                elif selected_file.lower().endswith('.mp4'):
                    # Si es un video, muestra el video
                    if media is not None:
                        media_widget.remove_widget(media)
                    media = VideoPlayer(source=selected_file, state='play')

                media_widget.add_widget(media)

        file_chooser.bind(selection=load_media)

        layout.add_widget(file_chooser)
        layout.add_widget(media_widget)

        return layout

if __name__ == '__main__':
    MediaExplorerApp().run()
