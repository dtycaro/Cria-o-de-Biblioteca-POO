#serve para mostrar o dia e calcular a data da devolução
from datetime import datetime, timedelta
#importando as excecoes personalizadas 
from .excecoes import LivroIndisponivelError, UsuarioInvalidoError
#aqui estou importanto das classes que criei em outra parte do cod para usar no emprestimo
from .livro import Livro
from .pessoa import Leitor

#criei a classe emprestimo e estou recebendo livro e leitor como objeto (obs-> usar ":" em vez de "="), e coloquei prazo de 15 dias para o emprestimo
class Emprestimo:
    def __init__(self, livro: Livro, leitor: Leitor, dias_emprestimo: int = 15):
        self.livro = livro #objeto da classe Livro
        self._leitor = leitor #objeto da classe Leitor
        self.data_emprestimo = datetime.now() # data do empréstimo no momento da criação
        self.data_devolucao = None # coloquei none pq será preenchida quando devolver
        self.dias_emprestimo = dias_emprestimo
        self._devolvido = False
    
  
    
    @property   #estou usando esse método para manter o nome do leitor protegido
    def leitor(self):
        return self._leitor
    @property
    def devolvido(self):
        return self._devolvido

    
 
   #esse metodo calcula a data final do emprestimo adicionando os dias ao dia atual
    def data_prevista_devolucao(self) -> datetime:
        return self.data_emprestimo + timedelta(days=self.dias_emprestimo)
    
    
#esse metodo aqui primeiramente marca o emprestimo como devolvido agora, atualiza o status dele chamando o metodo devolver do objeto livro
    def devolver(self):
        self.data_devolucao = datetime.now()
        self._devolvido = True #estou usando o devolvido como privado pq o  atributo representa um estado interno que não deveria ser alterado diretamente de fora da classe, então usei o metodo devolver para modifa-lo :)
        self.livro.devolver()
    
#aqui vou usar as excecoes que criei 
    @classmethod
    def criar(cls, livro, leitor, dias_emprestimo=15):
        if livro is None:
            raise ValueError("Livro não encontrado.")
        if leitor is None:
            raise UsuarioInvalidoError()
        if not livro.disponivel:
            raise LivroIndisponivelError()
        
        livro.emprestar()
        return cls(livro, leitor, dias_emprestimo)



    def __str__(self):
        status = "Devolvido" if self._devolvido else "Em empréstimo"
        return f"Empréstimo: {self.livro.titulo} para {self._leitor.nome} - {status}"