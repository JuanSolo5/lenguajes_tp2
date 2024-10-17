from getpass import getpass  # para que no sea visible la pass en consola al escribirla
import sys
import random
import string

from model import Database
#color de los logs (instalar colorama en la terminal)
#pip install colorama
from colorama import Fore, Style, init
# Inicializar colorama
init(autoreset=True)



# Función principal del menú
def main_menu():
    print("\n--- Administrator Main Menu ---")
    print("1. User Management")
    print("2. Store Management")
    print("3. Exit")
    choice = input("Select an option (1-3): ")

    if choice == "1":
        user_management()
    elif choice == "2":
        store_management()
    elif choice == "3":
        print("Exiting program...")
        sys.exit()
    else:
        print("Invalid choice, please try again.")
        main_menu()

def user_management():
    print("\n--- User Management ---")
    print("1. Create User")
    print("2. Read Users")
    print("3. Update User")
    print("4. Delete User")
    print("5. Back to Main Menu")
    choice = input("Select an option (1-5): ")

    if choice == "1":
        create_user_ui()
    elif choice == "2":
        read_users_ui()
    elif choice == "3":
        update_user_ui()
    elif choice == "4":
        delete_user_ui()
    elif choice == "5":
        main_menu()
    else:
        print("Invalid choice, please try again.")
        user_management()


def store_management():
    print("\n--- Store Management ---")
    print("1. Create Store")
    print("2. Read Stores")
    print("3. Update Store")
    print("4. Delete Store")
    print("5. Back to Main Menu")
    choice = input("Select an option (1-5): ")

    if choice == "1":
        create_store_ui()
    elif choice == "2":
        read_stores_ui()
    elif choice == "3":
        update_store_ui()
    elif choice == "4":
        delete_store_ui()
    elif choice == "5":
        main_menu()
    else:
        print("Invalid choice, please try again.")
        store_management()


## Creamos funcion para poder elegir un rol :
def select_role():
    print("Seleccionar rol:")
    print("1. Administrador")
    print("2. Empleado")

    choice = input("Ingresa el número de tu elección (1 o 2): ")

    if choice == "1":
        return "Administrador"
    elif choice == "2":
        return "Empleado"
    else:
        print("Elija una opcion valida")
        select_role()


def select_status():
    print("Select status:")
    print("1. Activo")
    print("2. Bloqueado")

    choice = input("Select an option 1-2: ")

    if choice == "1":
        return 1
    elif choice == "2":
        return 2
    else:
        print("Choose a valid option")
        select_status()


def create_user_ui():
    name = input("Enter name: ")
    email = input("Enter email: ")
    password = generate_password()
    role = select_role()
    telephone = input("Enter telephone: ")
    address = input("Enter address: ")
    status = 1  # inicializa en activo

    store_id = input("Enter store ID: ")
    store = Database.read_by_id("stores", store_id)
    if not store:
        print(f"Error: The store with ID {store_id} does not exist.")
        user_management()
        return

    Database.create("users", name=name, email=email, password=password, rol=role, telephone=telephone, address=address, status=status, store_id=store_id)
    print("User created successfully.")
    user_management()

def read_users_ui():
    users = Database.read("users")
    for user in users:
        log_print_user(user)
    user_management()


def log_print_user(user):

    status_texto = ""
    if user[7] == 1:
        status_texto = "ACTIVE"
    elif user[7] == 2:
        status_texto = "BLOCKED"
    log = (
        f"{Fore.GREEN}ID:{Fore.RESET} {user[0]}, "
        f"{Fore.GREEN}Name:{Fore.RESET} {user[1]}, "
        f"{Fore.GREEN}Email:{Fore.RESET} {user[2]}, "
        f"{Fore.GREEN}Password:{Fore.RESET} {user[3]}, "
        f"{Fore.GREEN}Role:{Fore.RESET} {user[4]}, "
        f"{Fore.GREEN}Tel:{Fore.RESET} {user[5]}, "
        f"{Fore.GREEN}Address:{Fore.RESET} {user[6]}, "
        f"{Fore.GREEN}Status:{Fore.RESET} {status_texto}, "
        f"{Fore.GREEN}StoreID:{Fore.RESET} {user[8]}"
    )
    print(log)


def read_users_ui():
    users = Database.read("users")
    for user in users:
        log_print_user(user)
    user_management()


