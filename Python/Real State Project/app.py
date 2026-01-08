# Author: Andrea Lobo
# Date: 06/10/2025
# Description: Developed a Python-based real estate property management application 
# using Tkinter and SQLite that tracks property status, supports editing and deletion, 
# and maintains a detailed history log of all modifications with timestamps.

# In the future I plan on making this available in other languages. 


import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Conectar o crear la base de datos
conn = sqlite3.connect("propiedades.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS propiedades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        direccion TEXT NOT NULL,
        estado TEXT NOT NULL
    )
""")

# Crear tabla de historial si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        propiedad_id INTEGER,
        direccion_anterior TEXT,
        estado_anterior TEXT,
        direccion_nueva TEXT,
        estado_nuevo TEXT,
        fecha TEXT
    )
""")

#Crear tabla de inquilinos si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inquilinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        propiedad_id INTEGER,
        nombre TEXT,
        telefono TEXT,
        fecha_ingreso TEXT,
        renta_mensual REAL,
        banco TEXT,
        cuenta TEXT,
        fecha_pago TEXT,
        atrasado TEXT,
        FOREIGN KEY(propiedad_id) REFERENCES propiedades(id)
    )
""")

conn.commit()

# Función para agregar propiedad
def agregar_propiedad():
    direccion = entrada_direccion.get()
    estado = estado_var.get()

    if direccion == "":
        messagebox.showwarning("Campo vacío", "La dirección no puede estar vacía.")
        return
    
    # Insertar la propiedad
    cursor.execute("INSERT INTO propiedades (direccion, estado) VALUES (?,?)", (direccion, estado))
    conn.commit()

    # Obtener el ID recién creado
    propiedad_id = cursor.lastrowid

    #if estado.lower() == "ocupada":
        #abrir_formulario_inquilino(propiedad_id)
    #else:
        #mostrar_propiedades()

    entrada_direccion.delete(0, tk.END) 

    #cursor.execute("INSERT INTO propiedades (direccion, estado) VALUES (?, ?)", (direccion, estado))
    #conn.commit()
    entrada_direccion.delete(0, tk.END)
    mostrar_propiedades()

# Función para mostrar propiedades
def mostrar_propiedades():
    lista_propiedades.delete(0, tk.END)
    cursor.execute("SELECT direccion, estado FROM propiedades")
    for propiedad in cursor.fetchall():
        lista_propiedades.insert(tk.END, f"{propiedad[0]} - {propiedad[1]}")
    
# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Gestión de Propiedades")
ventana.geometry("400x400")

tk.Label(ventana, text="Dirección:").pack()
entrada_direccion = tk.Entry(ventana, width=50)
entrada_direccion.pack()

tk.Label(ventana, text="Estado:").pack()
estado_var = tk.StringVar(value="libre")
tk.OptionMenu(ventana, estado_var, "Libre", "Ocupada", "En Reparacion", "En Matenimiento").pack()

tk.Button(ventana, text="Agregar Propiedad", command=agregar_propiedad).pack(pady=10)

tk.Label(ventana, text="Lista de propiedades registradas:").pack()
lista_propiedades = tk.Listbox(ventana, width=50)
lista_propiedades.pack(pady=5)

def eliminar_propiedad():
    seleccion = lista_propiedades.curselection()
    if seleccion:
        texto = lista_propiedades.get(seleccion[0])
        direccion, estado = texto.split(" - ")

        cursor.execute("SELECT id FROM propiedades WHERE direccion = ? AND estado = ?", (direccion, estado))
        resultado = cursor.fetchone()

        if resultado:
            propiedad_id = resultado[0]
            cursor.execute("DELETE FROM  propiedades WHERE id = ?", (propiedad_id,))
            conn.commit()
            print(f"Propiedad eliminada con ID {propiedad_id}")
            mostrar_propiedades() # Actualizar la lista en pantalla
        else:
            print("Propiedad no encontrada en la base de datos.")
    else:
        print("No hay nada seleccionado.")

def editar_propiedad():
    seleccion = lista_propiedades.curselection()
    if not seleccion:
        return
    
    texto = lista_propiedades.get(seleccion[0])
    direccion_actual, estado_actual = texto.split(" - ")

    cursor.execute("SELECT id FROM propiedades WHERE direccion = ? AND estado = ?", (direccion_actual, estado_actual))
    resultado = cursor.fetchone()

    if not resultado:
        print("No se encontró la propiedad en la base de datos.")
        return
    
    propiedad_id = resultado[0]

    ventana_editar = tk.Toplevel(ventana)
    ventana_editar.title("Editar Propiedad")
    ventana_editar.geometry("300x200")

    tk.Label(ventana_editar, text = "Dirección: ").pack()
    entrada_direccion = tk.Entry(ventana_editar)
    entrada_direccion.insert(0, direccion_actual)
    entrada_direccion.pack()

    tk.Label(ventana_editar, text = "Estado: ").pack()
    estado_var = tk.StringVar(value = estado_actual)
    tk.OptionMenu(ventana_editar, estado_var, "Libre", "Ocupada", "En Reparación", "En Mantenimiento"). pack()

    def guardar_cambios():
        nueva_direccion = entrada_direccion.get()
        nuevo_estado = estado_var.get()

        #Actualizar propiedad en base de datos
        cursor.execute("""
            UPDATE propiedades
            SET direccion = ?, estado = ?
            WHERE id = ?
        """, (nueva_direccion, nuevo_estado, propiedad_id))
        conn.commit()    # Confirma la actualización principal

        #Guardar en historial
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO historial (
                propiedad_id,
                direccion_anterior,
                estado_anterior,
                direccion_nueva,
                estado_nuevo,
                fecha
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            propiedad_id,
            direccion_actual,
            estado_actual,
            nueva_direccion,
            nuevo_estado,
            fecha_actual
        ))
        conn.commit()   # Confirmamos que también el registro en historial

        print("Cambios guardados y registrados en historial")
        ventana_editar.destroy() # Cierra la ventana de edición
        mostrar_propiedades()    # Refresca la lista

    tk.Button(
        ventana_editar,
        text = "Guardar cambios",
        command = guardar_cambios
    ).pack(pady = 10)

def ver_historial():
    seleccion = lista_propiedades.curselection()
    if not seleccion:
        return
    
    texto = lista_propiedades.get(seleccion[0])
    direccion, estado = texto.split(" - ")

    cursor.execute("SELECT id FROM propiedades WHERE direccion = ? AND estado = ?", (direccion, estado))
    resultado = cursor.fetchone()

    if resultado:
        propiedad_id = resultado[0]

        ventana_historial = tk.Toplevel(ventana)
        ventana_historial.title("Historial de cambios")
        ventana_historial.geometry("500x300")

        lista = tk.Listbox(ventana_historial, width = 80)
        lista.pack(pady = 10)

        cursor.execute("""
            SELECT direccion_anterior, estado_anterior,
                    direccion_nueva, estado_nuevo, fecha
            FROM historial
            WHERE propiedad_id = ?
            ORDER BY fecha DESC      
        """, (propiedad_id,))
        historial = cursor.fetchall()

        if historial:
            for registro in historial:
                texto = f"{registro[4]} | {registro[0]} ({registro[1]}) -> {registro[2]} ({registro[3]})"
                lista.insert(tk.END, texto)
        else:
            lista.insert(tk.END, "No hay historial registrado para esta propiedad.")

# Menú contextual
menu_contextual = tk.Menu(ventana, tearoff = 0)
menu_contextual.add_command(label = "Editar", command = editar_propiedad)
menu_contextual.add_command(label = "Eliminar", command = eliminar_propiedad)
menu_contextual.add_command(label = "Ver Historial", command = ver_historial)

# Función para mostrar menú al hacer clic derecho
def mostrar_menu(event):
    try:
        lista_propiedades.selection_clear(0, tk.END) # Hace limpieza de la selección hecha
        lista_propiedades.selection_set(lista_propiedades.nearest(event.y)) #Selecciona donde se hizo clic
        menu_contextual.tk_popup(event.x_root, event.y_root)
    finally:
        menu_contextual.grab_release()

# Enlaza el clic derecho al listbox
lista_propiedades.bind("<Button-3>", mostrar_menu) # <Button-3> es botón derecho en Windows

mostrar_propiedades()

ventana.mainloop()