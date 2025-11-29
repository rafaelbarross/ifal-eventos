import customtkinter as ctk
from tkinter import simpledialog, messagebox
from modules.certificados.certificados import gerar_certificado
import asyncio
import threading
from prisma import Prisma

db = Prisma()

class TelaCertificados():
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.participantes = []
        self.eventos = []
        self.frame = None

        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, daemon=True)
        self.thread.start()
        
    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def criar(self):
        self.frame = ctk.CTkFrame(self.parent, corner_radius=0, fg_color="white")
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        self.frame.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            self.frame,
            text="Certificados",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F2937"
        )
        titulo.grid(row=0, column=0, pady=20, padx=20)
        
        self.label_status = ctk.CTkLabel(
            self.frame, 
            text="Carregando eventos...", 
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        )
        self.label_status.grid(row=1, column=0, pady=10, padx=20)

        self.combo_eventos = ctk.CTkComboBox(
            self.frame, 
            values=["Carregando..."], 
            width=300, 
            state="disabled"
        )

        self.combo_eventos.grid(row=2, column=0, pady=0, padx=20)

        btn_emitir = ctk.CTkButton(
            self.frame,
            text = "Emitir Certificados",
            fg_color = "#22C55E",
            hover_color = "#16A34A",
            text_color = "white",
            command=lambda: self.emitir_certificados_wrapper()
        )
        btn_emitir.grid(row=3, column=0, padx=10, pady=20)
        
        asyncio.run_coroutine_threadsafe(self.carregar_dados(), self.loop)
        
        return self.frame

    async def carregar_dados(self):
        try:
            await db.connect()
            self.participantes = await db.participante.find_many()
            self.eventos = await db.evento.find_many()
            await db.disconnect()

            nomes_eventos = [e.nome for e in self.eventos]

            self.parent.after(0, lambda: self.atualizar_combo(nomes_eventos))
        
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.parent.after(0, lambda: messagebox.showerror("Erro ao carregar"))

    def atualizar_combo(self, nomes_eventos):
        if nomes_eventos:
            self.combo_eventos.configure(values=nomes_eventos, state="readonly")
            self.combo_eventos.set("Selecione um evento")
            self.label_status.configure(text=f"{len(self.eventos)} evento(s) carregado(s)")
        else:
            self.combo_eventos.configure(values=["Nenhum evento disponível"])
            self.combo_eventos.set("Nenhum evento disponível")
            self.label_status.configure(text="Nenhum evento encontrado")
    
    def emitir_certificados_wrapper(self):
        asyncio.run_coroutine_threadsafe(self.emitir_certificados(), self.loop) 
    
    async def emitir_certificados(self):
        try:         
            quantidade = await self.pedir_quantidade()

            if not quantidade or quantidade <= 0:
                return
        
            evento_nome = self.combo_eventos.get()    
        
            if not evento_nome or evento_nome == "Selecione um evento:" or evento_nome == "Carregando...":
                self.parent.after(0, lambda: messagebox.showwarning(
                  "Aviso", "Selecione um evento primeiro!"
                ))
                return
        
            evento = next((e for e in self.eventos if e.nome == evento_nome), None)
        
            if not evento:
                self.parent.after(0, lambda: messagebox.showerror("Erro", "Evento não encontrado"))
                return
        
            evento_id = evento.id
            data = "28/11/2025"
            contador = 0
            
            print(f"\n{'='*50}")
            print(f"Iniciando geração de {quantidade} certificados")
            print(f"{'='*50}\n")

            while contador < quantidade:
                if contador >= len(self.participantes):
                    self.parent.after(0, lambda: messagebox.showinfo(
                        "Informação", "Não há mais partipantes disponíveis."
                    ))
                    break
        
                participante = self.participantes[contador]
                print(f"Gerando para: {participante.nome}")
            
                try:
                    await gerar_certificado(participante.id, evento_id, data)
                    contador += 1
                
                    c = contador
                    q = quantidade
                    self.parent.after(0, lambda: self.label_status.configure(text=f"Gerando certificados... {c}/{q}"))
            
                except Exception as e:
                    print(f"Erro ao gerar certificados: {e}")
                    contador +=1
        
            print(f"\n{'='*50}")
            print(f"Concluído! {contador} certificados gerados")
            print(f"{'='*50}\n")

            c = contador
            self.parent.after(0, lambda: self.label_status.configure(
                text=f"{c} certificado(s) gerado(s) com sucesso!"
            ))

            self.parent.after(0, lambda: messagebox.showinfo(
                "Concluído", f"{c} certificado(s) gerado(s) com sucesso!"
            ))
        
        except Exception as e:
            print(f"Erro ao emitir certificados: {e}")
            import traceback
            traceback.print_exc()
            self.parent.after(0, lambda: messagebox.showerror("Erro", f"Erro: {str(e)}"))
            
    
    async def pedir_quantidade(self):
        future = asyncio.Future()
        
        def ask():
            try:
                max_qtd = len(self.participantes) if self.participantes else 100
                qtd = simpledialog.askinteger(
                    "Quantidade",
                    "Quantos certificados você deseja emitir:",
                    minvalue=1,
                    maxvalue=max_qtd
                )
                self.loop.call_soon_threadsafe(future.set_result, qtd)
            except Exception as e:
                self.loop.call_soon_threadsafe(future.set_exception, e)
        self.parent.after(0, ask)
        return await future
    
    def destruir(self):
        if self.frame:
            self.frame.destroy()
            self.frame = None
