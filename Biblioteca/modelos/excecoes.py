# esse arquivo guarda todas as exceções personalizadas do sistema
# serve pra deixar o tratamento de erros mais organizado e com mensagens claras

# exceção usada quando alguém tenta pegar um livro que já está emprestado
class LivroIndisponivelError(Exception):
    def __init__(self, mensagem="Livro já está emprestado."):
        super().__init__(mensagem)

# exceção para quando o CPF informado não está cadastrado ou é de um tipo errado de usuário
class UsuarioInvalidoError(Exception):
    def __init__(self, mensagem="Usuário não encontrado."):
        super().__init__(mensagem)

# exceção para quando o leitor já atingiu o número máximo de empréstimos ativos
class LimiteEmprestimosExcedidoError(Exception):
    def __init__(self, mensagem="O leitor atingiu o limite de empréstimos."):
        super().__init__(mensagem)

# exceção para quando tentam buscar ou devolver um livro com um código que não existe
class LivroNaoEncontradoError(Exception):
    def __init__(self, mensagem="Livro não encontrado no sistema."):
        super().__init__(mensagem)

# exceção para quando não é possível localizar o empréstimo do livro (ex: já foi devolvido)
class EmprestimoNaoEncontradoError(Exception):
    def __init__(self, mensagem="Empréstimo não encontrado ou já devolvido."):
        super().__init__(mensagem)

# exceção opcional, caso você queira validar CPF duplicado ou com formato inválido
class CPFInvalidoError(Exception):
    def __init__(self, mensagem="CPF inválido ou já cadastrado."):
        super().__init__(mensagem)
