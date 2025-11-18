from prisma import Prisma
from datetime import datetime
from typing import List, Optional, Dict, Any


class EventoManager:
    """Gerenciador de eventos usando Prisma ORM"""
    
    def __init__(self):
        self.db = Prisma()
    
    async def conectar(self):
        """Conecta ao banco de dados"""
        if not self.db.is_connected():
            await self.db.connect()
    
    async def desconectar(self):
        """Desconecta do banco de dados"""
        if self.db.is_connected():
            await self.db.disconnect()
    
    async def criar_evento(
        self,
        nome: str,
        descricao: str,
        data: datetime,
        horario: str,
        local: str,
        vagas: int,
        tipo: str,
        status: str = "Aberto"
    ) -> Dict[str, Any]:
        """
        Cria um novo evento
        
        Args:
            nome: Nome do evento
            descricao: Descrição do evento
            data: Data do evento
            horario: Horário do evento
            local: Local do evento
            vagas: Número de vagas
            tipo: Tipo do evento (Palestra, Workshop, SEMIC)
            status: Status do evento (Aberto, Encerrado, Cancelado)
        
        Returns:
            Dicionário com os dados do evento criado
        """
        await self.conectar()
        
        evento = await self.db.evento.create(
            data={
                'nome': nome,
                'descricao': descricao,
                'data': data,
                'horario': horario,
                'local': local,
                'vagas': vagas,
                'tipo': tipo,
                'status': status
            }
        )
        
        return {
            'id': evento.id,
            'nome': evento.nome,
            'descricao': evento.descricao,
            'data': evento.data,
            'horario': evento.horario,
            'local': evento.local,
            'vagas': evento.vagas,
            'tipo': evento.tipo,
            'status': evento.status,
            'criado_em': evento.criado_em
        }
    
    async def listar_eventos(
        self,
        status: Optional[str] = None,
        tipo: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lista todos os eventos com filtros opcionais
        
        Args:
            status: Filtrar por status (opcional)
            tipo: Filtrar por tipo (opcional)
        
        Returns:
            Lista de eventos
        """
        await self.conectar()
        
        where_clause = {}
        if status:
            where_clause['status'] = status
        if tipo:
            where_clause['tipo'] = tipo
        
        eventos = await self.db.evento.find_many(
            where=where_clause if where_clause else None,
            include={'inscricoes': True},
            order={'data': 'desc'}
        )
        
        resultado = []
        for evento in eventos:
            resultado.append({
                'id': evento.id,
                'nome': evento.nome,
                'descricao': evento.descricao,
                'data': evento.data,
                'horario': evento.horario,
                'local': evento.local,
                'vagas': evento.vagas,
                'tipo': evento.tipo,
                'status': evento.status,
                'total_inscricoes': len(evento.inscricoes) if evento.inscricoes else 0,
                'criado_em': evento.criado_em
            })
        
        return resultado
    
    async def buscar_evento_por_id(self, evento_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca um evento específico por ID
        
        Args:
            evento_id: ID do evento
        
        Returns:
            Dicionário com os dados do evento ou None
        """
        await self.conectar()
        
        evento = await self.db.evento.find_unique(
            where={'id': evento_id},
            include={'inscricoes': True}
        )
        
        if not evento:
            return None
        
        return {
            'id': evento.id,
            'nome': evento.nome,
            'descricao': evento.descricao,
            'data': evento.data,
            'horario': evento.horario,
            'local': evento.local,
            'vagas': evento.vagas,
            'tipo': evento.tipo,
            'status': evento.status,
            'total_inscricoes': len(evento.inscricoes) if evento.inscricoes else 0,
            'criado_em': evento.criado_em
        }
    
    async def atualizar_evento(
        self,
        evento_id: int,
        nome: Optional[str] = None,
        descricao: Optional[str] = None,
        data: Optional[datetime] = None,
        horario: Optional[str] = None,
        local: Optional[str] = None,
        vagas: Optional[int] = None,
        tipo: Optional[str] = None,
        status: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Atualiza um evento existente
        
        Args:
            evento_id: ID do evento
            nome: Novo nome (opcional)
            descricao: Nova descrição (opcional)
            data: Nova data (opcional)
            horario: Novo horário (opcional)
            local: Novo local (opcional)
            vagas: Novo número de vagas (opcional)
            tipo: Novo tipo (opcional)
            status: Novo status (opcional)
        
        Returns:
            Dicionário com os dados do evento atualizado ou None
        """
        await self.conectar()
        
        # Verificar se o evento existe
        evento_existente = await self.db.evento.find_unique(
            where={'id': evento_id}
        )
        
        if not evento_existente:
            return None
        
        # Preparar dados para atualização
        dados_atualizacao = {}
        if nome is not None:
            dados_atualizacao['nome'] = nome
        if descricao is not None:
            dados_atualizacao['descricao'] = descricao
        if data is not None:
            dados_atualizacao['data'] = data
        if horario is not None:
            dados_atualizacao['horario'] = horario
        if local is not None:
            dados_atualizacao['local'] = local
        if vagas is not None:
            dados_atualizacao['vagas'] = vagas
        if tipo is not None:
            dados_atualizacao['tipo'] = tipo
        if status is not None:
            dados_atualizacao['status'] = status
        
        evento = await self.db.evento.update(
            where={'id': evento_id},
            data=dados_atualizacao
        )
        
        return {
            'id': evento.id,
            'nome': evento.nome,
            'descricao': evento.descricao,
            'data': evento.data,
            'horario': evento.horario,
            'local': evento.local,
            'vagas': evento.vagas,
            'tipo': evento.tipo,
            'status': evento.status,
            'criado_em': evento.criado_em
        }
    
    async def deletar_evento(self, evento_id: int) -> bool:
        """
        Deleta um evento
        
        Args:
            evento_id: ID do evento
        
        Returns:
            True se deletado com sucesso, False se não encontrado
        """
        await self.conectar()
        
        try:
            # Verificar se o evento existe
            evento_existente = await self.db.evento.find_unique(
                where={'id': evento_id}
            )
            
            if not evento_existente:
                return False
            
            # Deletar inscrições relacionadas primeiro (devido à restrição de FK)
            await self.db.inscricao.delete_many(
                where={'evento_id': evento_id}
            )
            
            # Deletar o evento
            await self.db.evento.delete(
                where={'id': evento_id}
            )
            
            return True
        except Exception as e:
            print(f"Erro ao deletar evento: {e}")
            return False
    
    async def contar_vagas_disponiveis(self, evento_id: int) -> Optional[int]:
        """
        Calcula o número de vagas disponíveis em um evento
        
        Args:
            evento_id: ID do evento
        
        Returns:
            Número de vagas disponíveis ou None se evento não encontrado
        """
        await self.conectar()
        
        evento = await self.db.evento.find_unique(
            where={'id': evento_id},
            include={'inscricoes': True}
        )
        
        if not evento:
            return None
        
        total_inscricoes = len(evento.inscricoes) if evento.inscricoes else 0
        vagas_disponiveis = evento.vagas - total_inscricoes
        
        return max(0, vagas_disponiveis)
    
    async def verificar_evento_lotado(self, evento_id: int) -> Optional[bool]:
        """
        Verifica se um evento está lotado
        
        Args:
            evento_id: ID do evento
        
        Returns:
            True se lotado, False se há vagas, None se evento não encontrado
        """
        vagas_disponiveis = await self.contar_vagas_disponiveis(evento_id)
        
        if vagas_disponiveis is None:
            return None
        
        return vagas_disponiveis == 0
    
    async def buscar_eventos_disponiveis(self) -> List[Dict[str, Any]]:
        """
        Lista eventos com status 'Aberto' e com vagas disponíveis
        
        Returns:
            Lista de eventos disponíveis para inscrição
        """
        await self.conectar()
        
        eventos = await self.db.evento.find_many(
            where={'status': 'Aberto'},
            include={'inscricoes': True},
            order={'data': 'asc'}
        )
        
        resultado = []
        for evento in eventos:
            total_inscricoes = len(evento.inscricoes) if evento.inscricoes else 0
            vagas_disponiveis = evento.vagas - total_inscricoes
            
            if vagas_disponiveis > 0:
                resultado.append({
                    'id': evento.id,
                    'nome': evento.nome,
                    'descricao': evento.descricao,
                    'data': evento.data,
                    'horario': evento.horario,
                    'local': evento.local,
                    'vagas': evento.vagas,
                    'tipo': evento.tipo,
                    'status': evento.status,
                    'total_inscricoes': total_inscricoes,
                    'vagas_disponiveis': vagas_disponiveis,
                    'criado_em': evento.criado_em
                })
        
        return resultado
    
    async def buscar_por_nome(self, termo_busca: str) -> List[Dict[str, Any]]:
        """
        Busca eventos por nome (busca parcial)
        
        Args:
            termo_busca: Termo para buscar no nome do evento
        
        Returns:
            Lista de eventos que correspondem à busca
        """
        await self.conectar()
        
        eventos = await self.db.evento.find_many(
            where={
                'nome': {
                    'contains': termo_busca,
                }
            },
            include={'inscricoes': True},
            order={'data': 'desc'}
        )
        
        resultado = []
        for evento in eventos:
            resultado.append({
                'id': evento.id,
                'nome': evento.nome,
                'descricao': evento.descricao,
                'data': evento.data,
                'horario': evento.horario,
                'local': evento.local,
                'vagas': evento.vagas,
                'tipo': evento.tipo,
                'status': evento.status,
                'total_inscricoes': len(evento.inscricoes) if evento.inscricoes else 0,
                'criado_em': evento.criado_em
            })
        
        return resultado
    
    async def obter_estatisticas_evento(self, evento_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém estatísticas detalhadas de um evento
        
        Args:
            evento_id: ID do evento
        
        Returns:
            Dicionário com estatísticas do evento ou None
        """
        await self.conectar()
        
        evento = await self.db.evento.find_unique(
            where={'id': evento_id},
            include={
                'inscricoes': {
                    'include': {
                        'participante': True
                    }
                }
            }
        )
        
        if not evento:
            return None
        
        total_inscricoes = len(evento.inscricoes) if evento.inscricoes else 0
        total_presentes = sum(1 for i in evento.inscricoes if i.presente) if evento.inscricoes else 0
        total_certificados = sum(1 for i in evento.inscricoes if i.certificado) if evento.inscricoes else 0
        vagas_disponiveis = evento.vagas - total_inscricoes
        taxa_ocupacao = (total_inscricoes / evento.vagas * 100) if evento.vagas > 0 else 0
        taxa_presenca = (total_presentes / total_inscricoes * 100) if total_inscricoes > 0 else 0
        
        return {
            'id': evento.id,
            'nome': evento.nome,
            'total_inscricoes': total_inscricoes,
            'total_presentes': total_presentes,
            'total_certificados': total_certificados,
            'vagas_totais': evento.vagas,
            'vagas_disponiveis': max(0, vagas_disponiveis),
            'taxa_ocupacao': round(taxa_ocupacao, 2),
            'taxa_presenca': round(taxa_presenca, 2),
            'status': evento.status
        }


# Funções auxiliares para uso síncrono (opcional)
def criar_manager():
    """Cria uma instância do EventoManager"""
    return EventoManager()
