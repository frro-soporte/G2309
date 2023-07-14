import sqlite3
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window


def crear_tabla_productos():
    conn = sqlite3.connect('productos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productos
                 (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL, stock INTEGER)''')
    conn.commit()
    conn.close()


class Producto:
    def __init__(self, id, nombre, precio, stock):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def guardar(self):
        conn = sqlite3.connect('productos.db')
        c = conn.cursor()
        c.execute("INSERT INTO productos (id, nombre, precio, stock) VALUES (?, ?, ?, ?)",
                  (self.id, self.nombre, self.precio, self.stock))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todos():
        conn = sqlite3.connect('productos.db')
        c = conn.cursor()
        c.execute("SELECT * FROM productos")
        rows = c.fetchall()
        productos = []
        for row in rows:
            producto = Producto(row[0], row[1], row[2], row[3])
            productos.append(producto)
        conn.close()
        return productos

    def actualizar(self):
        conn = sqlite3.connect('productos.db')
        c = conn.cursor()
        c.execute("UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?",
                  (self.nombre, self.precio, self.stock, self.id))
        conn.commit()
        conn.close()

    def eliminar(self):
        conn = sqlite3.connect('productos.db')
        c = conn.cursor()
        c.execute("DELETE FROM productos WHERE id=?", (self.id,))
        conn.commit()
        conn.close()


class AddProduct(BoxLayout):
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

        self.guardar_button = Button(text='Guardar', background_color=(0.3, 0.6, 0.9, 1))
        self.guardar_button.bind(on_press=self.guardar_producto)
        self.add_widget(self.guardar_button)

    def guardar_producto(self, instance):
        id = self.id_input.text
        nombre = self.nombre_input.text
        precio = float(self.precio_input.text)
        stock = int(self.stock_input.text)

        if id and nombre and precio and stock:
            producto = Producto(id, nombre, precio, stock)
            producto.guardar()
            self.list_tab.actualizar_lista()  # Actualizar la lista de productos en ListProductTab
            self.limpiar_campos()
            self.mostrar_mensaje('Producto guardado correctamente.')
        else:
            self.mostrar_mensaje('Todos los campos son requeridos.')

    def limpiar_campos(self):
        self.id_input.text = ''
        self.nombre_input.text = ''
        self.precio_input.text = ''
        self.stock_input.text = ''

    def mostrar_mensaje(self, mensaje):
        popup = Popup(title='Mensaje', content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


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
        precio = float(self.precio_input.text)
        stock = int(self.stock_input.text)

        if id and nombre and precio and stock:
            producto = Producto(id, nombre, precio, stock)
            producto.actualizar()
            self.list_tab.actualizar_lista()  # Actualizar la lista de productos en ListProductTab
            self.limpiar_campos()
            self.mostrar_mensaje('Producto actualizado correctamente.')
        else:
            self.mostrar_mensaje('Todos los campos son requeridos.')

    def limpiar_campos(self):
        self.id_input.text = ''
        self.nombre_input.text = ''
        self.precio_input.text = ''
        self.stock_input.text = ''

    def mostrar_mensaje(self, mensaje):
        popup = Popup(title='Mensaje', content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


class ListProductTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [-600, -200, 10, 100]
        self.spacing = 5

        self.list_label = Label(text='')
        self.add_widget(self.list_label)

        self.actualizar_lista()

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

        if id:
            producto = Producto(id, '', 0, 0)
            producto.eliminar()
            self.list_tab.actualizar_lista()  # Actualizar la lista de productos en ListProductTab
            self.limpiar_campos()
            self.mostrar_mensaje('Producto eliminado correctamente.')
        else:
            self.mostrar_mensaje('El ID del producto es requerido.')

    def limpiar_campos(self):
        self.id_input.text = ''

    def mostrar_mensaje(self, mensaje):
        popup = Popup(title='Mensaje', content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


class VerduApp(App):
    def build(self):
        Window.clearcolor = (0.90, 0.80, 0.70, 1)  # Cambiar el color de fondo de la ventana

        crear_tabla_productos()

        tabbed_panel = TabbedPanel(do_default_tab=False)

        list_tab = ListProductTab()
        add_tab = TabbedPanelItem(text='Añadir', background_color=(0.2, 0.4, 0.6, 1)) #color pestaña
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
