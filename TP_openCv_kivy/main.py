#Crear una aplicación CÁMARA empleando OpenCV y Kivy con las siguientes características:

#1) Logeo por reconocimiento facial 
#(tener el cuenta solo el alta de ususario, no es necesario bajas y modificaciones).

#2) Si detecta un rostro que habilite la captura según las siguientes situaciones:

#	a) Si detecta la mano izquierda:
# Tomar una foto cuando cuente 5 segundos mostrando en la pantalla la cuenta regresiva.
#	b) Si detecta la mano derecha:
# Grabar un video hasta que deje de detectar la mano derecha.

#3) Grabar el nombre de los archivos creados (video o imágenes) en una base de datos 
#y mostrar en una lista para poder reproducirla mediante un click.
# Importa las bibliotecas necesarias
import cv2
import time
import mediapipe as mp
import sqlite3
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
        self.user_name = ""

    def build(self):
        self.title = "Registro con Foto y Video"
        self.registered = False
        self.video_recording = False
        self.photo_taken = False

        self.layout = BoxLayout(orientation="vertical")

        # Create the TabbedPanel widget
        self.tabbed_panel = TabbedPanel(do_default_tab=False)
        self.layout.add_widget(self.tabbed_panel)

        # Registration Tab
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

        # Add a new tab to display saved photos and videos
        self.tab_gallery = TabbedPanelHeader(text="Galería")
        self.gallery_content = BoxLayout(orientation="vertical")
        self.gallery_images = GridLayout(cols=3)
        self.load_images_and_videos()

        self.gallery_content.add_widget(Label(text="Fotos y Videos Guardados"))
        self.gallery_content.add_widget(ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100), do_scroll_x=False))
        self.gallery_content.children[1].add_widget(self.gallery_images)
        self.tab_gallery.content = self.gallery_content
        self.tabbed_panel.add_widget(self.tab_gallery)

        return self.layout

    def register(self, instance):
        name = self.name_input.text
        if name:
            self.user_name = name
            image = self.capture_camera_image()

            if image is not None:
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(faces) > 0:
                    image_filename = f"{self.user_name}_photoRegistro.png"
                    cv2.imwrite(image_filename, image)
                    print(f"Foto tomada y guardada como {image_filename}")
                    self.registered = True
                    self.save_image_to_database(image_filename, image)

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

                    self.tabbed_panel.switch_to(self.tab_video)
                else:
                    print("No se detectaron caras en la foto. Intenta nuevamente.")
            else:
                print("No se pudo capturar una imagen de la cámara. La cámara no está disponible.")
        else:
            print("Por favor, ingresa tu nombre.")

    def capture_camera_image(self):
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
        return None

    def save_image_to_database(self, image_filename, image):
        conn = sqlite3.connect("image_database.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY,
                user_name TEXT,
                image_data BLOB
            )
        ''')

        with open(image_filename, "rb") as f:
            image_data = f.read()

        cursor.execute('''
            INSERT INTO images (user_name, image_data)
            VALUES (?, ?)
        ''', (self.user_name, image_data))

        conn.commit()
        conn.close()

        print(f"Foto tomada y guardada en la base de datos como {image_filename}")

    def record_video(self, instance):
        if not self.registered:
            print("Primero debes registrarte antes de grabar un video.")
        else:
            try:
                cap = cv2.VideoCapture(0)
                start_time = time.time()
                recording = False
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = None

                while True:
                    ret, frame = cap.read()

                    if not recording:
                        if not self.hand_detected:
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            results = self.hands.process(frame_rgb)

                            if results.multi_hand_landmarks:
                                for landmarks in results.multi_hand_landmarks:
                                    for lm in landmarks.landmark:
                                        if lm.y > 0.7:
                                            self.hand_detected = True
                                            if lm.x < 0.5:
                                                image_filename = f"{self.user_name}_photoManoIzq.png"
                                                cv2.imwrite(image_filename, frame)
                                                print(f"Foto tomada y guardada como {image_filename}")
                                                self.photo_taken = True
                                            else:
                                                recording = True
                                                start_time = time.time()

                    if recording:
                        if out is None:
                            video_filename = f"{self.user_name}_video.mp4"
                            out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))
                        out.write(frame)

                    cv2.imshow('Video', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                cap.release()
                if out is not None:
                    out.release()
                cv2.destroyAllWindows()

                self.hand_detected = False
            except Exception as e:
                print(f"Error al grabar el video: {str(e)}")

    def load_images_and_videos(self):
        conn = sqlite3.connect("image_database.db")
        cursor = conn.cursor()

        cursor.execute('SELECT user_name, image_data FROM images UNION SELECT user_name, video_data FROM videos')

        rows = cursor.fetchall()

        for row in rows:
            user_name, data = row
            
            if data.startswith(b'\x89PNG'):
                image_texture = self.load_image_from_data(data)
                image_widget = Image(texture=image_texture)
                image_widget.size = (300, 300)
                self.gallery_images.add_widget(image_widget)
            elif data.startswith(b'\x1aE\xdf\xa3'):
                video_widget = self.load_video_from_data(data)
                self.gallery_images.add_widget(video_widget)

        conn.close()

    def load_video_from_data(self, video_data):
        video_filename = "temp_video.mp4"
        with open(video_filename, "wb") as f:
            f.write(video_data)

        video_widget = VideoWidget(video_data=video_data, source=video_filename)
        return video_widget
    
    def load_image_from_data(self, data):
        image_data = BytesIO(data)
        image_texture = CoreImage(io.BytesIO(data), ext="png").texture
        return image_texture

if __name__ == "__main__":
    Window.clearcolor = (1, 1, 1, 1)
    RegistrationApp().run()
