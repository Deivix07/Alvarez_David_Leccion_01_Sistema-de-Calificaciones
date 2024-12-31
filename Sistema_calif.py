import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class GestionCalificacionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Calificaciones")
        
        # Conexión a la base de datos SQLite
        self.conn = sqlite3.connect("calificaciones.db")
        self.cursor = self.conn.cursor()
        self.crear_tabla()

        # Crear la interfaz gráfica
        self.create_widgets()

    def crear_tabla(self):
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

    def create_widgets(self):
        # Título
        self.texto = tk.Label(self.root, text="Gestión de Calificaciones de Alumnos")
        self.texto.grid(row=0, column=0, columnspan=4, pady=10)

        # Treeview para mostrar los alumnos
        self.tree = ttk.Treeview(self.root, columns=("DNI", "Apellidos", "Nombre", "Nota", "Calificación"), show="headings", height=8)
        self.tree.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        # Estilo compacto para el Treeview
        style = ttk.Style()
        style.configure("Treeview",
                        font=("Arial", 8),  # Fuente más pequeña
                        rowheight=18)      # Altura de fila más baja
        style.configure("Treeview.Heading",
                        font=("Arial", 9, "bold"))  # Fuente de los encabezados

        # Definir las columnas
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Nota", text="Nota")
        self.tree.heading("Calificación", text="Calificación")

        # Ajustar la visualización de las columnas
        self.tree.column("DNI", width=70, anchor="center")       # Ancho reducido de la columna DNI
        self.tree.column("Apellidos", width=120, anchor="w")     # Ancho reducido de Apellidos
        self.tree.column("Nombre", width=120, anchor="w")        # Ancho reducido de Nombre
        self.tree.column("Nota", width=50, anchor="center")      # Ancho reducido de la columna Nota
        self.tree.column("Calificación", width=80, anchor="center")  # Ancho reducido de Calificación

        # Botones organizados con grid
        
        self.introducir_btn = tk.Button(self.root, text="Introducir Alumno", command=self.introducir_alumno)
        self.introducir_btn.grid(row=2, columnspan=4, padx=5, pady=5)
        
        self.mostrar_btn = tk.Button(self.root, text="Mostrar Alumnos", command=self.mostrar_alumnos)
        self.mostrar_btn.grid(row=3, column=0, padx=5, pady=5)

        self.eliminar_btn = tk.Button(self.root, text="Eliminar Alumno", command=self.eliminar_alumno)
        self.eliminar_btn.grid(row=3, column=1, padx=5, pady=5)

        self.consultar_btn = tk.Button(self.root, text="Consultar Alumno", command=self.consultar_alumno)
        self.consultar_btn.grid(row=3, column=2, padx=5, pady=5)

        self.modificar_btn = tk.Button(self.root, text="Modificar Nota", command=self.modificar_nota)
        self.modificar_btn.grid(row=3, column=3, padx=5, pady=5)

        self.suspensos_btn = tk.Button(self.root, text="Mostrar Suspensos", command=self.mostrar_suspensos)
        self.suspensos_btn.grid(row=4, column=0, padx=5, pady=5)

        self.aprobados_btn = tk.Button(self.root, text="Mostrar Aprobados", command=self.mostrar_aprobados)
        self.aprobados_btn.grid(row=4, column=1, padx=5, pady=5)

        self.mh_btn = tk.Button(self.root, text="Mostrar Candidatos a MH", command=self.mostrar_mh)
        self.mh_btn.grid(row=4, column=2, padx=5, pady=5)

    def mostrar_alumnos(self):
        """Muestra todos los alumnos desde la base de datos"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        self.cursor.execute("SELECT * FROM alumnos")
        alumnos = self.cursor.fetchall()

        for alumno in alumnos:
            self.tree.insert("", "end", values=alumno)

    def introducir_alumno(self):
        """Introduce un nuevo alumno en la base de datos"""
        def guardar_alumno():
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

            self.cursor.execute("INSERT INTO alumnos (dni, apellidos, nombre, nota, calificacion) VALUES (?, ?, ?, ?, ?)",
                                (dni, apellidos, nombre, nota, calificacion))
            self.conn.commit()
            ventana_nuevo_alumno.destroy()
            self.mostrar_alumnos()
            messagebox.showinfo("Éxito", "Alumno registrado con éxito")

        ventana_nuevo_alumno = tk.Toplevel(self.root)
        ventana_nuevo_alumno.title("Introducir Alumno")

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

    def eliminar_alumno(self):
        """Elimina un alumno de la base de datos por su DNI"""
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

        ventana_eliminar = tk.Toplevel(self.root)
        ventana_eliminar.title("Eliminar Alumno")

        tk.Label(ventana_eliminar, text="DNI del Alumno a Eliminar").pack(pady=5)
        entry_dni = tk.Entry(ventana_eliminar)
        entry_dni.pack(pady=5)

        tk.Button(ventana_eliminar, text="Eliminar", command=eliminar).pack(pady=10)

    def consultar_alumno(self):
        """Consulta los datos de un alumno a partir de su DNI"""
        def consultar():
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

        ventana_consultar = tk.Toplevel(self.root)
        ventana_consultar.title("Consultar Alumno")

        tk.Label(ventana_consultar, text="DNI del Alumno a Consultar").pack(pady=5)
        entry_dni = tk.Entry(ventana_consultar)
        entry_dni.pack(pady=5)

        tk.Button(ventana_consultar, text="Consultar", command=consultar).pack(pady=10)

    def modificar_nota(self):
        """Modifica la nota de un alumno en la base de datos"""
        def modificar():
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

        ventana_modificar = tk.Toplevel(self.root)
        ventana_modificar.title("Modificar Nota")

        tk.Label(ventana_modificar, text="DNI del Alumno a Modificar").pack(pady=5)
        entry_dni = tk.Entry(ventana_modificar)
        entry_dni.pack(pady=5)

        tk.Label(ventana_modificar, text="Nueva Nota").pack(pady=5)
        entry_nota = tk.Entry(ventana_modificar)
        entry_nota.pack(pady=5)

        tk.Button(ventana_modificar, text="Modificar", command=modificar).pack(pady=10)

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

    def dni_existe(self, dni):
        """Comprueba si un alumno con el DNI existe en la base de datos"""
        self.cursor.execute("SELECT 1 FROM alumnos WHERE dni=?", (dni,))
        return self.cursor.fetchone() is not None

    def calcular_calificacion(self, nota):
        """Calcula la calificación según la nota"""
        if nota < 5:
            return "SS"
        elif 5 <= nota < 7:
            return "AP"
        elif 7 <= nota < 9:
            return "NT"
        elif nota >= 9:
            return "SB"

    def __del__(self):
        """Cierra la conexión a la base de datos cuando se cierre la aplicación"""
        self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = GestionCalificacionesApp(root)
    root.mainloop()
