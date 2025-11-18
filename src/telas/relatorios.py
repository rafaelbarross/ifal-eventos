import customtkinter as ctk

class TelaRelatorios:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = None
        
    def criar(self):
        self.frame = ctk.CTkFrame(self.parent, corner_radius=0, fg_color="white")
        self.frame.grid(row=0, column=1, sticky="nsew")
        
        titulo = ctk.CTkLabel(
            self.frame,
            text="Relatórios",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F2937"
        )
        titulo.pack(padx=30, pady=30)
        
        # Adicione aqui a interface de relatórios
        
        return self.frame
    
    def destruir(self):
        if self.frame:
            self.frame.destroy()
