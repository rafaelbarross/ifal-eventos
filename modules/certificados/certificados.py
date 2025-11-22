from prisma import Prisma
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
 
db = Prisma()

async def gerar_certificado(participante_id, evento_id, data):
     
   await db.connect()
    
   participante = await db.participante.find_unique(
        where={"id":participante_id}
   )
    
   evento = await db.evento.find_unique(
        where={"id": evento_id}
   )
    
   await db.disconnect()

   nome = participante.nome
   nome_evento = evento.nome
   carga_horaria =participante.carga_horaria

   caminho_arquivo = f"@/certificado_{nome.replace(' ', '_')}.pdf"
    
   pdf = canvas.Canvas(caminho_arquivo, pagesize=A4)
   largura, altura = A4

   pdf.setFont("Helvetica-Bold", 28)
   pdf.drawCentredString(largura/2, altura - 7*cm, "Certificado")
   pdf.setFont("Helvetica", 14)
   pdf.drawCentredString(
       largura/2, alutura - 10*cm, 
       f"Certificamos que {nome} participor do evento '{nome_evento} ({carga_horaria}h)"
    )
   pdf.save()
   print("Certificado gerado:", caminho_arquivo)
    
   with open("certificados.txt","a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome} - {carga_horaria}h\n")

