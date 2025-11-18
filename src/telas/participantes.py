import customtkinter as ctk
from tkinter import messagebox
import asyncio
import sys
import os

# Adicionar o diretório modules ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from modules.participante.participante import ParticipanteManager


def executar_async(coro):
    """Executa uma coroutine de forma segura, criando um novo loop se necessário"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)


class TelaParticipantes:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = None
        self.participante_manager = ParticipanteManager()
        self.participante_selecionado_id = None
        
    def criar(self):
        self.frame = ctk.CTkFrame(self.parent, corner_radius=0, fg_color="white")
        self.frame.grid(row=0, column=1, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        
        # Título
        titulo = ctk.CTkLabel(
            self.frame,
            text="Gerenciamento de Participantes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F2937"
        )
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 5))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            self.frame,
            text="Adicione, busque e edite os participantes do evento.",
            font=ctk.CTkFont(size=14),
            text_color="#6B7280"
        )
        subtitulo.grid(row=1, column=0, columnspan=2, sticky="w", padx=30, pady=(0, 20))
        
        # Container com 2 colunas
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=30, pady=(0, 20))
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        # --- COLUNA ESQUERDA: Cadastrar Novo Participante ---
        frame_cadastro = ctk.CTkFrame(container, fg_color="#F9FAFB", corner_radius=10)
        frame_cadastro.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        frame_cadastro.grid_propagate(False)
        frame_cadastro.configure(width=280)
        
        label_cadastro = ctk.CTkLabel(
            frame_cadastro,
            text="Cadastrar Novo\nParticipante",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1F2937"
        )
        label_cadastro.pack(padx=80, pady=(20, 15), anchor="w")
        
        # Nome Completo
        ctk.CTkLabel(frame_cadastro, text="Nome Completo", text_color="#374151", font=ctk.CTkFont(size=12)).pack(padx=20, pady=(5, 2), anchor="w")
        self.entry_nome = ctk.CTkEntry(frame_cadastro, placeholder_text="e.g. Maria da Silva", height=35)
        self.entry_nome.pack(padx=20, pady=(0, 10), fill="x")
        
        # CPF
        ctk.CTkLabel(frame_cadastro, text="CPF", text_color="#374151", font=ctk.CTkFont(size=12)).pack(padx=20, pady=(5, 2), anchor="w")
        self.entry_cpf = ctk.CTkEntry(frame_cadastro, placeholder_text="000.000.000-00", height=35)
        self.entry_cpf.pack(padx=20, pady=(0, 10), fill="x")
        
        # Email
        ctk.CTkLabel(frame_cadastro, text="Email", text_color="#374151", font=ctk.CTkFont(size=12)).pack(padx=20, pady=(5, 2), anchor="w")
        self.entry_email = ctk.CTkEntry(frame_cadastro, placeholder_text="e.g. maria.silva@email.com", height=35)
        self.entry_email.pack(padx=20, pady=(0, 10), fill="x")
        
        # Curso
        ctk.CTkLabel(frame_cadastro, text="Curso", text_color="#374151", font=ctk.CTkFont(size=12)).pack(padx=20, pady=(5, 2), anchor="w")
        self.entry_curso = ctk.CTkEntry(frame_cadastro, placeholder_text="e.g. Ciência da Computação", height=35)
        self.entry_curso.pack(padx=20, pady=(0, 10), fill="x")
        
        # Turma
        ctk.CTkLabel(frame_cadastro, text="Turma", text_color="#374151", font=ctk.CTkFont(size=12)).pack(padx=20, pady=(5, 2), anchor="w")
        self.entry_turma = ctk.CTkEntry(frame_cadastro, placeholder_text="e.g. 2024.1", height=35)
        self.entry_turma.pack(padx=20, pady=(0, 15), fill="x")
        
        # Botões
        frame_botoes = ctk.CTkFrame(frame_cadastro, fg_color="transparent")
        frame_botoes.pack(padx=20, pady=(10, 20), fill="x")
        
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar Participante",
            command=self.salvar_participante,
            fg_color="#22C55E",
            hover_color="#16A34A",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_salvar.pack(fill="x", pady=(0, 5))
        
        btn_limpar = ctk.CTkButton(
            frame_botoes,
            text="Limpar",
            command=self.limpar_formulario,
            fg_color="white",
            text_color="#374151",
            border_width=1,
            border_color="#D1D5DB",
            hover_color="#F3F4F6",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        btn_limpar.pack(fill="x")
        
        # --- COLUNA DIREITA: Lista de Inscritos ---
        frame_lista = ctk.CTkFrame(container, fg_color="#F9FAFB", corner_radius=10)
        frame_lista.grid(row=0, column=1, sticky="nsew")
        
        # Cabeçalho da lista
        frame_header_lista = ctk.CTkFrame(frame_lista, fg_color="transparent")
        frame_header_lista.pack(fill="x", padx=20, pady=(20, 15))
        
        label_lista = ctk.CTkLabel(
            frame_header_lista,
            text="Lista de Inscritos",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1F2937"
        )
        label_lista.pack(side="left")
        
        # Campo de busca
        frame_busca = ctk.CTkFrame(frame_header_lista, fg_color="white", corner_radius=5, border_width=1, border_color="#D1D5DB")
        frame_busca.pack(side="right")
        
        self.entry_busca = ctk.CTkEntry(
            frame_busca,
            placeholder_text="Buscar por CPF",
            width=180,
            height=30,
            border_width=0,
            fg_color="white"
        )
        self.entry_busca.pack(side="left", padx=8)
        self.entry_busca.bind('<Return>', lambda e: self.buscar_por_cpf())
        
        # Cabeçalho da tabela
        frame_table_header = ctk.CTkFrame(frame_lista, fg_color="#E5E7EB", height=40)
        frame_table_header.pack(fill="x", padx=20, pady=(0, 5))
        frame_table_header.pack_propagate(False)
        
        headers_config = [
            ("NOME", 0.25),
            ("CPF", 0.20),
            ("EMAIL", 0.30),
            ("CURSO", 0.15),
            ("AÇÕES", 0.10)
        ]
        
        for texto, peso in headers_config:
            lbl = ctk.CTkLabel(
                frame_table_header,
                text=texto,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#374151"
            )
            lbl.pack(side="left", expand=True, fill="both", padx=10)
        
        # Scrollable frame para participantes
        self.scroll_participantes = ctk.CTkScrollableFrame(frame_lista, fg_color="white", corner_radius=5)
        self.scroll_participantes.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Carregar participantes do banco
        self.carregar_participantes()
        
        # Paginação
        frame_paginacao = ctk.CTkFrame(frame_lista, fg_color="transparent", height=40)
        frame_paginacao.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            frame_paginacao,
            text="Mostrando 1-4 de 20 resultados",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        ).pack(side="left")
        
        frame_btns_paginacao = ctk.CTkFrame(frame_paginacao, fg_color="transparent")
        frame_btns_paginacao.pack(side="right")
        
        ctk.CTkButton(
            frame_btns_paginacao,
            text="Anterior",
            width=80,
            height=30,
            fg_color="white",
            text_color="#374151",
            border_width=1,
            border_color="#D1D5DB",
            hover_color="#F3F4F6",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            frame_btns_paginacao,
            text="Próximo",
            width=80,
            height=30,
            fg_color="white",
            text_color="#374151",
            border_width=1,
            border_color="#D1D5DB",
            hover_color="#F3F4F6",
            font=ctk.CTkFont(size=12)
        ).pack(side="left")
        
        return self.frame
    
    def carregar_participantes(self):
        """Carrega participantes do banco de dados"""
        try:
            participantes = executar_async(self.participante_manager.listar_participantes())
            
            # Limpar lista atual
            for widget in self.scroll_participantes.winfo_children():
                widget.destroy()
            
            # Adicionar participantes
            if participantes:
                for participante in participantes:
                    self.adicionar_participante_lista(participante)
            else:
                label_vazio = ctk.CTkLabel(
                    self.scroll_participantes,
                    text="Nenhum participante cadastrado ainda.",
                    text_color="#9CA3AF",
                    font=ctk.CTkFont(size=14)
                )
                label_vazio.pack(pady=40)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar participantes: {str(e)}")
    
    def buscar_por_cpf(self):
        """Busca participante por CPF"""
        cpf = self.entry_busca.get().strip()
        
        if not cpf:
            self.carregar_participantes()
            return
        
        try:
            participante = executar_async(self.participante_manager.buscar_participante_por_cpf(cpf))
            
            # Limpar lista atual
            for widget in self.scroll_participantes.winfo_children():
                widget.destroy()
            
            if participante:
                self.adicionar_participante_lista(participante)
            else:
                label_vazio = ctk.CTkLabel(
                    self.scroll_participantes,
                    text=f"Nenhum participante encontrado com CPF '{cpf}'.",
                    text_color="#9CA3AF",
                    font=ctk.CTkFont(size=14)
                )
                label_vazio.pack(pady=40)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar participante: {str(e)}")
    
    def adicionar_participante_lista(self, participante_data):
        frame_participante = ctk.CTkFrame(self.scroll_participantes, fg_color="white", height=50)
        frame_participante.pack(fill="x", pady=2)
        frame_participante.pack_propagate(False)
        
        participante_id = participante_data['id']
        nome = participante_data['nome']
        cpf = participante_data['cpf']
        email = participante_data['email']
        curso = participante_data['curso']
        
        # Nome
        ctk.CTkLabel(frame_participante, text=nome, text_color="#1F2937", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # CPF
        ctk.CTkLabel(frame_participante, text=cpf, text_color="#6B7280", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # Email
        ctk.CTkLabel(frame_participante, text=email, text_color="#6B7280", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # Curso
        ctk.CTkLabel(frame_participante, text=curso, text_color="#6B7280", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # Ações
        frame_acoes = ctk.CTkFrame(frame_participante, fg_color="transparent")
        frame_acoes.pack(side="left", expand=True, padx=10)
        
        btn_editar = ctk.CTkButton(
            frame_acoes, 
            text="Editar", 
            width=60, 
            height=25, 
            fg_color="transparent", 
            text_color="#22C55E", 
            hover_color="#F0FDF4", 
            cursor="hand2",
            command=lambda: self.editar_participante(participante_id)
        )
        btn_editar.pack(side="left", padx=2)
        
        btn_excluir = ctk.CTkButton(
            frame_acoes, 
            text="Excluir", 
            width=60, 
            height=25, 
            fg_color="transparent", 
            text_color="#EF4444", 
            hover_color="#FEE2E2", 
            cursor="hand2",
            command=lambda: self.excluir_participante(participante_id)
        )
        btn_excluir.pack(side="left", padx=2)
    
    def salvar_participante(self):
        """Salva ou atualiza um participante"""
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        email = self.entry_email.get().strip()
        curso = self.entry_curso.get().strip()
        turma = self.entry_turma.get().strip()
        
        # Validações
        if not all([nome, cpf, email, curso, turma]):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        
        try:
            # Salvar ou atualizar
            if self.participante_selecionado_id:
                # Atualizar participante existente
                executar_async(self.participante_manager.atualizar_participante(
                    participante_id=self.participante_selecionado_id,
                    nome=nome,
                    cpf=cpf,
                    email=email,
                    curso=curso,
                    turma=turma
                ))
                messagebox.showinfo("Sucesso", f"Participante '{nome}' atualizado com sucesso!")
                self.participante_selecionado_id = None
            else:
                # Criar novo participante
                executar_async(self.participante_manager.criar_participante(
                    nome=nome,
                    cpf=cpf,
                    email=email,
                    curso=curso,
                    turma=turma
                ))
                messagebox.showinfo("Sucesso", f"Participante '{nome}' cadastrado com sucesso!")
            
            self.limpar_formulario()
            self.carregar_participantes()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar participante: {str(e)}")
    
    def editar_participante(self, participante_id):
        """Carrega dados do participante para edição"""
        try:
            participante = executar_async(self.participante_manager.buscar_participante_por_id(participante_id))
            
            if participante:
                self.participante_selecionado_id = participante_id
                
                # Preencher formulário
                self.entry_nome.delete(0, 'end')
                self.entry_nome.insert(0, participante['nome'])
                
                self.entry_cpf.delete(0, 'end')
                self.entry_cpf.insert(0, participante['cpf'])
                
                self.entry_email.delete(0, 'end')
                self.entry_email.insert(0, participante['email'])
                
                self.entry_curso.delete(0, 'end')
                self.entry_curso.insert(0, participante['curso'])
                
                self.entry_turma.delete(0, 'end')
                self.entry_turma.insert(0, participante['turma'])
                
                messagebox.showinfo("Editar", f"Editando participante: {participante['nome']}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar participante: {str(e)}")
    
    def excluir_participante(self, participante_id):
        """Exclui um participante"""
        try:
            participante = executar_async(self.participante_manager.buscar_participante_por_id(participante_id))
            
            if participante:
                if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o participante '{participante['nome']}'?\n\nIsso também excluirá todas as inscrições relacionadas."):
                    sucesso = executar_async(self.participante_manager.deletar_participante(participante_id))
                    
                    if sucesso:
                        messagebox.showinfo("Sucesso", "Participante excluído com sucesso!")
                        self.carregar_participantes()
                    else:
                        messagebox.showerror("Erro", "Não foi possível excluir o participante.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir participante: {str(e)}")
    
    def limpar_formulario(self):
        """Limpa o formulário"""
        self.participante_selecionado_id = None
        self.entry_nome.delete(0, 'end')
        self.entry_cpf.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_curso.delete(0, 'end')
        self.entry_turma.delete(0, 'end')
    
    def destruir(self):
        """Destroi a tela e desconecta do banco"""
        try:
            executar_async(self.participante_manager.desconectar())
        except:
            pass
        
        if self.frame:
            self.frame.destroy()
