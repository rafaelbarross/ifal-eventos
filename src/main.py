import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import asyncio
from prisma import Prisma

# Importar telas
# from telas.dashboard import TelaDashboard
from telas.eventos import TelaEventos
from telas.participantes import TelaParticipantes
from telas.inscricoes import TelaInscricoes
from telas.relatorios import TelaRelatorios
# from telas.configuracoes import TelaConfiguracoes

# Importar utilitários
from utils.icons import obter_icone

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Gerenciamento de Eventos - IFAL")
        self.geometry("1400x800")
        
        # Tema e cores
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        # Cores personalizadas do IFAL
        self.cor_sidebar = "#F0F9F4"  # Verde claro
        self.cor_verde_ifal = "#22C55E"  # Verde principal do IFAL
        self.cor_verde_escuro = "#16A34A"  # Verde hover
        self.cor_verde_claro = "#86EFAC"  # Verde claro
        self.cor_vermelho = "#EF4444"
        
        # Layout em grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Criar sidebar
        self.criar_sidebar()
        
        # Gerenciador de telas
        self.tela_atual = None
        
        # Mostrar tela inicial
        self.mostrar_eventos()
        
    def criar_sidebar(self):
        # Frame lateral
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=self.cor_sidebar)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        self.sidebar.grid_propagate(False)
        
        # Informações do usuário
        self.frame_usuario = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.frame_usuario.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="ew")
        
        self.label_usuario = ctk.CTkLabel(
            self.frame_usuario,
            text="Organizador",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1F2937"
        )
        self.label_usuario.pack(anchor="w")
        
        self.label_email = ctk.CTkLabel(
            self.frame_usuario,
            text="organizador@edu.com",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        )
        self.label_email.pack(anchor="w")
        
        # # Botões do menu
        # self.btn_dashboard = ctk.CTkButton(
        #     self.sidebar,
        #     text=f"{obter_icone('dashboard')}  Dashboard",
        #     command=self.mostrar_dashboard,
        #     fg_color="transparent",
        #     text_color="#1F2937",
        #     hover_color="#E5E7EB",
        #     anchor="w",
        #     height=40,
        #     # font=ctk.CTkFont(size=14)
        #     width=190
        # )
        # self.btn_dashboard.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        
        self.btn_eventos = ctk.CTkButton(
            self.sidebar,
            text="Eventos",
            command=self.mostrar_eventos,
            fg_color="#22C55E",
            text_color="white",
            hover_color="#16A34A",
            anchor="w",
            height=40,
            width=190,
            font=ctk.CTkFont(size=14)
        )
        self.btn_eventos.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        
        self.btn_participantes = ctk.CTkButton(
            self.sidebar,
            text="Participantes",
            command=self.mostrar_participantes,
            fg_color="transparent",
            text_color="#1F2937",
            hover_color="#E5E7EB",
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_participantes.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        
        self.btn_inscricoes = ctk.CTkButton(
            self.sidebar,
            text="Inscrições",
            command=self.mostrar_inscricoes,
            fg_color="transparent",
            text_color="#1F2937",
            hover_color="#E5E7EB",
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_inscricoes.grid(row=4, column=0, padx=15, pady=5, sticky="ew")
        
        self.btn_relatorios = ctk.CTkButton(
            self.sidebar,
            text="Relatórios",
            command=self.mostrar_relatorios,
            fg_color="transparent",
            text_color="#1F2937",
            hover_color="#E5E7EB",
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_relatorios.grid(row=5, column=0, padx=15, pady=5, sticky="ew")
        
        # # Botões inferiores
        # self.btn_config = ctk.CTkButton(
        #     self.sidebar,
        #     text=f"{obter_icone('gear')}  Configurações",
        #     command=self.mostrar_config,
        #     fg_color="transparent",
        #     text_color="#1F2937",
        #     hover_color="#E5E7EB",
        #     anchor="w",
        #     height=40,
        #     font=ctk.CTkFont(size=14)
        # )
        # self.btn_config.grid(row=7, column=0, padx=15, pady=5, sticky="ew")
        
        self.btn_sair = ctk.CTkButton(
            self.sidebar,
            text="Sair",
            command=self.sair,
            fg_color="transparent",
            text_color="#EF4444",
            hover_color="#FEE2E2",
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_sair.grid(row=8, column=0, padx=15, pady=(5, 20), sticky="ew")
    
    def atualizar_botao_ativo(self, botao_ativo):
        """Atualiza o visual do botão ativo no menu"""
        botoes = [
            # self.btn_dashboard,
            self.btn_eventos,
            self.btn_participantes,
            self.btn_inscricoes,
            self.btn_relatorios
        ]
        
        for btn in botoes:
            if btn == botao_ativo:
                btn.configure(fg_color="#22C55E", text_color="white", hover_color="#16A34A")
            else:
                btn.configure(fg_color="transparent", text_color="#1F2937", hover_color="#E5E7EB")
    
    def limpar_tela_atual(self):
        if self.tela_atual:
            self.tela_atual.destruir()
            self.tela_atual = None
    
    # def mostrar_dashboard(self):
    #     self.limpar_tela_atual()
    #     self.atualizar_botao_ativo(self.btn_dashboard)
    #     self.tela_atual = TelaDashboard(self, self)
    #     self.tela_atual.criar()
    
    def mostrar_eventos(self):
        self.limpar_tela_atual()
        self.atualizar_botao_ativo(self.btn_eventos)
        self.tela_atual = TelaEventos(self, self)
        self.tela_atual.criar()
    
    def mostrar_participantes(self):
        self.limpar_tela_atual()
        self.atualizar_botao_ativo(self.btn_participantes)
        self.tela_atual = TelaParticipantes(self, self)
        self.tela_atual.criar()
    
    def mostrar_inscricoes(self):
        self.limpar_tela_atual()
        self.atualizar_botao_ativo(self.btn_inscricoes)
        self.tela_atual = TelaInscricoes(self, self)
        self.tela_atual.criar()
    
    def mostrar_relatorios(self):
        self.limpar_tela_atual()
        self.atualizar_botao_ativo(self.btn_relatorios)
        self.tela_atual = TelaRelatorios(self, self)
        self.tela_atual.criar()
    
    # def mostrar_config(self):
    #     self.limpar_tela_atual()
    #     self.tela_atual = TelaConfiguracoes(self, self)
    #     self.tela_atual.criar()
    
    def sair(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.quit()


if __name__ == "__main__":
    app = App()
    app.mainloop()