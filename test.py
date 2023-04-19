import customtkinter
import json
import os
import base64
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = ""

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Form"]
FORMAT = "utf-8"

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.title("Formulario")
label3 = None
label2 = None
root.geometry("600x450")

def login():
    global label3
    col = db["login"]
    usuario = col.find_one({"nombre": entry.get()})
    if usuario:
        print("a")
        if usuario["contraseña"].decode('utf-8') == entry2.get():
            if checkbox.get() == 1:
                with open("save.json", "w") as a:
                    json.dump({"usuario": entry.get(), "contra":base64.b64encode(entry2.get().encode(FORMAT)).decode("utf-8")}, a)
            else:
                if os.path.exists("save.json"):
                    os.remove("save.json")
            tabs()
            return
        else:
            entry.delete(0, "end")
            entry2.delete(0, "end")
            if label3:
                label3.configure(require_redraw=True, text="La contraseña es incorrecta")
            else:
                label3 = customtkinter.CTkLabel(master=frame, text="La contraseña es incorrecta", text_color=("red", "red"))
                label3.pack(pady=12, padx=10)
    else:
        print("b")
        entry.delete(0, "end")
        entry2.delete(0, "end")
        if label3:
            label3.configure(require_redraw=True, text="El usuario es incorrecto")
        else:
            label3 = customtkinter.CTkLabel(master=frame, text="El usuario es incorrecto", text_color=("red", "red"))
            label3.pack(pady=12, padx=10)



def tabs():
    frame.destroy()
    tabview = customtkinter.CTkTabview(root)
    tabview.pack(padx=20, pady=20)

    tab_1 = tabview.add("tab 1")
    tab_2 = tabview.add("tab 2")  
    tabview.set("tab 1")


def crear_cuenta():
    global label2
    col = db["login"]
    usuario = entry.get()
    if not usuario:
        if label2:
            label2.configure(require_redraw=True, text="El usuario es incorrecto")
        else:
            label2 = customtkinter.CTkLabel(master=frame, text="El usuario es incorrecto", text_color=("red", "red"))
            label2.pack(pady=12, padx=10)
        return
    usuario = col.find_one({"nombre": usuario})
    if usuario:
        entry.delete(0, "end")
        entry2.delete(0, "end")
        if label2:
            label2.configure(require_redraw=True, text="El usuario ya existe")
        else:
            label2 = customtkinter.CTkLabel(master=frame, text="El usuario ya existe", text_color=("red", "red"))
            label2.pack(pady=12, padx=10)
        return
    datos = {"nombre": entry.get(), "contraseña": entry2.get().encode(FORMAT)}
    col.insert_one(datos)
    tabs()



def registro():
    label.configure(require_redraw=True, text="Registro")
    button.configure(require_redraw=True, text="Crear cuenta", command=crear_cuenta)
    if label3:
        label3.destroy()
    registro.destroy()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login", font=("Calibri", 24))
label.pack(pady=12, padx=10)

entry = customtkinter.CTkEntry(master=frame, placeholder_text="Usuario")
entry.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Contraseña", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Enviar", command=login)
button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Recuerdame")
checkbox.pack(pady=12, padx=10)

registro = customtkinter.CTkButton(master=frame, text="Registrarse", command=registro)
registro.pack(pady=12, padx=10)

if os.path.exists("save.json"):
    with open("save.json", "r") as f:
        credentials = json.load(f)
    entry.insert(0, credentials["usuario"])
    entry2.insert(0, base64.b64decode(credentials["contra"]).decode(FORMAT))

root.mainloop()