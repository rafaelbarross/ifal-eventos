from prisma import Prisma
from datetime import datetime


class InscricaoService:

    def __init__(self):
        self.db = Prisma()
    
    async def conectar(self):
        if not self.db.is_connected():
            await self.db.connect()
        
    async def create_inscricao(
        self, 
        evento_id: int, 
        participante_id: int,
        data_inscricao: datetime
        ) -> dict:

        await self.conectar()

        try:
            inscricao = await self.db.inscricao.create(
                data={
                    'evento_id': evento_id,
                    'participante_id': participante_id,
                    'data_inscricao': data_inscricao,
                
                }
            )
        
              
            return inscricao
        
        except Exception as e:
            print("Erro ao cadastrar inscrição:", e)
            return None
        
        finally:
            await self.db.disconnect()
        
    async def get_participante(self, termo: str):
        await self.conectar()

        try:
            if termo == "":
                # Se termo vazio, retornar todos
                participante = await self.db.participante.find_many()
            else:
                # Buscar com contains (case-sensitive no SQLite)
                participante = await self.db.participante.find_many(
                    where={
                        'OR': [
                            {'nome': {'contains': termo}},
                            {'email': {'contains': termo}},
                            {'cpf': {'contains': termo}},
                            {'curso': {'contains': termo}},
                            {'turma': {'contains': termo}}
                        ]
                    }
                )

            if not participante:
                return None
            
            return participante

        except Exception as e:
            print("Erro ao buscar participante:", e)
            return None
        
        finally:
            await self.db.disconnect()
    
    async def get_evento(self, termo: str):
        await self.conectar()

        try:
            if termo == "":
                # Se termo vazio, retornar todos os eventos
                eventos = await self.db.evento.find_many()
            else:
                # Buscar com contains (case-sensitive no SQLite)
                eventos = await self.db.evento.find_many(
                    where={
                        'OR': [
                            {'nome': {'contains': termo}},
                            {'descricao': {'contains': termo}},
                            {'local': {'contains': termo}},
                            {'status': {'contains': termo}}   
                        ]
                    }
                )
            
            if not eventos:
                return None

            return eventos
        
        except Exception as e:
            print("Erro ao buscar evento:", e)
            return None
        
        finally:
            await self.db.disconnect()

    async def get_inscricao_by_user(self, participante_id: int) -> dict | None:
        await self.conectar()

        try:

            inscricao = await self.db.inscricao.find_first(
            where={'participante_id': participante_id},
            include={'participante': True, 'evento': True}
            )
            
            if not inscricao:
               return None
            
            return inscricao

        except Exception as e:
            print("Erro ao buscar por inscrição.", e)
            return None
        finally:
            await self.db.disconnect()
    
    async def deletar_inscricao(self, participante_id: int) -> bool:
        try:
         await self.conectar()
         await self.db.inscricao.delete_many(
                where={'participante_id': participante_id}
         )
         return True
        except Exception as e:
            print("Erro ao deletar inscrição:", e)
            return False
        
        finally:
            await self.db.disconnect()
            

        
        