import os
import tkinter as tk 
from tkinter import messagebox, filedialog
from connection import Client

class GUI:
    def window_client(self):
        self.root = tk.Tk()
        self.root.title("Client")
        self.client = Client()

        self.ip_field_label = tk.Label(self.root, text = "IP Field")
        self.ip_field_label.pack(padx=10, pady=10)
        self.ip_field_entry = tk.Entry(self.root, width=20)
        self.ip_field_entry.pack(padx=10, pady=10)

        self.send_file = tk.Button(self.root, text="Send File", command=self.enviar_archivo)
        self.send_file.pack(padx=10, pady=10)
        
        self.directory = tk.Button(self.root, text="Send Directory", command=self.enviar_directorio)
        self.directory.pack(padx=10, pady=10)
        self.root.mainloop()

    def enviar_archivo(self):
        archivo = filedialog.askopenfilename()
        ip = self.ip_field_entry.get()
        if archivo and ip:
            try:
                nombre_archivo = os.path.abspath(archivo)
                self.client.start_client(ip, nombre_archivo)
                messagebox.showinfo("Success", f"{os.path.basename(nombre_archivo)} has been sent succesfully")
            except Exception as err:
                messagebox.showerror("Error", "Error when sending the file check IP address and conectivity")
                print(err)
            
    def enviar_directorio(self):
        directory = filedialog.askdirectory()
        ip = self.ip_field_entry.get()
        if directory and ip:
            try:
                nombre_directorio = os.path.abspath(directory)
                self.client.start_client(ip, nombre_directorio)
                messagebox.showinfo("Success", f"{os.path.basename(nombre_directorio)} has been sent succesfully")
            except Exception as err:
                messagebox.showerror("Error", "Error when sending the file check IP address and conectivity")
                print(err)
    
    def __init__(self):
        self.window_client()