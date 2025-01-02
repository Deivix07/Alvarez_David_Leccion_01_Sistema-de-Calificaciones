# Importar las librerias necesarias
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Alvarez_David_Leccion_01_Sistema-de-Calificaciones

""" 
Escriba un programa para la gestión de las calificaciones de un grupo de alumnos. 
Los alumnos se caracterizan por: DNI, Apellidos, Nombre, Nota y Calificación, donde Nota 
es la calificación numérica (un número real) dada por el profesor, mientras que la Calificación 
se calculará automáticamente a partir de la nota (siempre que se introduzca o actualice ésta), 
de la siguiente forma: SS si Nota<5, AP si 5≤ Nota<7 NT si 7≤ Nota<9 y SB si Nota≥9. 

Las funciones que ha de realizar el programa son las siguientes: 

1. Mostrar los alumnos con toda su información, de la siguiente forma: DNI APELLIDOS, NOMBRE NOTA CALIFICACIÓN; 33245 García Pérez, Carlos 7,8 NT; 128676 Romero Rodríguez, Luisa 9 SB; 
2. Introducir alumno, donde se pide DNI, apellidos, nombre y nota del alumno. No pueden existir dos alumnos con el mismo DNI. 
3. Eliminar alumno a partir del DNI. 
4. Consultar la nota y la calificación de un alumno a partir del DNI 
5. Modificar la nota de un alumno a partir del DNI. 
6. Mostrar alumnos suspensos 
7. Mostrar alumnos aprobados 
8. Mostrar candidatos a MH (los que tengan un 10 de nota) 
9. Modificar calificación: permite modificar la calificación calculada automáticamente
"""

