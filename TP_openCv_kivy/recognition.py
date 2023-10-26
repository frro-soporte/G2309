import cv2
import time
import sqlite3
import mediapipe as mp
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from io import BytesIO
import io
from kivy.core.image import Image as CoreImage
from kivy.uix.videoplayer import VideoPlayer

# Importa la clase DatabaseHandler del archivo database.py
from database import DatabaseHandler

class VideoWidget(VideoPlayer):
    def __init__(self, video_data=None, **kwargs):
        super(VideoWidget, self).__init__(**kwargs)
        if video_data:
            self.video_data = video_data

class RegistrationApp(App):
    def __init__(self):
        super().__init__()
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.hand_detected = False
        self.temp_video_filename = None
        self.user_name = ""  # Inicializa user_name

    def build(self):
        self.title = "Registro con Foto y Video"
        self.registered = False
        self.photo_taken = False
        self.video_recording = False

        self.layout = BoxLayout(orientation="vertical")

        # Crear el widget TabbedPanel
        self.tabbed_panel = TabbedPanel(do_default_tab=False)
        self.layout.add_widget(self.tabbed_panel)

        # Pestaña de Registro
        self.tab_register = TabbedPanelHeader(text="Registro")
        self.register_content = BoxLayout(orientation="vertical")
        self.name_input = TextInput(hint_text="Nombre")
        self.register_button = Button(text="Registrarse")
        self.register_button.bind(on_press=self.register)
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
        self.gallery_images = GridLayout(cols=3)  # GridLayout para mostrar las imágenes
        self.load_images_and_videos()  # Carga las imágenes y videos en el GridLayout

        self.gallery_content.add_widget(Label(text="Fotos y Videos Guardados"))
        self.gallery_content.add_widget(ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100), do_scroll_x=False))
        self.gallery_content.children[1].add_widget(self.gallery_images)  # Agregar el GridLayout al ScrollView
        self.tab_gallery.content = self.gallery_content
        self.tabbed_panel.add_widget(self.tab_gallery)

        return self.layout

    def register(self, instance):
        name = self.name_input.text
        if name:
            self.user_name = name

            # Captura una foto
            image = self.capture_camera_image()

            # Detecta caras en la foto
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                # Si se detecta al menos una cara, guarda la foto con el nombre proporcionado
                image_filename = f"{self.user_name}_photoRegistro.png"
                cv2.imwrite(image_filename, image)
                print(f"Foto tomada y guardada como {image_filename}")
                self.registered = True

                # Inserta el usuario en la base de datos
                self.db_handler.insert_user(self.user_name)

                # Agregar pestaña de Video después del registro
                if not self.video_recording:
                    self.video_recording = True
                    self.tab_video = TabbedPanelHeader(text="Video")
                    self.video_content = BoxLayout(orientation="vertical")
                    self.video_button = Button(text="Grabar Video")
                    self.video_button.bind(on_press=self.record_video)
                    self.video_content.add_widget(Label(text="Grabación de Video"))
                    self.video_content.add_widget(self.video_button)
                    self.tab_video.content = self.video_content
                    self.tabbed_panel.add_widget(self.tab_video)

                # Cambiar a la pestaña de Video
                self.tabbed_panel.switch_to(self.tab_video)
            else:
                print("No se detectaron caras en la foto. Intenta nuevamente.")
        else:
            print("Por favor, ingresa tu nombre.")

    def capture_camera_image(self):
        # Captura una imagen de la cámara
        camera = self.camera
        if camera is not None and camera.texture is not None:
            buf = camera.texture.pixels
            if buf is not None:
                image = np.frombuffer(buf, dtype='uint8')
                image = image.reshape(camera.texture.height, camera.texture.width, -1)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                return image
            else:
                print("No se pudo capturar una imagen de la cámara. Buffer de imagen nulo.")
        else:
            print("No se pudo capturar una imagen de la cámara. La cámara no está disponible.")
        return None

    def record_video(self, instance):
        if not self.registered:
            print("Primero debes registrarte antes de grabar un video.")
        else:
            self.video_button.text = "Grabando..."
            self.video_button.disabled = True

            cap = cv2.VideoCapture(0)
            video_frames = []

            start_time = time.time()
            recording = False

            while True:
                ret, frame = cap.read()

                if not recording:
                    if not self.hand_detected:
                        # Detecta la mano derecha en el cuadro actual
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        results = self.hands.process(frame_rgb)

                        if results.multi_hand_landmarks:
                            # Se detectó la mano derecha
                            self.hand_detected = True
                            start_time = time.time()

                    elif time.time() - start_time >= 5:
                        # Toma una foto después de 5 segundos
                        image_filename = f"{self.user_name}_photoManoDer.png"
                        cv2.imwrite(image_filename, frame)
                        print(f"Foto tomada y guardada como {image_filename}")
                        recording = True
                        self.photo_taken = True

                if recording:
                    # Añade el cuadro al video
                    video_frames.append(frame)

                    if not self.hand_detected:
                        # Detén la grabación si la mano derecha ya no se detecta
                        self.save_video(video_frames)
                        self.video_button.text = "Grabar Video"
                        self.video_button.disabled = False
                        break

                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    if not recording:
                        self.video_button.text = "Grabar Video"
                        self.video_button.disabled = False
                    else:
                        self.save_video(video_frames)
                    break

            cap.release()
            cv2.destroyAllWindows()

    def save_video(self, frames):
        if frames:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_filename = f"{self.user_name}_videoManoDer.mp4"
            out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frames[0].shape[1], frames[0].shape[0]))
            for frame in frames:
                out.write(frame)
            out.release()

            # Inserta el video en la base de datos
            self.db_handler.insert_video(self.user_name, video_filename)
            print(f"Video grabado y guardado como {video_filename}")
        else:
            print("No se grabó ningún video.")

    def load_images_and_videos(self):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect("image_database.db")
        cursor = conn.cursor()

        # Consulta para seleccionar todas las imágenes y videos
        cursor.execute('SELECT user_name, image_data FROM images UNION SELECT user_name, video_data FROM videos')

        # Obtener todas las filas de resultados
        rows = cursor.fetchall()

        # Iterar a través de las filas y mostrar las imágenes y videos
        for row in rows:
            user_name, data = row

            if data.startswith(b'\x89PNG'):
                # Es una imagen
                image_texture = self.load_image_from_data(data)
                image_widget = Image(texture=image_texture)
                # Aumenta el tamaño de las imágenes en la galería
                image_widget.size = (300, 300)
                self.gallery_images.add_widget(image_widget)
            elif data.startswith(b'\x1aE\xdf\xa3'):
                # Es un video
                video_widget = self.load_video_from_data(data)
                self.gallery_images.add_widget(video_widget)

        # Cerrar la conexión a la base de datos
        conn.close()

    def load_video_from_data(self, video_data):
        video_filename = "temp_video.mp4"  # Nombre de archivo temporal
        with open(video_filename, "wb") as f:
            f.write(video_data)

        video_widget = VideoWidget(video_data=video_data, source=video_filename)
        return video_widget

    def load_image_from_data(self, data):
        # Cargar una imagen desde los datos binarios
        image_data = BytesIO(data)
        image_texture = CoreImage(io.BytesIO(data), ext="png").texture
        return image_texture

    def on_stop(self):
        # Cierra la base de datos cuando la aplicación se detiene
        self.db_handler.close()

if __name__ == "__main__":
    Window.clearcolor = (1, 1, 1, 1)
    RegistrationApp().run()
