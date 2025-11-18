import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import asyncio
import sys
import os

# Adicionar o diretório modules ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from modules.evento.evento import EventoManager


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

class TelaEventos:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = None
        self.evento_manager = EventoManager()
        self.evento_selecionado_id = None
        
    def criar(self):
        # Frame principal
        self.frame = ctk.CTkFrame(self.parent, corner_radius=0, fg_color="white")
        self.frame.grid(row=0, column=1, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        # Título
        titulo = ctk.CTkLabel(
            self.frame,
            text="Gerenciamento de Eventos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F2937"
        )
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 30))
        
        # Container com 2 colunas
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=30, pady=(0, 20))
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        # --- COLUNA ESQUERDA: Cadastrar Novo Evento ---
        frame_cadastro = ctk.CTkFrame(container, fg_color="#F9FAFB", corner_radius=10)
        frame_cadastro.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        frame_cadastro.grid_propagate(False)
        frame_cadastro.configure(width=400)
        
        label_cadastro = ctk.CTkLabel(
            frame_cadastro,
            text="Cadastrar Novo Evento",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1F2937"
        )
        label_cadastro.pack(padx=20, pady=(20, 15), anchor="w")
        
        # Nome do Evento
        ctk.CTkLabel(frame_cadastro, text="Nome do Evento", text_color="#374151", font=ctk.CTkFont(size=12)).pack(padx=20, pady=(5, 2), anchor="w")
        self.entry_nome_evento = ctk.CTkEntry(frame_cadastro, placeholder_text="Ex: Semana de Inovação e Tecn", height=35)
        self.entry_nome_evento.pack(padx=20, pady=(0, 10), fill="x")
        
        # Data e Vagas
        frame_data_vagas = ctk.CTkFrame(frame_cadastro, fg_color="transparent")
        frame_data_vagas.pack(padx=20, pady=(0, 10), fill="x")
        frame_data_vagas.grid_columnconfigure((0, 1), weight=1)
        
        frame_data = ctk.CTkFrame(frame_data_vagas, fg_color="transparent")
        frame_data.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkLabel(frame_data, text="Data", text_color="#374151", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.entry_data = ctk.CTkEntry(frame_data, placeholder_text="10/25/2024", height=35)
        self.entry_data.pack(fill="x")
        
        frame_vagas = ctk.CTkFrame(frame_data_vagas, fg_color="transparent")
        frame_vagas.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ctk.CTkLabel(frame_vagas, text="Vagas", text_color="#374151", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.entry_vagas = ctk.CTkEntry(frame_vagas, placeholder_text="100", height=35)
        self.entry_vagas.pack(fill="x")
        
        # Horário e Local
        frame_horario_local = ctk.CTkFrame(frame_cadastro, fg_color="transparent")
        frame_horario_local.pack(padx=20, pady=(0, 10), fill="x")
        frame_horario_local.grid_columnconfigure((0, 1), weight=1)
        
        frame_horario = ctk.CTkFrame(frame_horario_local, fg_color="transparent")
        frame_horario.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkLabel(frame_horario, text="Horário", text_color="#374151", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.entry_horario = ctk.CTkEntry(frame_horario, placeholder_text="14:00", height=35)
        self.entry_horario.pack(fill="x")
        
        frame_local = ctk.CTkFrame(frame_horario_local, fg_color="transparent")
        frame_local.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ctk.CTkLabel(frame_local, text="Local", text_color="#374151", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.entry_local = ctk.CTkEntry(frame_local, placeholder_text="Auditório", height=35)
        self.entry_local.pack(fill="x")
        
        # Descrição
        ctk.CTkLabel(frame_cadastro, text="Descrição", text_color="#374151", font=ctk.CTkFont(size=12)).pack(padx=20, pady=(5, 2), anchor="w")
        self.entry_descricao = ctk.CTkEntry(frame_cadastro, placeholder_text="Breve descrição do evento", height=35)
        self.entry_descricao.pack(padx=20, pady=(0, 10), fill="x")
        
        # Tipo e Status
        frame_tipo_status = ctk.CTkFrame(frame_cadastro, fg_color="transparent")
        frame_tipo_status.pack(padx=20, pady=(0, 15), fill="x")
        frame_tipo_status.grid_columnconfigure((0, 1), weight=1)
        
        frame_tipo = ctk.CTkFrame(frame_tipo_status, fg_color="transparent")
        frame_tipo.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkLabel(frame_tipo, text="Tipo", text_color="#374151", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.combo_tipo = ctk.CTkOptionMenu(frame_tipo, values=["Palestra", "Workshop", "SEMIC"], height=35)
        self.combo_tipo.pack(fill="x")
        
        frame_status = ctk.CTkFrame(frame_tipo_status, fg_color="transparent")
        frame_status.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ctk.CTkLabel(frame_status, text="Status", text_color="#374151", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.combo_status = ctk.CTkOptionMenu(frame_status, values=["Aberto", "Encerrado", "Cancelado"], height=35)
        self.combo_status.pack(fill="x")
        
        # Botões
        frame_botoes = ctk.CTkFrame(frame_cadastro, fg_color="transparent")
        frame_botoes.pack(padx=20, pady=(10, 20), fill="x")
        
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar Evento",
            command=self.salvar_evento,
            fg_color="#22C55E",
            hover_color="#16A34A",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_salvar.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
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
        btn_limpar.pack(side="left", expand=True, fill="x", padx=(5, 0))
        
        # --- COLUNA DIREITA: Lista de Eventos ---
        frame_lista = ctk.CTkFrame(container, fg_color="#F9FAFB", corner_radius=10)
        frame_lista.grid(row=0, column=1, sticky="nsew")
        
        # Cabeçalho da lista
        frame_header_lista = ctk.CTkFrame(frame_lista, fg_color="transparent")
        frame_header_lista.pack(fill="x", padx=20, pady=(20, 15))
        
        label_lista = ctk.CTkLabel(
            frame_header_lista,
            text="Lista de Eventos",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1F2937"
        )
        label_lista.pack(side="left")
        
        frame_filtro = ctk.CTkFrame(frame_header_lista, fg_color="transparent")
        frame_filtro.pack(side="right")
        
        ctk.CTkLabel(frame_filtro, text="Filtrar por:", text_color="#6B7280", font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 5))
        self.combo_filtro = ctk.CTkOptionMenu(
            frame_filtro, 
            values=["Todos", "Palestra", "Workshop", "SEMIC"],
            command=self.filtrar_eventos,
            width=120, 
            height=30
        )
        self.combo_filtro.pack(side="left")
        
        # Cabeçalho da tabela
        frame_table_header = ctk.CTkFrame(frame_lista, fg_color="#E5E7EB", height=40)
        frame_table_header.pack(fill="x", padx=20, pady=(0, 5))
        frame_table_header.pack_propagate(False)
        
        headers = [("Nome do Evento", 0.3), ("Data", 0.15), ("Tipo", 0.15), ("Status", 0.15), ("Ações", 0.15)]
        for texto, peso in headers:
            lbl = ctk.CTkLabel(frame_table_header, text=texto, font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151")
            lbl.pack(side="left", expand=True, fill="both", padx=10)
        
        # Scrollable frame para eventos
        self.scroll_eventos = ctk.CTkScrollableFrame(frame_lista, fg_color="white", corner_radius=5)
        self.scroll_eventos.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Carregar eventos do banco
        self.carregar_eventos()
        
        return self.frame
    
    def adicionar_evento_lista(self, evento_data):
        frame_evento = ctk.CTkFrame(self.scroll_eventos, fg_color="white", height=50)
        frame_evento.pack(fill="x", pady=2)
        frame_evento.pack_propagate(False)
        
        evento_id = evento_data['id']
        nome = evento_data['nome']
        data = evento_data['data'].strftime('%d/%m/%Y') if isinstance(evento_data['data'], datetime) else str(evento_data['data'])
        tipo = evento_data['tipo']
        status = evento_data['status']
        
        # Nome
        ctk.CTkLabel(frame_evento, text=nome, text_color="#1F2937", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # Data
        ctk.CTkLabel(frame_evento, text=data, text_color="#6B7280", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # Tipo
        ctk.CTkLabel(frame_evento, text=tipo, text_color="#6B7280", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # Status
        cor_status = "#10B981" if status == "Aberto" else ("#F59E0B" if status == "Encerrado" else "#EF4444")
        ctk.CTkLabel(frame_evento, text=status, text_color=cor_status, font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", expand=True, fill="both", padx=10)
        
        # Ações
        frame_acoes = ctk.CTkFrame(frame_evento, fg_color="transparent")
        frame_acoes.pack(side="left", expand=True, padx=10)
        
        btn_editar = ctk.CTkButton(
            frame_acoes, 
            text="Editar", 
            width=60, 
            height=25, 
            fg_color="transparent", 
            text_color="#22C55E", 
            hover_color="#F0FDF4",
            command=lambda: self.editar_evento(evento_id)
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
            command=lambda: self.excluir_evento(evento_id)
        )
        btn_excluir.pack(side="left", padx=2)
    
    def carregar_eventos(self):
        """Carrega eventos do banco de dados"""
        try:
            eventos = executar_async(self.evento_manager.listar_eventos())
            
            # Limpar lista atual
            for widget in self.scroll_eventos.winfo_children():
                widget.destroy()
            
            # Adicionar eventos
            if eventos:
                for evento in eventos:
                    self.adicionar_evento_lista(evento)
            else:
                label_vazio = ctk.CTkLabel(
                    self.scroll_eventos,
                    text="Nenhum evento cadastrado ainda.",
                    text_color="#9CA3AF",
                    font=ctk.CTkFont(size=14)
                )
                label_vazio.pack(pady=40)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar eventos: {str(e)}")
    
    def filtrar_eventos(self, tipo_filtro):
        """Filtra eventos por tipo"""
        try:
            if tipo_filtro == "Todos":
                eventos = executar_async(self.evento_manager.listar_eventos())
            else:
                eventos = executar_async(self.evento_manager.listar_eventos(tipo=tipo_filtro))
            
            # Limpar lista atual
            for widget in self.scroll_eventos.winfo_children():
                widget.destroy()
            
            # Adicionar eventos filtrados
            if eventos:
                for evento in eventos:
                    self.adicionar_evento_lista(evento)
            else:
                label_vazio = ctk.CTkLabel(
                    self.scroll_eventos,
                    text=f"Nenhum evento do tipo '{tipo_filtro}' encontrado.",
                    text_color="#9CA3AF",
                    font=ctk.CTkFont(size=14)
                )
                label_vazio.pack(pady=40)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar eventos: {str(e)}")
    
    def salvar_evento(self):
        """Salva ou atualiza um evento"""
        nome = self.entry_nome_evento.get().strip()
        data_str = self.entry_data.get().strip()
        horario = self.entry_horario.get().strip()
        vagas_str = self.entry_vagas.get().strip()
        local = self.entry_local.get().strip()
        descricao = self.entry_descricao.get().strip()
        tipo = self.combo_tipo.get()
        status = self.combo_status.get()
        
        # Validações
        if not all([nome, data_str, horario, vagas_str, local, descricao]):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        
        try:
            # Converter data
            data = datetime.strptime(data_str, '%d/%m/%Y')
            vagas = int(vagas_str)
            
            if vagas <= 0:
                messagebox.showwarning("Atenção", "O número de vagas deve ser maior que zero!")
                return
            
            # Salvar ou atualizar
            if self.evento_selecionado_id:
                # Atualizar evento existente
                executar_async(self.evento_manager.atualizar_evento(
                    evento_id=self.evento_selecionado_id,
                    nome=nome,
                    descricao=descricao,
                    data=data,
                    horario=horario,
                    local=local,
                    vagas=vagas,
                    tipo=tipo,
                    status=status
                ))
                messagebox.showinfo("Sucesso", f"Evento '{nome}' atualizado com sucesso!")
                self.evento_selecionado_id = None
            else:
                # Criar novo evento
                executar_async(self.evento_manager.criar_evento(
                    nome=nome,
                    descricao=descricao,
                    data=data,
                    horario=horario,
                    local=local,
                    vagas=vagas,
                    tipo=tipo,
                    status=status
                ))
                messagebox.showinfo("Sucesso", f"Evento '{nome}' cadastrado com sucesso!")
            
            self.limpar_formulario()
            self.carregar_eventos()
            
        except ValueError as e:
            messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar evento: {str(e)}")
    
    def editar_evento(self, evento_id):
        """Carrega dados do evento para edição"""
        try:
            evento = executar_async(self.evento_manager.buscar_evento_por_id(evento_id))
            
            if evento:
                self.evento_selecionado_id = evento_id
                
                # Preencher formulário
                self.entry_nome_evento.delete(0, 'end')
                self.entry_nome_evento.insert(0, evento['nome'])
                
                self.entry_data.delete(0, 'end')
                data_formatada = evento['data'].strftime('%d/%m/%Y') if isinstance(evento['data'], datetime) else str(evento['data'])
                self.entry_data.insert(0, data_formatada)
                
                self.entry_horario.delete(0, 'end')
                self.entry_horario.insert(0, evento['horario'])
                
                self.entry_vagas.delete(0, 'end')
                self.entry_vagas.insert(0, str(evento['vagas']))
                
                self.entry_local.delete(0, 'end')
                self.entry_local.insert(0, evento['local'])
                
                self.entry_descricao.delete(0, 'end')
                self.entry_descricao.insert(0, evento['descricao'])
                
                self.combo_tipo.set(evento['tipo'])
                self.combo_status.set(evento['status'])
                
                messagebox.showinfo("Editar", f"Editando evento: {evento['nome']}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar evento: {str(e)}")
    
    def excluir_evento(self, evento_id):
        """Exclui um evento"""
        try:
            evento = executar_async(self.evento_manager.buscar_evento_por_id(evento_id))
            
            if evento:
                if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o evento '{evento['nome']}'?\n\nIsso também excluirá todas as inscrições relacionadas."):
                    sucesso = executar_async(self.evento_manager.deletar_evento(evento_id))
                    
                    if sucesso:
                        messagebox.showinfo("Sucesso", "Evento excluído com sucesso!")
                        self.carregar_eventos()
                    else:
                        messagebox.showerror("Erro", "Não foi possível excluir o evento.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir evento: {str(e)}")
    
    def limpar_formulario(self):
        """Limpa o formulário"""
        self.evento_selecionado_id = None
        self.entry_nome_evento.delete(0, 'end')
        self.entry_data.delete(0, 'end')
        self.entry_horario.delete(0, 'end')
        self.entry_vagas.delete(0, 'end')
        self.entry_local.delete(0, 'end')
        self.entry_descricao.delete(0, 'end')
        self.combo_tipo.set("Palestra")
        self.combo_status.set("Aberto")
    
    def destruir(self):
        """Destroi a tela e desconecta do banco"""
        try:
            executar_async(self.evento_manager.desconectar())
        except:
            pass
        
        if self.frame:
            self.frame.destroy()
