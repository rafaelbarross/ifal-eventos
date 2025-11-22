import customtkinter as ctk
from tkinter import messagebox, ttk
from modules.inscricao.inscricao import InscricaoService
import asyncio
from datetime import datetime

class TelaInscricoes:
    def __init__(self, parent, app):
        self.inscricao_service = InscricaoService()
        self.parent = parent
        self.app = app
        self.frame = None
        self.evento_selecionado = None
        self.eventos_disponiveis = []
        self.participantes_disponiveis = []
        
        # Widgets
        self.combo_eventos = None
        self.combo_participantes = None
        self.label_vagas = None
        self.label_inscritos = None
        self.label_capacidade = None
        self.tree_inscritos = None
        
    def criar(self):
        self.frame = ctk.CTkFrame(self.parent, corner_radius=0, fg_color="white")
        self.frame.grid(row=0, column=1, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        
        # ===== CABEÇALHO =====
        frame_header = ctk.CTkFrame(self.frame, fg_color="transparent")
        frame_header.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))
        
        ctk.CTkLabel(
            frame_header,
            text="Inscrições de Eventos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F2937"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            frame_header,
            text="Gerencie a inscrição de participantes nos eventos da instituição.",
            font=ctk.CTkFont(size=14),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(5, 0))
        
        # ===== SELEÇÃO DE EVENTO =====
        frame_evento = ctk.CTkFrame(self.frame, fg_color="#F9FAFB", corner_radius=10)
        frame_evento.grid(row=1, column=0, sticky="ew", padx=30, pady=10)
        
        ctk.CTkLabel(
            frame_evento,
            text="1. Selecione o Evento",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1F2937"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        self.combo_eventos = ctk.CTkComboBox(
            frame_evento,
            values=["Carregando eventos..."],
            width=600,
            height=40,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=13),
            command=self.ao_selecionar_evento
        )
        self.combo_eventos.pack(padx=20, pady=(0, 10), fill="x")
        
        # Info do evento
        frame_info = ctk.CTkFrame(frame_evento, fg_color="white", corner_radius=8)
        frame_info.pack(padx=20, pady=(0, 15), fill="x")
        
        info_grid = ctk.CTkFrame(frame_info, fg_color="transparent")
        info_grid.pack(padx=15, pady=12, fill="x")
        
        self.label_vagas = ctk.CTkLabel(
            info_grid,
            text="Vagas Disponíveis: --",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#10B981"
        )
        self.label_vagas.pack(side="left", padx=(0, 30))
        
        self.label_inscritos = ctk.CTkLabel(
            info_grid,
            text="Inscritos: --",
            font=ctk.CTkFont(size=13),
            text_color="#1F2937"
        )
        self.label_inscritos.pack(side="left", padx=(0, 30))
        
        self.label_capacidade = ctk.CTkLabel(
            info_grid,
            text="Capacidade: --",
            font=ctk.CTkFont(size=13),
            text_color="#6B7280"
        )
        self.label_capacidade.pack(side="left")
        
        # ===== NOVA INSCRIÇÃO =====
        frame_inscricao = ctk.CTkFrame(self.frame, fg_color="#F0FDF4", corner_radius=10)
        frame_inscricao.grid(row=2, column=0, sticky="ew", padx=30, pady=10)
        
        ctk.CTkLabel(
            frame_inscricao,
            text="2. Inscrever Participante",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1F2937"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        frame_form = ctk.CTkFrame(frame_inscricao, fg_color="transparent")
        frame_form.pack(padx=20, pady=(0, 15), fill="x")
        
        self.combo_participantes = ctk.CTkComboBox(
            frame_form,
            values=["Carregando participantes..."],
            width=500,
            height=40,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=13)
        )
        self.combo_participantes.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            frame_form,
            text="+ Inscrever",
            width=150,
            height=40,
            fg_color="#22C55E",
            hover_color="#16A34A",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.cadastrar_inscricao
        ).pack(side="left")
        
        # ===== LISTA DE INSCRITOS =====
        frame_lista = ctk.CTkFrame(self.frame, fg_color="#F9FAFB", corner_radius=10)
        frame_lista.grid(row=3, column=0, sticky="ew", padx=30, pady=10)
        
        ctk.CTkLabel(
            frame_lista,
            text="3. Inscritos no Evento",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1F2937"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Treeview para lista de inscritos
        frame_tree = ctk.CTkFrame(frame_lista, fg_color="white", corner_radius=8)
        frame_tree.pack(padx=20, pady=(0, 15), fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical")
        
        # Treeview
        self.tree_inscritos = ttk.Treeview(
            frame_tree,
            columns=("nome", "cpf", "data", "status"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=8
        )
        scrollbar.config(command=self.tree_inscritos.yview)
        
        # Colunas
        self.tree_inscritos.heading("nome", text="Nome")
        self.tree_inscritos.heading("cpf", text="CPF")
        self.tree_inscritos.heading("data", text="Data de Inscrição")
        self.tree_inscritos.heading("status", text="Status")
        
        self.tree_inscritos.column("nome", width=250)
        self.tree_inscritos.column("cpf", width=150)
        self.tree_inscritos.column("data", width=150)
        self.tree_inscritos.column("status", width=100)
        
        self.tree_inscritos.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Botão cancelar inscrição
        frame_acoes = ctk.CTkFrame(frame_lista, fg_color="transparent")
        frame_acoes.pack(padx=20, pady=(0, 15))
        
        ctk.CTkButton(
            frame_acoes,
            text="Cancelar Inscrição Selecionada",
            width=200,
            height=35,
            fg_color="transparent",
            text_color="#EF4444",
            border_width=2,
            border_color="#EF4444",
            hover_color="#FEE2E2",
            font=ctk.CTkFont(size=13),
            command=self.cancelar_inscricao_selecionada
        ).pack()
        
        # Carregar dados
        self.frame.after(100, self.carregar_dados_iniciais)
        
        return self.frame
    
    def carregar_dados_iniciais(self):
        """Carrega eventos e participantes"""
        try:
            asyncio.run(self.carregar_eventos())
            asyncio.run(self.carregar_participantes())
        except Exception as e:
            print(f"Erro ao carregar dados iniciais: {e}")
            messagebox.showerror("Erro", f"Falha ao carregar dados: {e}")
    
    async def carregar_eventos(self):
        """Carrega lista de eventos"""
        try:
            eventos = await self.inscricao_service.get_evento("")
            if eventos:
                self.eventos_disponiveis = eventos
                valores = [f"{e.nome} - {e.data.strftime('%d/%m/%Y %H:%M')}" for e in eventos]
                self.combo_eventos.configure(values=valores)
                self.combo_eventos.set("Selecione um evento...")
                print(f"✓ {len(eventos)} eventos carregados")
            else:
                self.combo_eventos.configure(values=["Nenhum evento disponível"])
                self.combo_eventos.set("Nenhum evento disponível")
                print("⚠ Nenhum evento encontrado")
        except Exception as e:
            print(f"✗ Erro ao carregar eventos: {e}")
            self.combo_eventos.configure(values=["Erro ao carregar"])
            self.combo_eventos.set("Erro ao carregar eventos")
    
    async def carregar_participantes(self):
        """Carrega lista de participantes"""
        try:
            participantes = await self.inscricao_service.get_participante("")
            if participantes:
                self.participantes_disponiveis = participantes
                valores = [f"{p.nome} - {p.cpf}" for p in participantes]
                self.combo_participantes.configure(values=valores)
                self.combo_participantes.set("Selecione um participante...")
                print(f"✓ {len(participantes)} participantes carregados")
            else:
                self.combo_participantes.configure(values=["Nenhum participante cadastrado"])
                self.combo_participantes.set("Nenhum participante cadastrado")
                print("⚠ Nenhum participante encontrado")
        except Exception as e:
            print(f"✗ Erro ao carregar participantes: {e}")
            self.combo_participantes.configure(values=["Erro ao carregar"])
            self.combo_participantes.set("Erro ao carregar participantes")
    
    def ao_selecionar_evento(self, escolha):
        """Callback quando um evento é selecionado"""
        try:
            # Encontrar o evento selecionado
            index = self.combo_eventos.cget("values").index(escolha)
            evento = self.eventos_disponiveis[index]
            self.evento_selecionado = evento.id
            
            # Atualizar info do evento
            asyncio.run(self.atualizar_info_evento(evento))
            asyncio.run(self.carregar_inscritos(evento.id))
            
            print(f"✓ Evento selecionado: {evento.nome}")
        except Exception as e:
            print(f"✗ Erro ao selecionar evento: {e}")
    
    async def atualizar_info_evento(self, evento):
        """Atualiza informações do evento selecionado"""
        try:
            await self.inscricao_service.conectar()
            inscricoes = await self.inscricao_service.db.inscricao.find_many(
                where={'evento_id': evento.id}
            )
            await self.inscricao_service.db.disconnect()
            
            num_inscritos = len(inscricoes)
            vagas_disponiveis = evento.vagas - num_inscritos
            
            self.label_vagas.configure(text=f"Vagas Disponíveis: {vagas_disponiveis}")
            self.label_inscritos.configure(text=f"Inscritos: {num_inscritos}")
            self.label_capacidade.configure(text=f"Capacidade: {evento.vagas}")
            
            # Mudar cor se lotado
            if vagas_disponiveis <= 0:
                self.label_vagas.configure(text_color="#EF4444")
            elif vagas_disponiveis <= 5:
                self.label_vagas.configure(text_color="#F59E0B")
            else:
                self.label_vagas.configure(text_color="#10B981")
                
        except Exception as e:
            print(f"✗ Erro ao atualizar info do evento: {e}")
    
    async def carregar_inscritos(self, evento_id):
        """Carrega inscritos do evento selecionado"""
        # Limpar árvore
        for item in self.tree_inscritos.get_children():
            self.tree_inscritos.delete(item)
        
        try:
            await self.inscricao_service.conectar()
            inscricoes = await self.inscricao_service.db.inscricao.find_many(
                where={'evento_id': evento_id},
                include={'participante': True}
            )
            await self.inscricao_service.db.disconnect()
            
            for inscricao in inscricoes:
                p = inscricao.participante
                self.tree_inscritos.insert(
                    "",
                    "end",
                    values=(
                        p.nome,
                        p.cpf,
                        inscricao.data_inscricao.strftime("%d/%m/%Y %H:%M"),
                        "Confirmado"
                    ),
                    tags=(inscricao.id,)
                )
            
            print(f"✓ {len(inscricoes)} inscritos carregados")
        except Exception as e:
            print(f"✗ Erro ao carregar inscritos: {e}")
    
    def cadastrar_inscricao(self):
        """Cadastra nova inscrição"""
        if not self.evento_selecionado:
            messagebox.showerror("Erro", "Selecione um evento primeiro.")
            return
        
        escolha_participante = self.combo_participantes.get()
        if not escolha_participante or "Selecione" in escolha_participante or "Nenhum" in escolha_participante:
            messagebox.showerror("Erro", "Selecione um participante.")
            return
        
        try:
            # Encontrar participante selecionado
            index = self.combo_participantes.cget("values").index(escolha_participante)
            participante = self.participantes_disponiveis[index]
            
            # Executar todas as operações assíncronas de uma vez
            asyncio.run(self._realizar_inscricao(participante))
            
        except Exception as e:
            print(f"✗ Erro ao cadastrar inscrição: {e}")
            messagebox.showerror("Erro", f"Falha ao cadastrar inscrição: {e}")
    
    async def _realizar_inscricao(self, participante):
        """Método auxiliar assíncrono para realizar a inscrição"""
        try:
            # Verificar se já está inscrito
            await self.inscricao_service.conectar()
            inscricao_existente = await self.inscricao_service.db.inscricao.find_first(
                where={
                    'participante_id': participante.id,
                    'evento_id': self.evento_selecionado
                }
            )
            await self.inscricao_service.db.disconnect()
            
            if inscricao_existente:
                messagebox.showwarning("Aviso", "Este participante já está inscrito neste evento.")
                return
            
            # Criar inscrição
            await self.inscricao_service.create_inscricao(
                participante_id=participante.id,
                evento_id=self.evento_selecionado,
                data_inscricao=datetime.now()
            )
            
            # Atualizar interface
            evento = next(e for e in self.eventos_disponiveis if e.id == self.evento_selecionado)
            await self.atualizar_info_evento(evento)
            await self.carregar_inscritos(self.evento_selecionado)
            
            # Resetar combo
            self.combo_participantes.set("Selecione um participante...")
            
            messagebox.showinfo("Sucesso", f"Inscrição de {participante.nome} realizada com sucesso!")
            print(f"✓ Inscrição cadastrada: {participante.nome}")
            
        except Exception as e:
            print(f"✗ Erro ao realizar inscrição: {e}")
            raise
    
    def cancelar_inscricao_selecionada(self):
        """Cancela inscrição selecionada na árvore"""
        selecionado = self.tree_inscritos.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma inscrição para cancelar.")
            return
        
        item = selecionado[0]
        inscricao_id = int(self.tree_inscritos.item(item)['tags'][0])
        nome = self.tree_inscritos.item(item)['values'][0]
        
        confirmar = messagebox.askyesno(
            "Confirmar Cancelamento",
            f"Tem certeza que deseja cancelar a inscrição de {nome}?"
        )
        
        if not confirmar:
            return
        
        try:
            # Executar todas as operações assíncronas de uma vez
            asyncio.run(self._realizar_cancelamento(inscricao_id, nome))
            
        except Exception as e:
            print(f"✗ Erro ao cancelar inscrição: {e}")
            messagebox.showerror("Erro", f"Falha ao cancelar inscrição: {e}")
    
    async def _realizar_cancelamento(self, inscricao_id, nome):
        """Método auxiliar assíncrono para cancelar inscrição"""
        try:
            await self.inscricao_service.conectar()
            await self.inscricao_service.db.inscricao.delete(
                where={'id': inscricao_id}
            )
            await self.inscricao_service.db.disconnect()
            
            # Atualizar interface
            evento = next(e for e in self.eventos_disponiveis if e.id == self.evento_selecionado)
            await self.atualizar_info_evento(evento)
            await self.carregar_inscritos(self.evento_selecionado)
            
            messagebox.showinfo("Sucesso", "Inscrição cancelada com sucesso!")
            print(f"✓ Inscrição cancelada: {nome}")
            
        except Exception as e:
            print(f"✗ Erro ao realizar cancelamento: {e}")
            raise
    
    def destruir(self):
        """Destroi o frame"""
        if self.frame:
            self.frame.destroy()
