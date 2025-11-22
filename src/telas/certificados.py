import customtkinter as ctk
from tkinter import simpledialog
from modules.certificados.certificados import gerar_certificado
import asyncio

class TelaCertificados:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = None
        self.participantes = []
        
    def criar(self):
        self.frame = ctk.CTkFrame(self.parent, corner_radius=0, fg_color="white")
        self.frame.grid(row=0, column=1, sticky="nsew")
        
        titulo = ctk.CTkLabel(
            self.frame,
            text="Certificados",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F2937"
        )
        titulo.pack(padx=30, pady=30)



        btn_emitir = ctk.CTkButton(
            self.frame,
            text = "Emitir Certificados",
            fg_color = "#22C55E",
            hover_color = "#16A34A",
            text_color = "white",
            command = self.emitir_certificados
        )
        btn_emitir.pack(padx=10)
        
        self.combo_eventos = ctk.CTkComboBox(self.frame, values=[], width=300)
        self.combo_eventos.pack(pady=10)
        self.combo_eventos.set("Carregando eventos...")

        btn_individual = ctk.CTkButton(self.frame, text="Gerar Certificado Indidual")
        
        # Adicione aqui a interface de certificados

    def emitir_certificados(self):
        quantidade = simpledialog.askinteger("Quantidade", f"Quantos certificados você deseja emitir:")
        
        if not quantidade:
            return
        
        contador = 0

        while contador < quantidade:
            if contador >= len(self.participantes):
                print("end", "Não há mais partipantes disponíveis.")
                break
        
            nome = self.participantes[contador]
            evento_nome = self.combo_eventos.get()
            evento_id = 1
            data = "2025-11-21"

            asyncio.run(gerar_certificado(participante["id"], evento_id, data))
        
            contador += 1
        
        return self.frame
    
    def destruir(self):
        if self.frame:
            self.frame.destroy()
