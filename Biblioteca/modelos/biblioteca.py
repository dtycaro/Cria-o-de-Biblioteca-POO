# importando json pra salvar e carregar os dados 
import json
# importando Path pra lidar com diretórios e arquivos
from pathlib import Path

# importando as classes de outros arquivos pra poder usar aqui
from modelos.livro import Livro
from modelos.pessoa import Leitor, Funcionario
from modelos.emprestimo import Emprestimo
from modelos.excecoes import (
    LivroIndisponivelError,
    UsuarioInvalidoError,
    LimiteEmprestimosExcedidoError,
    LivroNaoEncontradoError,
    EmprestimoNaoEncontradoError
)

# criei a classe Biblioteca, onde vai acontecer toda a "administração"
class Biblioteca:
    MAX_EMPRESTIMOS = 3  # limite de livros que um leitor pode pegar

    def __init__(self):
        self._livros = []        # lista de todos os livros cadastrados
        self._usuarios = []      # lista de leitores e funcionários
        self._emprestimos = []   # aqui ficam os empréstimos feitos
        self._carregar_dados()   # ao iniciar, já carrega os dados dos arquivos

    # esse método é chamado logo no começo e carrega os dados dos arquivos .json
    def _carregar_dados(self):
        dados_dir = Path(__file__).parent.parent / "dados"  # caminho da pasta "dados"

        # carregando livros
        livros_path = dados_dir / "livros.json"
        if livros_path.exists():
            with open(livros_path, 'r') as f:
                livros_data = json.load(f)
                self._livros = [Livro(**data) for data in livros_data]

        # carregando usuários (leitor ou funcionário)
        usuarios_path = dados_dir / "usuarios.json"
        if usuarios_path.exists():
            with open(usuarios_path, 'r') as f:
                usuarios_data = json.load(f)
                for data in usuarios_data:
                    # verifica o tipo da pessoa salvo no arquivo e reconstrói o objeto corretamente
                    if data['tipo'] == 'Leitor':
                        self._usuarios.append(Leitor(
                            data['nome'],
                            data['cpf'],
                            data.get('email')  # email pode ser None
                        ))
                    elif data['tipo'] == 'Funcionario':
                        self._usuarios.append(Funcionario(
                            data['nome'],
                            data['cpf'],
                            data.get('cargo', 'Bibliotecário'),  # se não tiver, assume "Bibliotecário"
                            data.get('matricula')  # matrícula também pode estar ausente
                        ))

        # carregando empréstimos (ainda será implementado)
        emprestimos_path = dados_dir / "emprestimos.json"
        if emprestimos_path.exists():
            with open(emprestimos_path, 'r') as f:
                emprestimos_data = json.load(f)
                # ainda falta reconstruir os empréstimos a partir do json

    # esse método salva tudo em arquivo sempre que tiver alguma alteração
    def _salvar_dados(self):
        dados_dir = Path(__file__).parent.parent / "dados"
        dados_dir.mkdir(exist_ok=True)  # se a pasta não existir, cria ela

        # salvando livros
        livros_data = [{
            'titulo': livro.titulo,
            'autor': livro.autor,
            'ano_publicacao': livro.ano_publicacao,
            'codigo': livro.codigo,
            'disponivel': livro.disponivel
        } for livro in self._livros]
        with open(dados_dir / "livros.json", 'w') as f:
            json.dump(livros_data, f, indent=2)

        # salvando usuários
        usuarios_data = []
        for usuario in self._usuarios:
            data = {
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'tipo': usuario.tipo_pessoa()  # garante que o tipo seja 'Leitor' ou 'Funcionario'
            }
            if isinstance(usuario, Leitor):
                data['email'] = usuario.email
            elif isinstance(usuario, Funcionario):
                data['cargo'] = usuario.cargo
                data['matricula'] = usuario.matricula
            usuarios_data.append(data)
        with open(dados_dir / "usuarios.json", 'w') as f:
            json.dump(usuarios_data, f, indent=2)

        # ainda falta salvar os empréstimos (parte ainda não implementada)
        emprestimos_data = []
        with open(dados_dir / "emprestimos.json", 'w') as f:
            json.dump(emprestimos_data, f, indent=2)

    # função pra cadastrar um livro novo
    def cadastrar_livro(self, titulo: str, autor: str, ano: int, codigo: str) -> Livro:
        livro = Livro(titulo, autor, ano, codigo)
        self._livros.append(livro)
        self._salvar_dados()
        return livro

    # função pra cadastrar um leitor (poderia também cadastrar funcionário)
    def cadastrar_leitor(self, nome: str, cpf: str, email: str = None) -> Leitor:
        leitor = Leitor(nome, cpf, email)
        self._usuarios.append(leitor)
        self._salvar_dados()
        return leitor

    # buscar livro pelo nome ou autor (usando o termo digitado)
    def buscar_livro(self, termo: str) -> list[Livro]:
        termo = termo.lower()
        return [livro for livro in self._livros 
                if termo in livro.titulo.lower() or termo in livro.autor.lower()]

    # buscar uma pessoa pelo CPF
    def buscar_usuario(self, cpf: str):
        for usuario in self._usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None  # se não achar, retorna nada

    # função principal pra realizar o empréstimo de um livro
    def realizar_emprestimo(self, codigo_livro: str, cpf_leitor: str) -> Emprestimo:
        # procura o livro pelo código
        livro = next((l for l in self._livros if l.codigo == codigo_livro), None)
        if not livro:
            raise LivroNaoEncontradoError()  # lança exceção se não achar o livro

        # verifica se o livro está disponível
        if not livro.disponivel:
            raise LivroIndisponivelError(f"O livro {livro.titulo} não está disponível")

        # procura o leitor pelo CPF
        leitor = self.buscar_usuario(cpf_leitor)
        if not leitor or not isinstance(leitor, Leitor):
            raise UsuarioInvalidoError("Leitor não encontrado ou inválido")

        # verifica se o leitor já atingiu o limite de empréstimos
        if len(leitor.emprestimos_ativos) >= self.MAX_EMPRESTIMOS:
            raise LimiteEmprestimosExcedidoError("Limite de empréstimos atingido")

        # tudo certo, cria o empréstimo
        emprestimo = Emprestimo(livro, leitor)
        livro.emprestar()
        leitor.adicionar_emprestimo(emprestimo)
        self._emprestimos.append(emprestimo)
        self._salvar_dados()

        return emprestimo

    # aqui devolve o livro e marca como devolvido
    def realizar_devolucao(self, codigo_livro: str) -> Emprestimo:
        emprestimo = next((e for e in self._emprestimos 
                          if e.livro.codigo == codigo_livro and not e.devolvido), None)
        if not emprestimo:
            raise EmprestimoNaoEncontradoError()  # se não achar, ou já foi devolvido, lança erro

        emprestimo.devolver()
        self._salvar_dados()
        return emprestimo

    # retorna a lista com todos os livros cadastrados
    def listar_livros(self) -> list[Livro]:
        return self._livros

    # retorna todos os usuários da biblioteca
    def listar_usuarios(self) -> list:
        return self._usuarios

    # mostra só os empréstimos que ainda não foram devolvidos
    def listar_emprestimos_ativos(self) -> list[Emprestimo]:
        return [e for e in self._emprestimos if not e.devolvido]
