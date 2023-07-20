import sqlite3
import textwrap
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView



def crear_tabla_productos():
    conn = sqlite3.connect('productos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, precio REAL, stock INTEGER)''')
    conn.commit()
    conn.close()


def mostrar_mensaje(message, x):
    wrapped_message = textwrap.fill(message, width=60)  # Tabular el mensaje en líneas de 60 caracteres
    popup = Popup(title='Mensaje', content=Label(text=wrapped_message), size_hint=(None, None), size=(x, 200))
    popup.open()


class Producto:
    def __init__(self, id, nombre, precio, stock):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def buscar_por_id(self):
        try:
            conn = sqlite3.connect('productos.db')
            c = conn.cursor()
            c.execute("select * from productos where id = ?", (self.id,))
            resultado = c.fetchone()
            conn.close()

            if resultado is not None:
                # Crear una instancia de Producto con los datos obtenidos de la base de datos
                producto = Producto(resultado[0], resultado[1], resultado[2], resultado[3])
                return producto
            else:
                return None

        except sqlite3.Error as e:
            error_message = 'Ocurrió un error de SQLite: ' + str(e)
            mostrar_mensaje(error_message, 400)

        except Exception as e:
            error_message = 'Ocurrió un error: ' + str(e)
            mostrar_mensaje(error_message, 400)

    def buscar_por_nombre(self):
        try:
            conn = sqlite3.connect('productos.db')
            c = conn.cursor()
            nombre = f"%{self.nombre}%"
            c.execute("select * from productos where nombre like ?", (nombre,))
            resultados = c.fetchall()
            conn.close()

        except sqlite3.Error as e:
            error_message = 'Ocurrió un error de SQLite: ' + str(e)
            mostrar_mensaje(error_message, 400)

        except Exception as e:
            error_message = 'Ocurrió un error: ' + str(e)
            mostrar_mensaje(error_message, 400)

        return len(resultados)

    def guardar(self):
        try:
            conn = sqlite3.connect('productos.db')
            c = conn.cursor()
            c.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                      (self.nombre, self.precio, self.stock))
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            error_message = 'Ocurrió un error de SQLite: ' + str(e)
            mostrar_mensaje(error_message, 400)

        except Exception as e:
            error_message = 'Ocurrió un error: ' + str(e)
            mostrar_mensaje(error_message, 400)

    @staticmethod
    def obtener_todos():
        try:
            conn = sqlite3.connect('productos.db')
            c = conn.cursor()
            c.execute("SELECT * FROM productos")
            rows = c.fetchall()
            productos = []
            for row in rows:
                producto = Producto(row[0], row[1], row[2], row[3])
                productos.append(producto)
            conn.close()

        except sqlite3.Error as e:
            # Manejar cualquier excepción específica de SQLite que pueda ocurrir
            print('Ocurrió un error de SQLite:', str(e))

        except Exception as e:
            # Manejar cualquier otra excepción que pueda ocurrir
            print('Ocurrió un error:', str(e))

        return productos

    def actualizar(self):
        try:
            conn = sqlite3.connect('productos.db')
            c = conn.cursor()
            c.execute("UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?",
                      (self.nombre, self.precio, self.stock, self.id))
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            error_message = 'Ocurrió un error de SQLite: ' + str(e)
            mostrar_mensaje(error_message, 400)

        except Exception as e:
            error_message = 'Ocurrió un error: ' + str(e)
            mostrar_mensaje(error_message, 400)

    def eliminar(self):
        try:
            conn = sqlite3.connect('productos.db')
            c = conn.cursor()
            c.execute("DELETE FROM productos WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            error_message = 'Ocurrió un error de SQLite: ' + str(e)
            mostrar_mensaje(error_message, 400)

        except Exception as e:
            error_message = 'Ocurrió un error: ' + str(e)
            mostrar_mensaje(error_message, 400)


class AddProduct(BoxLayout):
    def __init__(self, list_tab, **kwargs):
        super().__init__(**kwargs)
        self.list_tab = list_tab
        self.orientation = 'vertical'
        self.padding = [20, 20, 20, 20]
        self.spacing = 10

        self.nombre_input = TextInput(hint_text='Nombre', multiline=False, background_color=(1, 1, 1, 1))
        self.add_widget(self.nombre_input)

        self.precio_input = TextInput(hint_text='Precio', multiline=False, background_color=(1, 1, 1, 1))
        self.add_widget(self.precio_input)

        self.stock_input = TextInput(hint_text='Stock', multiline=False, background_color=(1, 1, 1, 1))
        self.add_widget(self.stock_input)

        self.guardar_button = Button(text='Guardar', background_color=(0.3, 0.6, 0.9, 1))
        self.guardar_button.bind(on_press=self.guardar_producto)
        self.add_widget(self.guardar_button)

    def guardar_producto(self, instance):
        nombre = self.nombre_input.text
        precio = self.precio_input.text
        stock = self.stock_input.text

        if nombre:
            if precio.replace('.', '', 1).isdigit():
                precio = float(precio)
            else:
                mostrar_mensaje(
                    'El valor del Precio debe ser un número decimal o entero y puede contener decimales utilizando el punto (.) como separador.',
                    500)
                return

            if stock.isdigit():
                stock = int(stock)
            else:
                mostrar_mensaje('El valor del Stock debe ser un numero entero mayor o igual a 0.', 450)
                return

            producto = Producto(id, nombre, precio, stock)
            if producto.buscar_por_nombre() > 0:
                mostrar_mensaje('Ya existe un producto con este nombre', 400)
            else:
                producto.guardar()
                self.list_tab.actualizar_lista()  # Actualizar la lista de productos en ListProductTab
                mostrar_mensaje('Producto guardado correctamente.', 400)
                self.limpiar_campos()
        else:
            mostrar_mensaje('Todos los campos son requeridos.', 400)

    def limpiar_campos(self):
        self.nombre_input.text = ''
        self.precio_input.text = ''
        self.stock_input.text = ''


class ActualizarProd(BoxLayout):
    def __init__(self, list_tab, **kwargs):
        super().__init__(**kwargs)
        self.list_tab = list_tab
        self.orientation = 'vertical'
        self.padding = [20, 20, 20, 20]
        self.spacing = 10

        self.id_input = TextInput(hint_text='ID', multiline=False, background_color=(1, 1, 1, 1))
        self.add_widget(self.id_input)

        self.nombre_input = TextInput(hint_text='Nombre', multiline=False, background_color=(1, 1, 1, 1))
        self.add_widget(self.nombre_input)

        self.precio_input = TextInput(hint_text='Precio', multiline=False, background_color=(1, 1, 1, 1))
        self.add_widget(self.precio_input)

        self.stock_input = TextInput(hint_text='Stock', multiline=False, background_color=(1, 1, 1, 1))
        self.add_widget(self.stock_input)

        self.actualizar_button = Button(text='Actualizar', background_color=(0.3, 0.6, 0.9, 1))
        self.actualizar_button.bind(on_press=self.actualizar_producto)
        self.add_widget(self.actualizar_button)

    def actualizar_producto(self, instance):
        id = self.id_input.text
        nombre = self.nombre_input.text
        precio = self.precio_input.text
        stock = self.stock_input.text

        producto = Producto(id, nombre, precio, stock)

        if id.isdigit():
            # Verificar si el producto existe por su ID
            if producto.buscar_por_id() is not None:
                if nombre:
                    if precio.replace('.', '', 1).isdigit():
                        precio = float(precio)
                    else:
                        mostrar_mensaje(
                            'El valor del Precio debe ser flotante o entero y puede contener decimales utilizando el punto (.)',
                            500)
                        return

                    if stock.isdigit() and int(stock) >= 0:
                        stock = int(stock)
                    else:
                        mostrar_mensaje('El valor del Stock debe ser un número entero mayor o igual a 0.', 500)
                        return

                    producto.actualizar()
                    self.list_tab.actualizar_lista()  # Actualizar la lista de productos en ListProductTab
                    mostrar_mensaje('Producto actualizado correctamente.', 400)
                    self.limpiar_campos()
                else:
                    mostrar_mensaje('Todos los campos son requeridos.', 400)
            else:
                mostrar_mensaje('Debe ingresar el ID de un producto existente', 400)
        else:
            mostrar_mensaje('El ID debe ser un valor numérico', 400)

    def limpiar_campos(self):
        self.id_input.text = ''
        self.nombre_input.text = ''
        self.precio_input.text = ''
        self.stock_input.text = ''


class ListProductTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [-600, 1250, 10, 100]
        self.spacing = 5

        self.list_label = Label(text='', size_hint_y=None)
        self.list_label.bind(texture_size=self.list_label.setter('size'))
        root = ScrollView(size_hint=(1, None), size=(400, 400))
        root.add_widget(self.list_label)
        
       

        self.actualizar_lista()
        self.add_widget(root)
        

    def actualizar_lista(self):
        productos = Producto.obtener_todos()
        texto = ''
        for producto in productos:
            texto += f'Producto: {producto.nombre}\n'
            texto += f'ID: {producto.id}\n'
            texto += f'Precio: $ {producto.precio} \n'
            texto += f'Stock: {producto.stock} u\n\n'
        self.list_label.text = texto


class EliminarProd(BoxLayout):
    def __init__(self, list_tab, **kwargs):
        super().__init__(**kwargs)
        self.list_tab = list_tab
        self.orientation = 'vertical'
        self.padding = [20, 20, 20, 20]
        self.spacing = 10

        self.id_input = TextInput(hint_text='ID', multiline=False, background_color=(1, 1, 1, 1))
        self.add_widget(self.id_input)

        self.eliminar_button = Button(text='Eliminar', background_color=(0.3, 0.6, 0.9, 1))
        self.eliminar_button.bind(on_press=self.eliminar_producto)
        self.add_widget(self.eliminar_button)

    def eliminar_producto(self, instance):
        id = self.id_input.text

        if id.isdigit():
            producto = Producto(id, '', 0, 0)
            producto= producto.buscar_por_id()

            if producto is not None:
                self.limpiar_campos()
                producto.eliminar()
                self.list_tab.actualizar_lista()  # Actualizar la lista de productos en ListProductTab
                mostrar_mensaje('Producto: '+producto.nombre+ ' eliminado correctamente.', 400)
            else:
                mostrar_mensaje('No existe un producto con ese ID', 400)
        else:
            mostrar_mensaje('El ID del producto es requerido y debe ser numérico.', 400)

    def limpiar_campos(self):
        self.id_input.text = ''


class VerduApp(App):
    def build(self):
        Window.clearcolor = (0.90, 0.80, 0.70, 1)  # Cambiar el color de fondo de la ventana

        crear_tabla_productos()

        tabbed_panel = TabbedPanel(do_default_tab=False)

        list_tab = ListProductTab()
        add_tab = TabbedPanelItem(text='Añadir', background_color=(0.2, 0.4, 0.6, 1))  # color pestaña
        add_tab.content = AddProduct(list_tab)
        tabbed_panel.add_widget(add_tab)

        update_tab = TabbedPanelItem(text='Actualizar', background_color=(0.2, 0.4, 0.6, 1))
        update_tab.content = ActualizarProd(list_tab)
        tabbed_panel.add_widget(update_tab)

        list_tab_item = TabbedPanelItem(text='Listar', background_color=(0.2, 0.4, 0.6, 1))
        list_tab_item.content = list_tab
        tabbed_panel.add_widget(list_tab_item)
        

        delete_tab = TabbedPanelItem(text='Eliminar', background_color=(0.2, 0.4, 0.6, 1))
        delete_tab.content = EliminarProd(list_tab)
        tabbed_panel.add_widget(delete_tab)

        return tabbed_panel

if __name__ == '__main__':
    VerduApp().run()
