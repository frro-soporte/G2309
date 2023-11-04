import cv2

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import datetime

from identidad import validar_identidad 

class LoginScreen2(Screen):
    log_in = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Log In"  
        layout = BoxLayout(orientation='vertical')

        # Agregar un Label inicial arriba de la cámara
        self.label = Label(text="Login para ingresar.", size_hint_y=None, height=30)
        layout.add_widget(self.label)
        
        # Config. para la camara en kivy
        self.capture = cv2.VideoCapture(0)
        self.image = Image()
        layout.add_widget(self.image)

        buttonsLayout = BoxLayout(orientation='horizontal', spacing=10, size_hint= (None, None), height=50, padding = 10, pos_hint = {'center_x': 0.40})
         
        login_button = Button(text="Login", size_hint=(None, None), size=(100, 50))
        login_button.bind(on_press=self.capture_validate_image)
        buttonsLayout.add_widget(login_button)
# 
        login_button = Button(text="Create User", size_hint=(None, None), size=(100, 50))
        login_button.bind(on_press=self.create_user)
        buttonsLayout.add_widget(login_button)

        layout.add_widget(buttonsLayout)

        # Programa una función para actualizar la imagen en pantalla
        Clock.schedule_interval(self.update, 1.0 / 30.0) # 30 FPS

        # Agregamos el layout
        self.add_widget(layout)


    # Refresco de imafen para camara
    def update(self, dt):

        ret, frame = self.capture.read()

        if ret:
            # Convierte la imagen de OpenCV en una textura Kivy
            frame = cv2.flip(frame, 1) # Aplicar efecto espejo (reflejar horizontalmente) a la imagen
            buf = cv2.flip(frame, 0).tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # Muestra la imagen desde la cámara en la interfaz de Kivy
            self.image.texture = texture1

        if self.log_in:
            print("LOG IN")
            self.on_stop() # Paramos la camara
            self.go_to_index() # Vamos a la IdexScreen

    
    # Funcion para sacar la foto y validarla
    def capture_validate_image(self, instance):

        self.label.text = "Validando identidad..."

        # Captura una imagen y guarda en un archivo
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite("captured_image.jpg", frame)
            print("Imagen capturada y guardada como 'captured_image.jpg'")

        try:
            # Valida la identidad de la cara en la foto
            self.log_in = validar_identidad()
            if not self.log_in:
                self.label.text = f"Usuario no encontrado."

        except Exception as e:
            print(e)

    
    def create_user(self, instance):

        # Obtiene la fecha y hora actual y la formate
        now = datetime.datetime.now()
        date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

        # Captura una imagen y guarda en un archivo
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite(f"Faces/{date_time_str}.jpg", frame)
            self.label.text = f"Usuario creado con exito."
            print("Usuario Creado.")


    # Cambia de pagina al IndexPage
    def go_to_index(self):
        self.manager.current = "index"

    
    # Actualiza el titulo
    def on_pre_enter(self):
        App.get_running_app().title = self.title


    # Libera la cámara al cerrar la aplicación
    def on_stop(self):
        self.capture.release()
        Clock.unschedule(self.update) # Paramos el refresco de la camara

