from prisma import Prisma
from datetime import datetime
from typing import List, Optional, Dict, Any


class ParticipanteManager:
    """Gerenciador de participantes usando Prisma ORM"""
    
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
    
    async def criar_participante(
        self,
        nome: str,
        cpf: str,
        email: str,
        curso: str,
        turma: str
    ) -> Dict[str, Any]:
        """
        Cria um novo participante
        
        Args:
            nome: Nome completo do participante
            cpf: CPF do participante (deve ser único)
            email: Email do participante
            curso: Curso do participante
            turma: Turma do participante
        
        Returns:
            Dicionário com os dados do participante criado
        
        Raises:
            Exception: Se o CPF já estiver cadastrado
        """
        await self.conectar()
        
        # Verificar se CPF já existe
        participante_existente = await self.db.participante.find_unique(
            where={'cpf': cpf}
        )
        
        if participante_existente:
            raise Exception(f"CPF {cpf} já está cadastrado!")
        
        participante = await self.db.participante.create(
            data={
                'nome': nome,
                'cpf': cpf,
                'email': email,
                'curso': curso,
                'turma': turma
            }
        )
        
        return {
            'id': participante.id,
            'nome': participante.nome,
            'cpf': participante.cpf,
            'email': participante.email,
            'curso': participante.curso,
            'turma': participante.turma,
            'criado_em': participante.criado_em
        }
    
    async def listar_participantes(
        self,
        curso: Optional[str] = None,
        turma: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lista todos os participantes com filtros opcionais
        
        Args:
            curso: Filtrar por curso (opcional)
            turma: Filtrar por turma (opcional)
        
        Returns:
            Lista de participantes
        """
        await self.conectar()
        
        where_clause = {}
        if curso:
            where_clause['curso'] = curso
        if turma:
            where_clause['turma'] = turma
        
        participantes = await self.db.participante.find_many(
            where=where_clause if where_clause else None,
            include={'inscricoes': True},
            order={'nome': 'asc'}
        )
        
        resultado = []
        for participante in participantes:
            resultado.append({
                'id': participante.id,
                'nome': participante.nome,
                'cpf': participante.cpf,
                'email': participante.email,
                'curso': participante.curso,
                'turma': participante.turma,
                'total_inscricoes': len(participante.inscricoes) if participante.inscricoes else 0,
                'criado_em': participante.criado_em
            })
        
        return resultado
    
    async def buscar_participante_por_id(self, participante_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca um participante específico por ID
        
        Args:
            participante_id: ID do participante
        
        Returns:
            Dicionário com os dados do participante ou None
        """
        await self.conectar()
        
        participante = await self.db.participante.find_unique(
            where={'id': participante_id},
            include={'inscricoes': {'include': {'evento': True}}}
        )
        
        if not participante:
            return None
        
        return {
            'id': participante.id,
            'nome': participante.nome,
            'cpf': participante.cpf,
            'email': participante.email,
            'curso': participante.curso,
            'turma': participante.turma,
            'total_inscricoes': len(participante.inscricoes) if participante.inscricoes else 0,
            'inscricoes': [
                {
                    'id': insc.id,
                    'evento_nome': insc.evento.nome if insc.evento else None,
                    'presente': insc.presente,
                    'certificado': insc.certificado,
                    'data_inscricao': insc.data_inscricao
                } for insc in participante.inscricoes
            ] if participante.inscricoes else [],
            'criado_em': participante.criado_em
        }
    
    async def buscar_participante_por_cpf(self, cpf: str) -> Optional[Dict[str, Any]]:
        """
        Busca um participante por CPF
        
        Args:
            cpf: CPF do participante
        
        Returns:
            Dicionário com os dados do participante ou None
        """
        await self.conectar()
        
        participante = await self.db.participante.find_unique(
            where={'cpf': cpf},
            include={'inscricoes': True}
        )
        
        if not participante:
            return None
        
        return {
            'id': participante.id,
            'nome': participante.nome,
            'cpf': participante.cpf,
            'email': participante.email,
            'curso': participante.curso,
            'turma': participante.turma,
            'total_inscricoes': len(participante.inscricoes) if participante.inscricoes else 0,
            'criado_em': participante.criado_em
        }
    
    async def atualizar_participante(
        self,
        participante_id: int,
        nome: Optional[str] = None,
        cpf: Optional[str] = None,
        email: Optional[str] = None,
        curso: Optional[str] = None,
        turma: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Atualiza um participante existente
        
        Args:
            participante_id: ID do participante
            nome: Novo nome (opcional)
            cpf: Novo CPF (opcional)
            email: Novo email (opcional)
            curso: Novo curso (opcional)
            turma: Nova turma (opcional)
        
        Returns:
            Dicionário com os dados do participante atualizado ou None
        
        Raises:
            Exception: Se o novo CPF já estiver cadastrado para outro participante
        """
        await self.conectar()
        
        # Verificar se o participante existe
        participante_existente = await self.db.participante.find_unique(
            where={'id': participante_id}
        )
        
        if not participante_existente:
            return None
        
        # Se está alterando o CPF, verificar se o novo CPF já existe
        if cpf and cpf != participante_existente.cpf:
            cpf_duplicado = await self.db.participante.find_unique(
                where={'cpf': cpf}
            )
            if cpf_duplicado:
                raise Exception(f"CPF {cpf} já está cadastrado para outro participante!")
        
        # Preparar dados para atualização
        dados_atualizacao = {}
        if nome is not None:
            dados_atualizacao['nome'] = nome
        if cpf is not None:
            dados_atualizacao['cpf'] = cpf
        if email is not None:
            dados_atualizacao['email'] = email
        if curso is not None:
            dados_atualizacao['curso'] = curso
        if turma is not None:
            dados_atualizacao['turma'] = turma
        
        participante = await self.db.participante.update(
            where={'id': participante_id},
            data=dados_atualizacao
        )
        
        return {
            'id': participante.id,
            'nome': participante.nome,
            'cpf': participante.cpf,
            'email': participante.email,
            'curso': participante.curso,
            'turma': participante.turma,
            'criado_em': participante.criado_em
        }
    
    async def deletar_participante(self, participante_id: int) -> bool:
        """
        Deleta um participante
        
        Args:
            participante_id: ID do participante
        
        Returns:
            True se deletado com sucesso, False se não encontrado
        """
        await self.conectar()
        
        try:
            # Verificar se o participante existe
            participante_existente = await self.db.participante.find_unique(
                where={'id': participante_id}
            )
            
            if not participante_existente:
                return False
            
            # Deletar inscrições relacionadas primeiro
            await self.db.inscricao.delete_many(
                where={'participante_id': participante_id}
            )
            
            # Deletar o participante
            await self.db.participante.delete(
                where={'id': participante_id}
            )
            
            return True
        except Exception as e:
            print(f"Erro ao deletar participante: {e}")
            return False
    
    async def buscar_por_nome(self, termo_busca: str) -> List[Dict[str, Any]]:
        """
        Busca participantes por nome (busca parcial)
        
        Args:
            termo_busca: Termo para buscar no nome
        
        Returns:
            Lista de participantes que correspondem à busca
        """
        await self.conectar()
        
        participantes = await self.db.participante.find_many(
            where={
                'nome': {
                    'contains': termo_busca,
                }
            },
            include={'inscricoes': True},
            order={'nome': 'asc'}
        )
        
        resultado = []
        for participante in participantes:
            resultado.append({
                'id': participante.id,
                'nome': participante.nome,
                'cpf': participante.cpf,
                'email': participante.email,
                'curso': participante.curso,
                'turma': participante.turma,
                'total_inscricoes': len(participante.inscricoes) if participante.inscricoes else 0,
                'criado_em': participante.criado_em
            })
        
        return resultado
    
    async def buscar_por_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca participante por email
        
        Args:
            email: Email do participante
        
        Returns:
            Dicionário com os dados do participante ou None
        """
        await self.conectar()
        
        participante = await self.db.participante.find_first(
            where={'email': email},
            include={'inscricoes': True}
        )
        
        if not participante:
            return None
        
        return {
            'id': participante.id,
            'nome': participante.nome,
            'cpf': participante.cpf,
            'email': participante.email,
            'curso': participante.curso,
            'turma': participante.turma,
            'total_inscricoes': len(participante.inscricoes) if participante.inscricoes else 0,
            'criado_em': participante.criado_em
        }
    
    async def listar_participantes_por_evento(self, evento_id: int) -> List[Dict[str, Any]]:
        """
        Lista todos os participantes inscritos em um evento específico
        
        Args:
            evento_id: ID do evento
        
        Returns:
            Lista de participantes inscritos no evento
        """
        await self.conectar()
        
        inscricoes = await self.db.inscricao.find_many(
            where={'evento_id': evento_id},
            include={'participante': True}
        )
        
        resultado = []
        for inscricao in inscricoes:
            if inscricao.participante:
                resultado.append({
                    'id': inscricao.participante.id,
                    'nome': inscricao.participante.nome,
                    'cpf': inscricao.participante.cpf,
                    'email': inscricao.participante.email,
                    'curso': inscricao.participante.curso,
                    'turma': inscricao.participante.turma,
                    'presente': inscricao.presente,
                    'certificado': inscricao.certificado,
                    'data_inscricao': inscricao.data_inscricao
                })
        
        return resultado
    
    async def obter_estatisticas_participante(self, participante_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém estatísticas de um participante
        
        Args:
            participante_id: ID do participante
        
        Returns:
            Dicionário com estatísticas ou None
        """
        await self.conectar()
        
        participante = await self.db.participante.find_unique(
            where={'id': participante_id},
            include={
                'inscricoes': {
                    'include': {
                        'evento': True
                    }
                }
            }
        )
        
        if not participante:
            return None
        
        total_inscricoes = len(participante.inscricoes) if participante.inscricoes else 0
        total_presencas = sum(1 for i in participante.inscricoes if i.presente) if participante.inscricoes else 0
        total_certificados = sum(1 for i in participante.inscricoes if i.certificado) if participante.inscricoes else 0
        taxa_presenca = (total_presencas / total_inscricoes * 100) if total_inscricoes > 0 else 0
        
        return {
            'id': participante.id,
            'nome': participante.nome,
            'total_inscricoes': total_inscricoes,
            'total_presencas': total_presencas,
            'total_certificados': total_certificados,
            'taxa_presenca': round(taxa_presenca, 2),
            'curso': participante.curso,
            'turma': participante.turma
        }


# Funções auxiliares para uso síncrono (opcional)
def criar_manager():
    """Cria uma instância do ParticipanteManager"""
    return ParticipanteManager()
