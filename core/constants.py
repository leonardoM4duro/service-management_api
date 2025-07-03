# Mensagens de erro
class ErrorMessages:
    # Cliente
    CLIENT_NOT_FOUND = "Cliente não encontrado"
    CLIENT_DUPLICATE_EMAIL_PHONE = "Já existe um cliente com este e-mail ou telefone"
    CLIENT_LIST_ERROR = "Erro ao listar clientes"
    CLIENT_CREATE_ERROR = "Erro interno ao criar cliente"
    CLIENT_GET_ERROR = "Erro ao buscar cliente"
    CLIENT_UPDATE_ERROR = "Erro interno ao atualizar cliente"
    CLIENT_DELETE_ERROR = "Erro ao deletar cliente"
    
    # Material
    MATERIAL_NOT_FOUND = "Material não encontrado"
    MATERIAL_DUPLICATE_CODE_NAME = "Já existe um material com este código ou nome"
    MATERIAL_LIST_ERROR = "Erro ao listar materiais"
    MATERIAL_CREATE_ERROR = "Erro interno ao criar material"
    MATERIAL_GET_ERROR = "Erro ao buscar material"
    MATERIAL_UPDATE_ERROR = "Erro interno ao atualizar material"
    MATERIAL_DELETE_ERROR = "Erro ao deletar material"
    MATERIAL_LOW_STOCK_ERROR = "Erro ao buscar materiais com estoque baixo"
    MATERIAL_UPDATE_STOCK_ERROR = "Erro ao atualizar estoque"
    MATERIAL_SEARCH_CATEGORY_ERROR = "Erro ao buscar materiais por categoria"
    MATERIAL_NEGATIVE_QUANTITY = "A quantidade não pode ser negativa"
    MATERIAL_CODE_GENERATE_ERROR = "Erro ao gerar código do material"
    
    # Usuário
    USER_NOT_FOUND = "Usuário não encontrado"
    USER_DUPLICATE_EMAIL = "Já existe um usuário com este e-mail"
    USER_CREATE_ERROR = "Erro interno ao criar usuário"
    USER_GET_ERROR = "Erro ao buscar usuário"
    USER_UPDATE_ERROR = "Erro interno ao atualizar usuário"
    USER_DELETE_ERROR = "Erro ao deletar usuário"
    USER_AUTH_ERROR = "Erro na autenticação do usuário"
    
    # Ordem de Serviço
    SERVICE_ORDER_NOT_FOUND = "Ordem de serviço não encontrada"
    SERVICE_ORDER_LIST_ERROR = "Erro ao listar ordens de serviço"
    SERVICE_ORDER_CREATE_ERROR = "Erro interno ao criar ordem de serviço"
    SERVICE_ORDER_GET_ERROR = "Erro ao buscar ordem de serviço"
    SERVICE_ORDER_UPDATE_ERROR = "Erro interno ao atualizar ordem de serviço"
    SERVICE_ORDER_DELETE_ERROR = "Erro ao deletar ordem de serviço"
    SERVICE_ORDER_CLIENT_ORDERS_ERROR = "Erro ao buscar ordens de serviço do cliente"
    SERVICE_ORDER_USER_ORDERS_ERROR = "Erro ao buscar ordens de serviço do usuário"
    SERVICE_ORDER_ADD_MATERIAL_ERROR = "Erro ao adicionar material à ordem de serviço"
    SERVICE_ORDER_REMOVE_MATERIAL_ERROR = "Erro ao remover material da ordem de serviço"
    SERVICE_ORDER_UPDATE_MATERIAL_ERROR = "Erro ao atualizar material na ordem de serviço"
    SERVICE_ORDER_GET_MATERIALS_ERROR = "Erro ao buscar materiais da ordem de serviço"
    SERVICE_ORDER_MATERIAL_NOT_IN_ORDER = "Material não encontrado na ordem de serviço"
    USER_ASSIGNED_NOT_FOUND = "Usuário atribuído não encontrado"

# Mensagens de sucesso
class SuccessMessages:
    CLIENT_DELETED = "Cliente deletado com sucesso"
    MATERIAL_DELETED = "Material deletado com sucesso"
    USER_DELETED = "Usuário deletado com sucesso"
    SERVICE_ORDER_DELETED = "Ordem de serviço deletada com sucesso"

# Configurações de validação
class ValidationConfig:
    MIN_STOCK_LEVEL = 0
    MIN_NAME_PARTS = 2
    ORDER_NUMBER_PREFIX = "OS-"
    ORDER_NUMBER_FORMAT = "{prefix}{seq:04d}"
