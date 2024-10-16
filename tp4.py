import mysql.connector
from getpass import getpass  ## para que no sea visible la pass en consola al escribirla
import sys  ## para poder cerrar la terminal de PY

from tp4functions import (
    main_menu,
    read_users_ui_unique,
    update_password
)  ## me traigo las funciones que necesito de " tp4functions.py "

config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "tp4_bd",
}


class Database:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def connect():
        return mysql.connector.connect(**config)

    @staticmethod
    def create(table, **kwargs):
        conn = Database.connect()
        cursor = conn.cursor()
        columns = ", ".join(kwargs.keys())
        values = tuple(kwargs.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({', '.join(['%s'] * len(values))})"
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update(table, any_id, **kwargs):
        conn = Database.connect()
        cursor = conn.cursor()
        columns = " = %s, ".join(kwargs.keys()) + " = %s"
        values = tuple(kwargs.values())
        query = f"UPDATE {table} SET {columns} WHERE id = %s"
        cursor.execute(query, values + (any_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_user_role(user_id):
        conn = Database.connect()
        cursor = conn.cursor()
        query = "SELECT rol FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def read_by_email(email):
        conn = Database.connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result


## Manejo de usuario
def login_user_ui():
    print("--- Login ---")
    email = input("Enter email: ")
    user = Database.read_by_email(email)

    if user:
        if user[7] == 2:  # columna status == blocked
            print("Blocked account.")
            sys.exit()

        password = getpass("Enter password: ")
        if user[3] == password:
            print("Login successful.")
            role = Database.get_user_role(user[0])
            if role:
                if role == "Administrador":
                    print("You have administrator credentials")
                    admin_actions()
                elif role == "Empleado":
                    user_actions(user)
                else:
                    print("Unknown role.")
            else:
                print("Role not found.")
        else:
            print("Invalid credentials.")
            sys.exit()
    else:
        print("User not found.")
        sys.exit()


## ROL ADMIN
def admin_actions():
    main_menu()  # llamamos al main menu del otro archivo que tiene todas las operaciones CRUD que pide el tp


## ROL EMPLEADO
def user_actions(user):
    user_management_employee(user)


def user_management_employee(user):
    print("\n--- User Employee ---")
    print("1. Personal Info")
    print("2. Change Password")
    print("3. Exit")

    choice = input("Select an option (1-3): ")

    if choice == "1":
        read_users_ui_unique(user)
        user_management_employee(user)
    elif choice == "3":
        print("Closing terminal...")
        sys.exit()

    elif choice == "2":
        update_password(user[0])
        user_management_employee(user)
    else:
        print("Invalid choice, please try again.")
        user_management_employee(user)


# Es para que se ejecute solo este codigo, ya que importe las funciones del otro archivo
if __name__ == "__main__":

    login_user_ui()
