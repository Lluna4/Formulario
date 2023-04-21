import customtkinter
import json
import os
import base64
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from customtkinter import filedialog
import docx

uri = ""
plantilla = docx.Document("Plantilla Autoconsumo.docx")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Form"]
FORMAT = "utf-8"
filename = ""
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")
tabview = None
root = customtkinter.CTk()
root.title("Formulario")
label3 = None
label2 = None
comunidades = ["Almeria", "Cadiz", "Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla"]
root.geometry("900x750")

def plant():
    siguente = {"Nombre de la instalación:": False, "TITULAR (Nombre y apellidos):": False, "Emplazamiento:": False, "CP:": False, "Provincia": False, "Municipio:": False}
    print("a")
    for table in plantilla.tables:
        for row in table.rows:
            for cell in row.cells:
                if siguente["Nombre de la instalación:"] == True:
                    cell.text = f"{entryy.get()}"
                    entryy.delete(0, "end")
                    siguente["Nombre de la instalación:"] = False
                elif siguente["TITULAR (Nombre y apellidos):"] == True and "TITULAR (Nombre y apellidos):" not in cell.text:
                    cell.text = f"{entry_nom.get()}"
                    entry_nom.delete(0, "end")
                    siguente["TITULAR (Nombre y apellidos):"] = False
                    continue
                elif "D.N.I." in cell.text:
                    if entry_dni.get() != "":
                        cell.text = f"D.N.I. {entry_dni.get().strip()}"
                        entry_dni.delete(0, "end")
                elif "Teléfono:" in cell.text:
                    if entry_tel.get() != "":
                        cell.text = f"Teléfono: {entry_tel.get().strip()}"
                        entry_tel.delete(0, "end")
                        continue
                elif "e-mail:" in cell.text:
                    cell.text = f"e-mail: {entry_mail.get().strip()}"
                    entry_mail.delete(0, "end")
                elif siguente["Emplazamiento:"] == True and "Emplazamiento:" not in cell.text:
                    if entry_calle.get() != "":
                        cell.text = f"{entry_calle.get().strip()} nº{entry_num.get().strip()}"
                        entry_calle.delete(0, "end")
                        entry_num.delete(0, "end")
                        siguente["Emplazamiento:"] = False
                        continue
                elif siguente["CP:"] == True and "CP:" not in cell.text:
                    if entry_cod.get() != "":
                        cell.text = f"{entry_cod.get().strip()}"
                        entry_cod.delete(0, "end")
                        siguente["CP:"] = False
                        continue
                elif siguente["Provincia"] == True and "Provincia" not in cell.text:
                    if entry_prov.get() != "":
                        cell.text = f"{entry_prov.get().strip()}"
                        siguente["Provincia"] = False
                        continue
                elif siguente["Municipio:"] == True and "Municipio:" not in cell.text:
                    if entry_loc.get() != "":
                        cell.text = f"{entry_loc.get().strip()}"
                        entry_loc.delete(0, "end")
                        siguente["Municipio:"] = False
                        continue
                

                if "Nombre de la instalación:" in cell.text:
                    siguente["Nombre de la instalación:"] = True
                    continue
                elif "TITULAR (Nombre y apellidos):" in cell.text:
                    siguente["TITULAR (Nombre y apellidos):"] = True
                    continue
                elif "Emplazamiento:" in cell.text:
                    siguente["Emplazamiento:"] = True
                    continue
                elif "CP:" in cell.text:
                    siguente["CP:"] = True
                    continue
                elif "Provincia" in cell.text:
                    siguente["Provincia"] = True
                    continue
                elif "Municipio:" in cell.text:
                    siguente["Municipio:"] = True
                    continue



    plantilla.save('Plantilla Autoconsumo.docx')


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

def subir():
    global filename
    filename = filedialog.askopenfilename(title = "Selecciona una imagen", filetype = (("Archivos jpeg","*.jpg"),("Archivos PNG","*.png")))


