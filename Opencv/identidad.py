# Iteramos con las imagenes de la carpeta
from deepface import DeepFace
import os


def validar_identidad():
    # Ruta de la carpeta con las imágenes
    carpeta_imagenes = "Faces"

    # Lista de archivos en la carpeta
    archivos = os.listdir(carpeta_imagenes)

    # Ruta de la imagen capturada para login
    imagen_referencia = "captured_image.jpg"

    print("Validando Identidad...")
    # Verificar la identidad de cada imagen en la carpeta con respecto a la imagen de referencia
    for archivo in archivos:
        # Ruta completa de la imagen actual
        imagen_actual = os.path.join(carpeta_imagenes, archivo)

        # Verificar la identidad de la imagen actual con respecto a la imagen de referencia
        try: 
            validacion = DeepFace.verify(img1_path=imagen_referencia, img2_path=imagen_actual)["verified"]
            if validacion:
                #resultado = True
                #break
                
                # Si encuentra 1 rostro similar corta el for y devuelve true
                print("Usuario Valido.")
                return True
        except Exception as e:
            print(f"Rostro no encontrado para {archivo}")

        # Imprimir el resultado
        # print(f"Verificación para {archivo}: {resultado}")

    # Si termino el for sin encontrar el rostro devuelve False
    print("Usuario no encontrado")
    return False


    #if resultado:
    #    print(f"Usuario Valido. [{archivo}]")
    #else:
    #    print("No se pudo validar el usuario")