from prisma import Prisma
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os
 
db = Prisma()

async def gerar_certificado(participante_id:int, evento_id: int, data: str):
     
   await db.connect()
    
   participante = await db.participante.find_unique(
        where={"id":participante_id}
   )
    
   evento = await db.evento.find_unique(
        where={"id": evento_id}
   )
    
   await db.disconnect()

   if not participante:
     raise ValueError("Participante não encontrado.")
   if not evento:
     raise ValueError("Evento não encontrado.")

   nome = participante.nome
   nome_evento = evento.nome
   
   
   pasta = "certificados"
   os.makedirs(pasta, exist_ok=True)
   caminho_arquivo = os.path.join(pasta, f"certificado_{nome.replace(' ', '_')}.pdf")
    
   pdf = canvas.Canvas(caminho_arquivo, pagesize=landscape(A4))
   largura, altura = landscape(A4)

   caminho_logo = "certificados/logo_ifal.png"

   if os.path.exists(caminho_logo):
     largura_logo = 7*cm
     altura_logo =  7*cm
     
     x_logo = (largura - largura_logo) /2
     y_logo = altura - 10*cm

     pdf.drawImage(caminho_logo, x_logo, y_logo,
                   width=largura_logo, height=altura_logo,
                   preserveAspectRatio=True, mask='auto')

   pdf.setFont("Helvetica-Bold", 28)
   pdf.drawCentredString(largura/2, altura - 10.5*cm, "Certificado")
   pdf.setFont("Helvetica", 14)
   linha1 = (
     f"Certificamos que {nome} participou do evento " 
     f"'{nome_evento}', realizado em {data}"
   )

   linha2 = ("com total de quarenta (40) horas de atividade.")
   pdf.drawCentredString(
       largura/2, altura - 12*cm, linha1
     )

   pdf.drawCentredString(
       largura/2, altura -13.2*cm, linha2
     )

   pdf.save()
   print("Certificado gerado:", caminho_arquivo)
    
   with open("certificados.txt","a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome} - 40h\n")

