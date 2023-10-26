import sqlite3

class DatabaseHandler:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Crea las tablas necesarias en la base de datos
        # Puedes definir la estructura de las tablas según tus necesidades
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                image_data BLOB,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def insert_user(self, name):
        # Inserta un usuario en la tabla 'users'
        self.cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
        self.conn.commit()

    def insert_image(self, user_id, image_data):
        # Inserta una imagen en la tabla 'images' asociada a un usuario
        self.cursor.execute('INSERT INTO images (user_id, image_data) VALUES (?, ?)', (user_id, image_data))
        self.conn.commit()

    def close(self):
        self.conn.close()
