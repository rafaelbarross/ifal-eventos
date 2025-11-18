"""Utilitário para ícones usando emojis Unicode"""

# Mapeamento de ícones usando emojis Unicode
ICONES = {
    'dashboard': '📊',
    'chart_line': '📈',
    'calendar': '📅',
    'users': '👥',
    'chart_bar': '📊',
    'gear': '⚙️',
    'settings': '⚙️',
    'right_from_bracket': '🚪',
    'logout': '🚪',
    'plus': '➕',
    'edit': '✏️',
    'trash': '🗑️',
    'search': '🔍',
    'file': '📄',
    'check': '✅',
    'times': '❌',
    'info': 'ℹ️',
    'warning': '⚠️',
}

def obter_icone(nome, estilo='solid', tamanho=20, cor="#1F2937"):
    """
    Retorna um emoji Unicode para usar como ícone
    
    Args:
        nome: Nome do ícone (ex: 'calendar', 'users', 'chart_line')
        estilo: Não usado, mantido para compatibilidade
        tamanho: Não usado, mantido para compatibilidade
        cor: Não usado, mantido para compatibilidade
    
    Returns:
        String com emoji ou None se não encontrado
    """
    return ICONES.get(nome, '•')