def tab1():
    global tabview
    label = customtkinter.CTkLabel(tabview.tab("Datos de la instalacion"), text="NOMBRE INSTALACION")
    label.grid(row=0, column=0)
    entryy = customtkinter.CTkEntry(tabview.tab("Datos de la instalacion"), placeholder_text="Nombre de la instalacion", width=300)
    entryy.grid(row=0, column=1, padx=10)

    titular_frame = customtkinter.CTkFrame(tabview.tab("Datos de la instalacion"),width=200 ,height=350, border_width=2)
    titular_frame.grid(row=3, column=0, pady=0, padx=30)

    label_nom = customtkinter.CTkLabel(master=titular_frame, text="Titular (nombre y apellidos)")
    entry_nom = customtkinter.CTkEntry(titular_frame, placeholder_text="Nombre y apellidos", width=180)
    label_nom.grid(row=1, column=0, padx=10, pady=(12, 0))
    entry_nom.grid(row=2, column=0, padx=10, pady=0)
    
    label_dni = customtkinter.CTkLabel(master=titular_frame, text="DNI")
    entry_dni = customtkinter.CTkEntry(titular_frame, placeholder_text="DNI", width=180)
    label_dni.grid(row=3, column=0, padx=10, pady=(12, 0))
    entry_dni.grid(row=4, column=0, padx=10, pady=0)
    
    label_tel = customtkinter.CTkLabel(master=titular_frame, text="Telefono")
    entry_tel = customtkinter.CTkEntry(titular_frame, placeholder_text="Telefono", width=180)
    label_tel.grid(row=5, column=0, padx=10, pady=(12, 0))
    entry_tel.grid(row=6, column=0, padx=10, pady=0)

    label_mail = customtkinter.CTkLabel(master=titular_frame, text="Email")
    entry_mail = customtkinter.CTkEntry(titular_frame, placeholder_text="Email", width=180)
    label_mail.grid(row=7, column=0, padx=10, pady=(12, 0))
    entry_mail.grid(row=8, column=0, padx=10, pady=(0, 12))


    ubi_frame = customtkinter.CTkFrame(tabview.tab("Datos de la instalacion"),width=300 ,height=350, border_width=2)
    ubi_frame.grid(row=3, column=1, pady=30)

    label_calle = customtkinter.CTkLabel(master=ubi_frame, text="Calle")
    entry_calle = customtkinter.CTkEntry(ubi_frame, placeholder_text="Calle", width=180)
    label_calle.grid(row=1, column=0, padx=10, pady=(12, 0))
    entry_calle.grid(row=2, column=0, padx=10, pady=0)

    label_num= customtkinter.CTkLabel(master=ubi_frame, text="Nº")
    entry_num = customtkinter.CTkEntry(ubi_frame, placeholder_text="Nº", width=40)
    label_num.grid(row=1, column=1, padx=10, pady=(12, 0))
    entry_num.grid(row=2, column=1, padx=10, pady=0)
    
    label_loc = customtkinter.CTkLabel(master=ubi_frame, text="Localidad")
    entry_loc = customtkinter.CTkEntry(ubi_frame, placeholder_text="Localidad", width=180)
    label_loc.grid(row=3, column=0, padx=10, pady=(12, 0))
    entry_loc.grid(row=4, column=0, padx=10, pady=0)

    label_cod = customtkinter.CTkLabel(master=ubi_frame, text="C.P")
    entry_cod = customtkinter.CTkEntry(ubi_frame, placeholder_text="C.P", width=60)
    label_cod.grid(row=3, column=1, padx=10, pady=(12, 0))
    entry_cod.grid(row=4, column=1, padx=10, pady=0)
    
    label_prov = customtkinter.CTkLabel(master=ubi_frame, text="Provincia")
    entry_prov = customtkinter.CTkComboBox(ubi_frame, values=comunidades, width=180)
    label_prov.grid(row=5, column=0, padx=10, pady=(12, 0))
    entry_prov.grid(row=6, column=0, padx=10, pady=0)

    label_bot = customtkinter.CTkLabel(master=ubi_frame, text="Imagen")
    entry_bot = customtkinter.CTkButton(ubi_frame, text="Imagen", width=60, command=subir)
    label_bot.grid(row=5, column=1, padx=10, pady=(12, 0))
    entry_bot.grid(row=6, column=1, padx=10, pady=0)

    label_ref = customtkinter.CTkLabel(master=ubi_frame, text="Referencia catastral")
    entry_ref = customtkinter.CTkEntry(ubi_frame, placeholder_text="Referencia catastral", width=180)
    label_ref.grid(row=7, column=0, padx=10, pady=(12, 0))
    entry_ref.grid(row=8, column=0, padx=10, pady=(0, 12))

    label_tipo = customtkinter.CTkLabel(master=tabview.tab("Datos de la instalacion"), text="Tipo de estructura")
    entry_tipo = customtkinter.CTkComboBox(tabview.tab("Datos de la instalacion"), values=["Coplanar", "Inclinada"], width=180)
    label_tipo.grid(row=4, column=0, padx=10, pady=0)
    entry_tipo.grid(row=5, column=0, padx=10, pady=0)

    label_pot= customtkinter.CTkLabel(master=tabview.tab("Datos de la instalacion"), text="Potencia instalada")
    entry_pot = customtkinter.CTkEntry(tabview.tab("Datos de la instalacion"), placeholder_text="Potencia instalada", width=60)
    label_pot.grid(row=4, column=1, padx=10, pady=(12, 0))
    entry_pot.grid(row=5, column=1, padx=10, pady=0)

    label_cons= customtkinter.CTkLabel(master=tabview.tab("Datos de la instalacion"), text="Energia consumida anual estimada en los \nconsumidores asociados a la instalacion de \ngeneracion de autoconsumo (kWh)", font=("Calibri", 10))
    entry_cons = customtkinter.CTkEntry(tabview.tab("Datos de la instalacion"), placeholder_text="KWh", width=60)
    label_cons.grid(row=4, column=2, padx=10, pady=(12, 0))
    entry_cons.grid(row=5, column=2, padx=10, pady=0)

    label_clas = customtkinter.CTkLabel(master=tabview.tab("Datos de la instalacion"), text="Clasificación de la instalacion")
    entry_clas = customtkinter.CTkComboBox(tabview.tab("Datos de la instalacion"), values=["Autoconsumo con excedentes acogido a compensacion", "Autoconsumo aislado"], width=180)
    label_clas.grid(row=6, column=0, padx=10, pady=0)
    entry_clas.grid(row=7, column=0, padx=10, pady=0)

    label_cons= customtkinter.CTkLabel(master=tabview.tab("Datos de la instalacion"), text="Energia generada anual estimada \nde la nueva instalacion (kWh)", font=("Calibri", 10))
    entry_cons = customtkinter.CTkEntry(tabview.tab("Datos de la instalacion"), placeholder_text="KWh", width=60)
    label_cons.grid(row=6, column=2, padx=10, pady=(12, 0))
    entry_cons.grid(row=7, column=2, padx=10, pady=0)

    label_cups = customtkinter.CTkLabel(master=tabview.tab("Datos de la instalacion"), text="CUPS")
    entry_cups = customtkinter.CTkEntry(tabview.tab("Datos de la instalacion"), placeholder_text="CUPS", width=180)
    label_cups.grid(row=8, column=0, padx=10, pady=0)
    entry_cups.grid(row=9, column=0, padx=10, pady=0)

    label_cau = customtkinter.CTkLabel(master=tabview.tab("Datos de la instalacion"), text="CAU")
    entry_cau = customtkinter.CTkEntry(tabview.tab("Datos de la instalacion"), placeholder_text="CAU", width=180)
    label_cau.grid(row=8, column=1, padx=10, pady=0)
    entry_cau.grid(row=9, column=1, padx=10, pady=0)

    sub = customtkinter.CTkButton(root, width=300, height=60, text="REGISTRAR CAMBIOS", font=("Calibri", 30), command=plant)
    sub.pack()
    globals().update(locals())



def tabs():
    global tabview
    frame.destroy()
    tabview = customtkinter.CTkTabview(root)
    tabview.pack(padx=10, pady=10)

    tab_1 = tabview.add("Datos de la instalacion")
    tab_2 = tabview.add("Placas")  
    tab_3 = tabview.add("Inversores")
    tab_4 = tabview.add("Instalador")  
    tab_5 = tabview.add("Esquemas y planos")  
    tab_6 = tabview.add("Certificado de la instalacion")  
    tab1()
    tabview.set("Datos de la instalacion")


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