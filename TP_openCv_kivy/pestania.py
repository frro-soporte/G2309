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
from kivy.core.window import Window
import tempfile
import os

class RegistrationApp(App):
        
    def __init__(self):
        super().__init__()
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.hand_detected = False
        self.temp_video_filename = None
    
    def build(self):
        self.title = "Registro con Foto y Video"
        self.registered = False
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
                self.save_image_to_database(image_filename, image)
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
    
    def save_image_to_database(self, image_filename, image):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect("image_database.db")
        cursor = conn.cursor()

        # Crear una tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY,
                user_name TEXT,
                image_data BLOB
            )
        ''')

        # Leer la imagen en formato de bytes
        with open(image_filename, "rb") as f:
            image_data = f.read()

        # Insertar la imagen y el nombre del usuario en la base de datos
        cursor.execute('''
            INSERT INTO images (user_name, image_data)
            VALUES (?, ?)
        ''', (self.user_name, image_data))

        # Guardar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        print(f"Foto tomada y guardada en la base de datos como {image_filename}")

    def record_video(self, instance):
        if not self.registered:
            print("Primero debes registrarte antes de grabar un video.")
        else:
            cap = cv2.VideoCapture(0)
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

                if recording:
                    # Inicia la grabación de video
                    if not self.hand_detected:
                        # Detén la grabación si la mano derecha ya no se detecta
                        break
                    else:
                        # Guarda el cuadro en el video
                        # Debes implementar la lógica para grabar el video aquí
                        pass

                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
               
               
    
    def save_video_to_database(self, video_filename):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect("image_database.db")
        cursor = conn.cursor()

        # Crear una tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY,
                user_name TEXT,
                video_data BLOB
            )
        ''')

        # Leer el video en formato de bytes
        with open(video_filename, "rb") as f:
            video_data = f.read()

        # Insertar el video y el nombre del usuario en la base de datos
        cursor.execute('''
            INSERT INTO videos (user_name, video_data)
            VALUES (?, ?)
        ''', (self.user_name, video_data))

        # Guardar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        print(f"Video grabado y guardado en la base de datos como {video_filename}")                





if __name__ == "__main__":
    Window.clearcolor = (1, 1, 1, 1)
    RegistrationApp().run()
