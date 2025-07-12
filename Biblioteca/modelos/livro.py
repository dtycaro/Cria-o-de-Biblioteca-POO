# essa classe que criei representa um livro na biblioteca
class Livro:
    def __init__(self, titulo: str, autor: str, ano_publicacao: int, codigo: str, disponivel: bool = True):
        # aqui estou guardando os dados básicos do livro quando ele é criado
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.codigo = codigo
        self.disponivel = disponivel  # por padrão, o livro já começa disponível na biblioteca

    
    # métodos que usei para fazer o livro ser emprestado ou devolvido
    def emprestar(self):
        # se o livro já estiver emprestado, não pode emprestar de novo
        if not self.disponivel:
            raise ValueError("Livro não está disponível para empréstimo")
        self.disponivel = False  # marca o livro como emprestado

    def devolver(self):
        self.disponivel = True  # quando devolvido, volta a ficar disponível

    # esse método é só pra exibir o livro de forma mais bonita no terminal
    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.ano_publicacao})"


    
