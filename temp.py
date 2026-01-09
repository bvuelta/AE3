import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Contraseñas")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        
        # Variables para almacenar datos
        self.password_length = tk.StringVar()
        self.uppercase_count = tk.StringVar()
        self.special_count = tk.StringVar()
        self.digit_count = tk.StringVar()
        self.save_filename = tk.StringVar()
        self.load_filename = tk.StringVar(value="passwords.txt")
        
        # Variable para almacenar la contraseña generada
        self.current_password = None
        
        # Variable para mostrar contraseña recuperada
        self.recovered_password = tk.StringVar()
        
        # Crear interfaz
        self.create_widgets()
    
    def create_widgets(self):
        """Crea todos los elementos de la interfaz gráfica"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Generador de Contraseñas",
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Campos de entrada
        labels = [
            ("Longitud de la contraseña:", self.password_length),
            ("Cantidad de mayúsculas:", self.uppercase_count),
            ("Cantidad de especiales:", self.special_count),
            ("Cantidad de dígitos:", self.digit_count),
            ("Archivo para guardar:", self.save_filename),
            ("Archivo para recuperar:", self.load_filename)
        ]
        
        for i, (label_text, variable) in enumerate(labels, start=1):
            # Etiqueta
            label = tk.Label(
                main_frame,
                text=label_text,
                font=("Arial", 10),
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", pady=5)
            
            # Campo de entrada
            entry = tk.Entry(
                main_frame,
                textvariable=variable,
                font=("Arial", 10),
                width=25
            )
            entry.grid(row=i, column=1, pady=5, padx=(10, 0))
        
        # Frame para botones
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        # Botones en dos filas
        buttons_row1 = [
            ("Generar Contraseña", self.generate_password),
            ("Guardar Contraseña en Fichero", self.save_password)
        ]
        
        for i, (text, command) in enumerate(buttons_row1):
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 10),
                width=20,
                height=1
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
        
        buttons_row2 = [
            ("Recuperar Contraseña", self.load_password),
            ("Borrar Campos", self.clear_fields)
        ]
        
        for i, (text, command) in enumerate(buttons_row2):
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 10),
                width=20,
                height=1
            )
            btn.grid(row=1, column=i, padx=5, pady=5)
        
        # Área para mostrar contraseña recuperada
        recovered_frame = tk.Frame(main_frame)
        recovered_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
        
        recovered_label = tk.Label(
            recovered_frame,
            text="Contraseña recuperada:",
            font=("Arial", 10)
        )
        recovered_label.pack(side="left")
        
        # Campo para mostrar la contraseña recuperada (similar a la imagen)
        recovered_display = tk.Entry(
            recovered_frame,
            textvariable=self.recovered_password,
            font=("Courier", 10, "bold"),
            width=20,
            state="readonly",
            readonlybackground="#f0f0f0"
        )
        recovered_display.pack(side="left", padx=(5, 0))
    
    def validate_inputs(self):
        """Valida los datos ingresados por el usuario"""
        try:
            # Verificar que todos los campos tengan valores numéricos
            length = int(self.password_length.get())
            uppercase = int(self.uppercase_count.get())
            special = int(self.special_count.get())
            digits = int(self.digit_count.get())
            
            # Verificar que los valores no sean negativos
            if length < 0 or uppercase < 0 or special < 0 or digits < 0:
                raise ValueError("Los valores no pueden ser negativos")
            
            # Verificar que la suma de componentes no exceda la longitud total
            total_components = uppercase + special + digits
            if total_components > length:
                raise ValueError(f"La suma de componentes ({total_components}) excede la longitud total ({length})")
            
            # Verificar longitud mínima
            if length < 4:
                raise ValueError("La longitud mínima debe ser de 4 caracteres")
            
            return length, uppercase, special, digits
            
        except ValueError as e:
            if "invalid literal" in str(e):
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
            else:
                messagebox.showerror("Error", str(e))
            return None
    
    def generate_password(self):
        """Genera una contraseña aleatoria basada en los parámetros especificados"""
        # Validar entradas
        params = self.validate_inputs()
        if params is None:
            return
        
        length, uppercase, special, digits = params
        
        # Calcular cantidad de letras minúsculas
        lowercase = length - (uppercase + special + digits)
        
        # Definir conjuntos de caracteres
        uppercase_chars = string.ascii_uppercase
        lowercase_chars = string.ascii_lowercase
        digit_chars = string.digits
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Inicializar lista para la contraseña
        password_chars = []
        
        # Agregar caracteres según las cantidades especificadas
        password_chars.extend(random.choices(uppercase_chars, k=uppercase))
        password_chars.extend(random.choices(special_chars, k=special))
        password_chars.extend(random.choices(digit_chars, k=digits))
        password_chars.extend(random.choices(lowercase_chars, k=lowercase))
        
        # Mezclar los caracteres para aleatorizar el orden
        random.shuffle(password_chars)
        
        # Convertir a string
        self.current_password = ''.join(password_chars)
        
        # Mostrar la contraseña generada en un mensaje
        messagebox.showinfo("Contraseña Generada", 
                           f"Contraseña generada:\n{self.current_password}")
        filename = self.save_filename.get().strip()

        if not filename:
            filename = "passwords.txt"
            self.save_filename.set(filename)

        if not os.path.exists(filename):
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(self.current_password)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el archivo:\n{str(e)}")
    
    def save_password(self):
        """Guarda la contraseña generada en un archivo"""
        # Verificar que haya una contraseña generada
        if self.current_password is None:
            messagebox.showwarning(
                "Error", 
                "No se ha podido realizar la operación.\nMotivo: Actualmente no hay ninguna contraseña que guardar."
            )
            return
        
        # Obtener nombre de archivo
        filename = self.save_filename.get().strip()
        
        if not filename:
            filename = "passwords.txt"
            self.save_filename.set(filename)
        
        try:
            # Guardar la contraseña en el archivo
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.current_password)
            
            messagebox.showinfo("Éxito", f"Contraseña guardada en: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la contraseña:\n{str(e)}")
    
    def load_password(self):
        """Recupera una contraseña desde un archivo"""
        # Obtener nombre de archivo
        filename = self.load_filename.get().strip()
        
        if not filename:
            filename = "passwords.txt"
            self.load_filename.set(filename)
        
        try:
            # Verificar si el archivo existe
            if not os.path.exists(filename):
                messagebox.showerror("Error", f"No se encontró el archivo: {filename}")
                return
            
            # Leer la contraseña del archivo
            with open(filename, 'r', encoding='utf-8') as file:
                password = file.read().strip()
            
            # Mostrar la contraseña recuperada
            self.recovered_password.set(password)
            
            # Ejemplo de la imagen: mostrar "7Ydo?Easdf!"
            # Para propósitos de demostración, si el archivo está vacío, mostrar el ejemplo
            if not password:
                self.recovered_password.set("7Ydo?Easdf!")
                messagebox.showinfo("Demo", "Mostrando contraseña de ejemplo (el archivo estaba vacío)")
            else:
                messagebox.showinfo("Éxito", f"Contraseña recuperada de: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo recuperar la contraseña:\n{str(e)}")
    
    def clear_fields(self):
        """Borra todos los campos de texto"""
        self.password_length.set("")
        self.uppercase_count.set("")
        self.special_count.set("")
        self.digit_count.set("")
        self.save_filename.set("")
        self.recovered_password.set("")
        self.current_password = None
        
        # Mantener el valor predeterminado para recuperar
        self.load_filename.set("passwords.txt")

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":

    main()
