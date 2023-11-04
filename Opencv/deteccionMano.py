from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

import mediapipe as mp
import time
from threading import Thread
import datetime
import numpy as np # Para la creacion del video e imagenes
# Usado para convertir el mensaje protobuf en un diccionario.
from google.protobuf.json_format import MessageToDict

from kivy.uix.screenmanager import ScreenManager, Screen


class CameraScreen(Screen):
    # Inicializar contadores y variables
    left_counter = 0
    right_counter = 0
    is_recording = False
    photo_taken = False # Variable para que no saque repetidas las fotos

    # Agrega variables para manejar la grabación de video
    video_writer = None 
    frame_width = int(cv2.VideoCapture(0).get(3))
    frame_height = int(cv2.VideoCapture(0).get(4))

    # Inicializar el modelo de detección de manos
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Camera Screen" 

        # Define el LayOut para kivy
        layout = BoxLayout(orientation='vertical')
        self.capture = cv2.VideoCapture(0)
        self.image = Image()
        
        # Agregar la vista de la cámara
        layout.add_widget(self.image)

        # Agregar un Label inicial debajo de la cámara
        self.label = Label(text="", size_hint_y=None, height=50)
        layout.add_widget(self.label)

        # Botón para regresar a la pantalla de índice
        files_button = Button(text="<< Back", size_hint=(None, None), size = (100, 50))
        files_button.bind(on_press=self.go_to_index)
        layout.add_widget(files_button)

        # ######################

        # Iniciar el temporizador en un hilo separado
        timer_thread = Thread(target=self.timer_function)
        timer_thread.daemon = True  # El hilo del temporizador se detendrá cuando el programa principal termine
        timer_thread.start()

        # ######################

        # Programa una función para actualizar la imagen en pantalla
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS

        self.add_widget(layout)
    

    # Función para el temporizador
    def timer_function(self):
        #global right_counter, left_counter, photo_taken
        while True:
            time.sleep(1)
            self.right_counter += 1
            self.left_counter += 1
            if self.left_counter == 6:
                self.left_counter = 0
                self.photo_taken = False


    # Funcion que se acutaliza constantemente para la camara
    def update(self, dt):

        ret, frame = self.capture.read()

        if ret:

            # Convierte la imagen de OpenCV en una textura Kivy
            # frame = cv2.flip(frame, 1) # Aplicar efecto espejo (reflejar horizontalmente) a la imagen
            img = self.capture
            img2 = cv2.flip(frame, 0).tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(img2, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture1

            # ############################################################

            # Leer el cuadro de video y voltear la imagen
            success, img = img.read()
            img = cv2.flip(img, 1)

            # Convertir la imagen BGR a RGB y procesarla
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)

            # Si se detectan manos en la imagen (frame)
            if results.multi_hand_landmarks:

                # Obtiene la fecha y hora actual y la formate
                now = datetime.datetime.now()
                date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
                
                # Se detectan dos manos
                if len(results.multi_handedness) == 2:
                    # Indica que se detectaron ambas manos
                    self.label.text = f"Ambas Manos Detectadas"
                    # Reinicia el contador y el video si se detectan ambas
                    self.right_counter = 0
                    self.left_counter = 0
                    if self.is_recording:
                        self.video_writer.release()
                        self.is_recording = False
                    
                # Se detecta una sola mano
                else:
                    for i in results.multi_handedness:
                        
                        # Devoluelve si es una mano derecha o izquierda
                        etiqueta = MessageToDict(i)['classification'][0]['label']

                        if etiqueta == 'Left':

                            # Mano Izquierda en pantalla
                            # Si llega a los 5 segundo con la mano levantada sacar foto
                            if self.left_counter == 5 and not self.photo_taken:
                                self.label.text = f"Tomando Foto..."
                                # Captura una imagen cuando el contador llega a 5
                                cv2.imwrite(f"Galeria/imagen{date_time_str}.jpg", img)
                                self.photo_taken = True
                            else:
                                self.label.text = f"{5 - self.left_counter} segundos para foto"
                            
                        if etiqueta == 'Right':

                            # Mano Derecha en pantalla
                            # Si llega a 5 segundos comenzar a grabar video
                            if self.right_counter >= 5:
                                self.label.text = f"{self.right_counter - 5} segundos grabando"
                                # Comienza la grabación de video cuando el contador llega a 5
                                if not self.is_recording:
                                    self.video_writer = cv2.VideoWriter(f"Galeria/video{date_time_str}.mp4", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (self.frame_width, self.frame_height))
                                    self.is_recording = True
                            else:
                                self.label.text = f"{5 - self.right_counter} segundos para comenzar a grabar"
            
            else:
                # Si no detecta ninguna mano
                self.label.text = f""
                # Reinicia contador
                self.right_counter = 0
                self.left_counter = 0

            if self.is_recording:
                self.video_writer.write(img)

            # ############################################################

    # Actualiza el titulo
    def on_pre_enter(self):
        App.get_running_app().title = self.title

    # Cambia de pagina al IndexPage
    def go_to_index(self, instance):
        self.manager.current = "index"

    # Libera la cámara al cerrar la aplicación
    def on_stop(self):
        self.capture.release()
        Clock.unschedule(self.update) # Paramos el refresco de la camara