class Sistema_calif: # Inicializar la clase para la app
    def __init__(self, root):
        self.root = root               # Configuración de la ventana principal
        self.root.title("Gestión de Calificaciones")
        
        # Conexión a la base de datos SQLite
        self.conn = sqlite3.connect("calificaciones.db")
        self.cursor = self.conn.cursor()
        self.crear_tabla()      # Crear tabla si no existe
 
        self.create_widgets()       # Crear la interfaz gráfica

    def crear_tabla(self):       # Método que crea las tablas
        """Crea la tabla de alumnos si no existe"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            dni TEXT PRIMARY KEY,
            apellidos TEXT,
            nombre TEXT,
            nota REAL,
            calificacion TEXT
        )
        """)
        self.conn.commit()

    def create_widgets(self):      # Crea los widgets de la interfaz gráfica y el treeview
        # Título
        self.texto = tk.Label(self.root, text="Gestión de Calificaciones de Alumnos")
        self.texto.grid(row=0, column=0, columnspan=4, pady=10)

        # Treeview para mostrar los alumnos
        self.tree = ttk.Treeview(self.root, columns=("DNI", "Apellidos", "Nombre", "Nota", "Calificación"), show="headings", height=8)
        self.tree.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        # Estilo del Treeview
        style = ttk.Style()
        style.configure("Treeview",
                        font=("Arial", 10),
                        rowheight=18) 
        style.configure("Treeview.Heading",
                        font=("Arial",10, "bold"))

        # Definir las columnas
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Nota", text="Nota")
        self.tree.heading("Calificación", text="Calificación")

        # Ajustar de las columnas
        self.tree.column("DNI", width=100, anchor="center")    
        self.tree.column("Apellidos", width=120, anchor="w")    
        self.tree.column("Nombre", width=120, anchor="w")      
        self.tree.column("Nota", width=60, anchor="center")    
        self.tree.column("Calificación", width=90, anchor="center") 

        # Botones para la acciones
        self.añadir_btn = tk.Button(self.root, text="Añadir Alumno", command=self.añadir_alumno)
        self.añadir_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=5)
        
        self.modificar_btn = tk.Button(self.root, text="Modificar Nota", command=self.modificar_nota)
        self.modificar_btn.grid(row=2, column=1, columnspan=2, padx=20, pady=5)
        
        self.mostrar_btn = tk.Button(self.root, text="Mostrar Alumnos", command=self.mostrar_alumnos)
        self.mostrar_btn.grid(row=3, column=0, padx=5, pady=5)

        self.eliminar_btn = tk.Button(self.root, text="Eliminar Alumno", command=self.eliminar_alumno)
        self.eliminar_btn.grid(row=3, column=1, padx=5, pady=5)

        self.consultar_btn = tk.Button(self.root, text="Consultar Alumno", command=self.consultar_alumno)
        self.consultar_btn.grid(row=3, column=2, padx=5, pady=5)

        self.suspensos_btn = tk.Button(self.root, text="Mostrar Suspensos", command=self.mostrar_suspensos)
        self.suspensos_btn.grid(row=4, column=0, padx=5, pady=5)

        self.aprobados_btn = tk.Button(self.root, text="Mostrar Aprobados", command=self.mostrar_aprobados)
        self.aprobados_btn.grid(row=4, column=1, padx=5, pady=5)

        self.mh_btn = tk.Button(self.root, text="Mostrar Candidatos a MH", command=self.mostrar_mh)
        self.mh_btn.grid(row=4, column=2, padx=5, pady=5)

    # Muestra los alumnos en el Treeview cargados desde la base de datos
    def mostrar_alumnos(self):

        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Consultar alumnos de la base de datos
        self.cursor.execute("SELECT * FROM alumnos")
        alumnos = self.cursor.fetchall()
         
        # Insertar alumnos en el Treeview
        for alumno in alumnos:
            self.tree.insert("", "end", values=alumno)

    # Introducir un nuevo alumno y lo guarda en la base de datos
    def añadir_alumno(self):
        def guardar_alumno():   # Función para guardar el alumno
            dni = entry_dni.get()
            if self.dni_existe(dni):
                messagebox.showerror("Error", "El DNI ya está registrado")
                return
            apellidos = entry_apellidos.get()
            nombre = entry_nombre.get()
            try:
                nota = float(entry_nota.get())
                if not (0 <= nota <= 10):
                    messagebox.showerror("Error", "La nota debe estar entre 0 y 10")
                    return
            except ValueError:
                messagebox.showerror("Error", "La nota debe ser un número válido")
                return
            calificacion = self.calcular_calificacion(nota)

             # Guardar alumno en la base de datos
            self.cursor.execute("INSERT INTO alumnos (dni, apellidos, nombre, nota, calificacion) VALUES (?, ?, ?, ?, ?)",
                                (dni, apellidos, nombre, nota, calificacion))
            self.conn.commit()
            ventana_nuevo_alumno.destroy()
            self.mostrar_alumnos()
            messagebox.showinfo("Éxito", "Alumno registrado con éxito")

        # Crear ventana para introducir alumno
        ventana_nuevo_alumno = tk.Toplevel(self.root)
        ventana_nuevo_alumno.title("Introducir Alumno")
        ventana_nuevo_alumno.geometry("250x300")

        # Campos de para los datos
        tk.Label(ventana_nuevo_alumno, text="DNI").pack(pady=5)
        entry_dni = tk.Entry(ventana_nuevo_alumno)
        entry_dni.pack(pady=5)

        tk.Label(ventana_nuevo_alumno, text="Apellidos").pack(pady=5)
        entry_apellidos = tk.Entry(ventana_nuevo_alumno)
        entry_apellidos.pack(pady=5)

        tk.Label(ventana_nuevo_alumno, text="Nombre").pack(pady=5)
        entry_nombre = tk.Entry(ventana_nuevo_alumno)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_nuevo_alumno, text="Nota").pack(pady=5)
        entry_nota = tk.Entry(ventana_nuevo_alumno)
        entry_nota.pack(pady=5)

        tk.Button(ventana_nuevo_alumno, text="Guardar", command=guardar_alumno).pack(pady=10)

    # Método eliminar un alumno por su DNI
    def eliminar_alumno(self):
        def eliminar():
            dni = entry_dni.get()
            if self.dni_existe(dni):
                self.cursor.execute("DELETE FROM alumnos WHERE dni=?", (dni,))
                self.conn.commit()
                ventana_eliminar.destroy()
                self.mostrar_alumnos()
                messagebox.showinfo("Éxito", f"Alumno con DNI {dni} eliminado")
            else:
                messagebox.showerror("Error", "No existe un alumno con ese DNI")
        
        # Ventana para eliminar alumno
        ventana_eliminar = tk.Toplevel(self.root)
        ventana_eliminar.title("Eliminar Alumno")
        ventana_eliminar.geometry("250x130")
        
        # Campos para el entry
        tk.Label(ventana_eliminar, text="DNI del Alumno a Eliminar").pack(pady=5)
        entry_dni = tk.Entry(ventana_eliminar)
        entry_dni.pack(pady=5)

        tk.Button(ventana_eliminar, text="Eliminar", command=eliminar).pack(pady=10)

    # Consultar los datos de un alumno por su DNI
    def consultar_alumno(self):
        def consultar():           # Consultar el alumno en la base de datos
            dni = entry_dni.get()
            if self.dni_existe(dni):
                self.cursor.execute("SELECT * FROM alumnos WHERE dni=?", (dni,))
                alumno = self.cursor.fetchone()
                messagebox.showinfo("Consulta", f"DNI: {alumno[0]}\n"
                                               f"Apellidos: {alumno[1]}\n"
                                               f"Nombre: {alumno[2]}\n"
                                               f"Nota: {alumno[3]}\n"
                                               f"Calificación: {alumno[4]}")
                ventana_consultar.destroy()
            else:
                messagebox.showerror("Error", "No existe un alumno con ese DNI")

        # Ventana para eliminar alumno
        ventana_consultar = tk.Toplevel(self.root)
        ventana_consultar.title("Consultar Alumno")
        ventana_consultar.geometry("250x130")

        # Capos para los datos
        tk.Label(ventana_consultar, text="DNI del Alumno a Consultar").pack(pady=5)
        entry_dni = tk.Entry(ventana_consultar)
        entry_dni.pack(pady=5)

        tk.Button(ventana_consultar, text="Consultar", command=consultar).pack(pady=10)

    # Método modificar nota
    def modificar_nota(self):
        def modificar():          # Modifica la nota en la base de datos
            dni = entry_dni.get()
            if self.dni_existe(dni):
                try:
                    nueva_nota = float(entry_nota.get())
                    if not (0 <= nueva_nota <= 10):
                        messagebox.showerror("Error", "La nota debe estar entre 0 y 10")
                        return
                except ValueError:
                    messagebox.showerror("Error", "La nota debe ser un número válido")
                    return
                calificacion = self.calcular_calificacion(nueva_nota)
                self.cursor.execute("UPDATE alumnos SET nota=?, calificacion=? WHERE dni=?", (nueva_nota, calificacion, dni))
                self.conn.commit()
                ventana_modificar.destroy()
                self.mostrar_alumnos()
                messagebox.showinfo("Éxito", f"Nota de {dni} modificada a {nueva_nota}")
            else:
                messagebox.showerror("Error", "No existe un alumno con ese DNI")

        # Ventana para modificar nota
        ventana_modificar = tk.Toplevel(self.root)
        ventana_modificar.title("Modificar Nota")
        ventana_modificar.geometry("250x200")

        # Campos para rellenar los datos
        tk.Label(ventana_modificar, text="DNI del Alumno a Modificar").pack(pady=5)
        entry_dni = tk.Entry(ventana_modificar)
        entry_dni.pack(pady=5)

        tk.Label(ventana_modificar, text="Nueva Nota").pack(pady=5)
        entry_nota = tk.Entry(ventana_modificar)
        entry_nota.pack(pady=5)

        tk.Button(ventana_modificar, text="Modificar", command=modificar).pack(pady=10)

    # Métodos para mostras los alumnos según el requerimiento
    
    def mostrar_suspensos(self):
        """Muestra a los alumnos suspensos"""
        self.mostrar_filtrados("SELECT * FROM alumnos WHERE nota < 5")

    def mostrar_aprobados(self):
        """Muestra a los alumnos aprobados"""
        self.mostrar_filtrados("SELECT * FROM alumnos WHERE nota >= 5")

    def mostrar_mh(self):
        """Muestra a los alumnos con nota 10"""
        self.mostrar_filtrados("SELECT * FROM alumnos WHERE nota = 10")

    def mostrar_filtrados(self, query):
        """Muestra los alumnos según una consulta SQL"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        self.cursor.execute(query)
        alumnos = self.cursor.fetchall()

        for alumno in alumnos:
            self.tree.insert("", "end", values=alumno)

    # Comprueba si un alumno con el DNI ya existe en la base de datos
    def dni_existe(self, dni):
        self.cursor.execute("SELECT 1 FROM alumnos WHERE dni=?", (dni,))
        return self.cursor.fetchone() is not None

    # Calcula la calificación según la nota
    def calcular_calificacion(self, nota):
        if nota < 5:
            return "SS"
        elif 5 <= nota < 7:
            return "AP"
        elif 7 <= nota < 9:
            return "NT"
        elif nota >= 9:
            return "SB"

    #Cierra la base de datos
    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = Sistema_calif(root)
    root.mainloop()