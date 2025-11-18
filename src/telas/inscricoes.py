import customtkinter as ctk
from tkinter import messagebox

class TelaInscricoes:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = None
        self.evento_selecionado = None
        
    def criar(self):
        self.frame = ctk.CTkFrame(self.parent, corner_radius=0, fg_color="white")
        self.frame.grid(row=0, column=1, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        
        # Título
        titulo = ctk.CTkLabel(
            self.frame,
            text="Inscrições de Eventos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F2937"
        )
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 5))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            self.frame,
            text="Gerencie a inscrição de participantes nos eventos da instituição.",
            font=ctk.CTkFont(size=14),
            text_color="#6B7280"
        )
        subtitulo.grid(row=1, column=0, columnspan=2, sticky="w", padx=30, pady=(0, 20))
        
        # Container com 2 colunas
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=30, pady=(0, 20))
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        # --- COLUNA ESQUERDA: Eventos Disponíveis ---
        frame_eventos = ctk.CTkFrame(container, fg_color="#F9FAFB", corner_radius=10)
        frame_eventos.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        frame_eventos.grid_propagate(False)
        frame_eventos.configure(width=350)
        
        label_eventos = ctk.CTkLabel(
            frame_eventos,
            text="Eventos Disponíveis",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1F2937"
        )
        label_eventos.pack(padx=20, pady=(20, 15), anchor="w")
        
        # Campo de busca
        frame_busca_evento = ctk.CTkFrame(frame_eventos, fg_color="white", corner_radius=5)
        frame_busca_evento.pack(padx=20, pady=(0, 10), fill="x")
        
        ctk.CTkLabel(frame_busca_evento, text="🔍", font=ctk.CTkFont(size=14)).pack(side="left", padx=(8, 0))
        entry_busca_evento = ctk.CTkEntry(
            frame_busca_evento,
            placeholder_text="Buscar evento por nome...",
            height=35,
            border_width=0,
            fg_color="white"
        )
        entry_busca_evento.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        # Scrollable frame para eventos
        self.scroll_eventos = ctk.CTkScrollableFrame(frame_eventos, fg_color="transparent")
        self.scroll_eventos.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Exemplos de eventos
        self.adicionar_evento_card("Palestra de Inteligência Artificial", "15 de Ago, 14:00", "Aberto", "#10B981")
        self.adicionar_evento_card("Workshop de Design Thinking", "22 de Ago, 09:00", "Lotado", "#EF4444")
        self.adicionar_evento_card("Hackathon de Inovação", "05 de Set, 18:00", "Últimas Vagas", "#F59E0B")
        self.adicionar_evento_card("Feira de Carreiras 2024", "12 de Out, 10:00", "Finalizado", "#6B7280")
        
        # --- COLUNA DIREITA: Detalhes do Evento ---
        frame_detalhes = ctk.CTkFrame(container, fg_color="#F9FAFB", corner_radius=10)
        frame_detalhes.grid(row=0, column=1, sticky="nsew")
        
        # Cabeçalho do evento selecionado
        frame_header = ctk.CTkFrame(frame_detalhes, fg_color="transparent")
        frame_header.pack(fill="x", padx=20, pady=(20, 15))
        
        self.label_evento_titulo = ctk.CTkLabel(
            frame_header,
            text="Palestra de Inteligência Artificial",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1F2937"
        )
        self.label_evento_titulo.pack(side="left", anchor="w")
        
        btn_editar_evento = ctk.CTkButton(
            frame_header,
            text="✏️ Editar Evento",
            width=120,
            height=32,
            fg_color="white",
            text_color="#22C55E",
            border_width=1,
            border_color="#22C55E",
            hover_color="#F0FDF4",
            font=ctk.CTkFont(size=12)
        )
        btn_editar_evento.pack(side="right")
        
        # Info do evento
        self.label_evento_info = ctk.CTkLabel(
            frame_detalhes,
            text="Auditório Principal • 15 de Ago, 14:00",
            font=ctk.CTkFont(size=13),
            text_color="#6B7280"
        )
        self.label_evento_info.pack(padx=20, pady=(0, 15), anchor="w")
        
        # Cards de estatísticas
        frame_stats = ctk.CTkFrame(frame_detalhes, fg_color="transparent")
        frame_stats.pack(fill="x", padx=20, pady=(0, 20))
        
        # Vagas Disponíveis
        card_vagas = ctk.CTkFrame(frame_stats, fg_color="white", corner_radius=8)
        card_vagas.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            card_vagas,
            text="Vagas Disponíveis",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        ).pack(padx=15, pady=(12, 2))
        
        ctk.CTkLabel(
            card_vagas,
            text="18",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#10B981"
        ).pack(padx=15, pady=(0, 12))
        
        # Inscritos
        card_inscritos = ctk.CTkFrame(frame_stats, fg_color="white", corner_radius=8)
        card_inscritos.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            card_inscritos,
            text="Inscritos",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        ).pack(padx=15, pady=(12, 2))
        
        ctk.CTkLabel(
            card_inscritos,
            text="32",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F2937"
        ).pack(padx=15, pady=(0, 12))
        
        # Capacidade Total
        card_capacidade = ctk.CTkFrame(frame_stats, fg_color="white", corner_radius=8)
        card_capacidade.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            card_capacidade,
            text="Capacidade Total",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        ).pack(padx=15, pady=(12, 2))
        
        ctk.CTkLabel(
            card_capacidade,
            text="50",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F2937"
        ).pack(padx=15, pady=(0, 12))
        
        # Inscrever Novo Participante
        frame_inscricao = ctk.CTkFrame(frame_detalhes, fg_color="#F0FDF4", corner_radius=8)
        frame_inscricao.pack(fill="x", padx=20, pady=(0, 15))
        
        label_inscricao = ctk.CTkLabel(
            frame_inscricao,
            text="Inscrever Novo Participante",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#1F2937"
        )
        label_inscricao.pack(padx=15, pady=(12, 8), anchor="w")
        
        frame_busca_participante = ctk.CTkFrame(frame_inscricao, fg_color="white", corner_radius=5)
        frame_busca_participante.pack(fill="x", padx=15, pady=(0, 12))
        
        ctk.CTkLabel(frame_busca_participante, text="🔍", font=ctk.CTkFont(size=14)).pack(side="left", padx=(8, 0))
        self.entry_busca_participante = ctk.CTkEntry(
            frame_busca_participante,
            placeholder_text="Buscar por nome, matrícula ou e-mail...",
            height=38,
            border_width=0,
            fg_color="white"
        )
        self.entry_busca_participante.pack(side="left", fill="x", expand=True, padx=8)
        
        btn_inscrever = ctk.CTkButton(
            frame_busca_participante,
            text="+ Inscrever",
            width=100,
            height=38,
            fg_color="#22C55E",
            hover_color="#16A34A",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        btn_inscrever.pack(side="right", padx=(0, 8))
        
        # Lista de Inscritos
        label_lista = ctk.CTkLabel(
            frame_detalhes,
            text="Lista de Inscritos (32)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1F2937"
        )
        label_lista.pack(padx=20, pady=(10, 10), anchor="w")
        
        # Cabeçalho da tabela
        frame_table_header = ctk.CTkFrame(frame_detalhes, fg_color="#E5E7EB", height=40)
        frame_table_header.pack(fill="x", padx=20, pady=(0, 5))
        frame_table_header.pack_propagate(False)
        
        headers_config = [
            ("Nome", 0.30),
            ("Matrícula", 0.20),
            ("Data de Inscrição", 0.30),
            ("Ações", 0.20)
        ]
        
        for texto, peso in headers_config:
            lbl = ctk.CTkLabel(
                frame_table_header,
                text=texto,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#374151"
            )
            lbl.pack(side="left", expand=True, fill="both", padx=10)
        
        # Scrollable frame para inscritos
        self.scroll_inscritos = ctk.CTkScrollableFrame(frame_detalhes, fg_color="white", corner_radius=5, height=200)
        self.scroll_inscritos.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Exemplos de inscritos
        self.adicionar_inscrito_lista("Carlos Almeida", "RA0012345", "10 de Jul, 2024")
        self.adicionar_inscrito_lista("Mariana Silva", "RA0054321", "11 de Jul, 2024")
        self.adicionar_inscrito_lista("João Pereira", "RA0098765", "11 de Jul, 2024")
        self.adicionar_inscrito_lista("Beatriz Santos", "RA0024680", "12 de Jul, 2024")
        
        return self.frame
    
    def adicionar_evento_card(self, nome, data, status, cor_status):
        frame_card = ctk.CTkFrame(self.scroll_eventos, fg_color="white", corner_radius=8, border_width=1, border_color="#E5E7EB")
        frame_card.pack(fill="x", pady=5)
        
        # Ícone e conteúdo
        frame_conteudo = ctk.CTkFrame(frame_card, fg_color="transparent")
        frame_conteudo.pack(fill="x", padx=12, pady=12)
        
        # Ícone
        label_icone = ctk.CTkLabel(
            frame_conteudo,
            text="🎓",
            font=ctk.CTkFont(size=20)
        )
        label_icone.pack(side="left", padx=(0, 10))
        
        # Texto
        frame_texto = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_texto.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            frame_texto,
            text=nome,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#1F2937",
            anchor="w"
        ).pack(fill="x")
        
        ctk.CTkLabel(
            frame_texto,
            text=data,
            font=ctk.CTkFont(size=11),
            text_color="#6B7280",
            anchor="w"
        ).pack(fill="x")
        
        # Badge de status
        badge = ctk.CTkLabel(
            frame_card,
            text=status,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=cor_status,
            fg_color=f"{cor_status}20",
            corner_radius=4
        )
        badge.pack(padx=12, pady=(0, 12), anchor="w")
    
    def adicionar_inscrito_lista(self, nome, matricula, data):
        frame_inscrito = ctk.CTkFrame(self.scroll_inscritos, fg_color="white", height=50)
        frame_inscrito.pack(fill="x", pady=2)
        frame_inscrito.pack_propagate(False)
        
        # Nome
        ctk.CTkLabel(frame_inscrito, text=nome, text_color="#1F2937", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # Matrícula
        ctk.CTkLabel(frame_inscrito, text=matricula, text_color="#6B7280", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # Data
        ctk.CTkLabel(frame_inscrito, text=data, text_color="#6B7280", font=ctk.CTkFont(size=13)).pack(side="left", expand=True, fill="both", padx=10)
        
        # Ações
        btn_cancelar = ctk.CTkButton(
            frame_inscrito,
            text="Cancelar Inscrição",
            width=120,
            height=28,
            fg_color="transparent",
            text_color="#EF4444",
            border_width=1,
            border_color="#EF4444",
            hover_color="#FEE2E2",
            font=ctk.CTkFont(size=11)
        )
        btn_cancelar.pack(side="left", expand=True, padx=10)
    
    def destruir(self):
        if self.frame:
            self.frame.destroy()