def read_users_ui_unique(user):  # la modifique para que el empleado no vea la pw ni datos internos de la bd
    print(f"{Fore.GREEN}Name:{Fore.RESET} {user[1]}, ")
    print(f"{Fore.GREEN}Email:{Fore.RESET} {user[2]}, ")
    print(f"{Fore.GREEN}Tel:{Fore.RESET} {user[5]}, ")
    print(f"{Fore.GREEN}Address:{Fore.RESET} {user[6]}, ")
    store = Database.read_by_id("stores", user[8])
    if store:
        print(f"{Fore.GREEN}Store: {Fore.RESET} {store[1]}")


def update_user_ui():
    user_id = input("Enter user ID to update: ")

    user = Database.read_by_id("users", user_id)

    if not user:
        print("User not found.")
        user_management()
        return
    (
        current_name,
        current_email,
        current_password,
        current_rol,
        current_telephone,
        current_address,
        current_status,
        current_store_id,
    ) = user[1:]

    name = (
        input(f"Enter new name (or press Enter to keep current: {current_name}): ")
        or current_name
    )

    email = (
        input(f"Enter new email (or press Enter to keep current: {current_email}): ")
        or current_email
    )

    password = (
        input(f"Enter new password (or press Enter to keep current): ")
        or current_password
    )

    rol = select_role()

    telephone = (
        input(
            f"Enter new telephone (or press Enter to keep current: {current_telephone}): "
        )
        or current_telephone
    )

    address = (
        input(
            f"Enter new address (or press Enter to keep current: {current_address}): "
        )
        or current_address
    )

    status = select_status()

    store_id = (
        input(f"Enter new store (or press Enter to keep current: {current_store_id}): ")
        or current_store_id
    )

    Database.update(
        "users",
        user_id,
        name=name,
        email=email,
        password=password,
        rol=rol,
        telephone=telephone,
        address=address,
        status=status,
        store_id=store_id,
    )
    print("User updated successfully.")
    user_management()


def update_password(user_id):

    user = Database.read_by_id("users", user_id)
    if not user:
        print("User not found.")
        user_management()
        return

    current_password = user[3]  # El password es el cuarto elemento

    password = input("Enter new password (or press Enter to keep current): ") or current_password

    Database.update("users", user_id, password=password)

    print("Password updated successfully.")

    #user_management()


def delete_user_ui():
    user_id = input("Enter user ID to delete: ")
    Database.delete("users", user_id)
    print("User deleted successfully.")
    user_management()


def create_store_ui():
    name = input("Enter store name: ")
    address = input("Enter store address: ")

    Database.create("stores", name=name, address=address)
    print("Store created successfully.")
    store_management()


def log_print_store(store):

    log = (
        f"{Fore.GREEN}ID:{Fore.RESET} {store[0]}, "
        f"{Fore.GREEN}Name:{Fore.RESET} {store[1]}, "
        f"{Fore.GREEN}Address:{Fore.RESET} {store[2]}, "
    )
    print(log)


def read_stores_ui():
    stores = Database.read("stores")
    for store in stores:
        log_print_store(store)
    store_management()


def update_store_ui():
    store_id = input("Enter store ID to update: ")

    store = Database.read_by_id("stores", store_id)
    if not store:
        print("Store not found.")
        store_management()
        return

    current_name = store[1]
    current_address = store[2]

    name = (
        input(f"Enter new name (or press Enter to keep current: {current_name}): ")
        or current_name
    )
    address = (
        input(
            f"Enter new address (or press Enter to keep current: {current_address}): "
        )
        or current_address
    )

    Database.update("stores", store_id, name=name, address=address)
    print("Store updated successfully.")
    store_management()


def delete_store_ui():
    store_id = input("Enter store ID to delete: ")
    Database.delete("stores", store_id)
    print("Store deleted successfully.")
    store_management()


def generate_password():
    password_chars = [  # para que tenga al menos una letra y un digito
        random.choice(string.ascii_letters),
        random.choice(string.digits)
    ]

    characters = string.ascii_letters + string.digits
    password_chars += random.choices(characters, k=6)  # agregamos otros 6 caracteres random

    random.shuffle(password_chars)

    password = ''.join(password_chars)
    return password


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




## Es para que se ejecute solo este codigo, ya que importe las funciones del otro archivo
if __name__ == "__main__":
    login_user_ui()
