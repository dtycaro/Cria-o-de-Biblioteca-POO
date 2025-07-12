# importando a classe principal do sistema e as exceções que podem acontecer
from modelos.biblioteca import Biblioteca
from modelos.excecoes import LivroIndisponivelError, UsuarioInvalidoError

# essa é a função principal, onde tudo vai acontecer
def main():
    biblioteca = Biblioteca()  # cria a biblioteca e já carrega os dados dos arquivos

    # esse while vai manter o sistema rodando até o usuário escolher sair
    while True:
        # aqui é o menu que aparece sempre que termina uma ação
        print("\n--- Sistema de Gestão de Biblioteca ---")
        print("1. Cadastrar Livro")
        print("2. Cadastrar Leitor")
        print("3. Buscar Livro")
        print("4. Realizar Empréstimo")
        print("5. Realizar Devolução")
        print("6. Listar Livros")
        print("7. Listar Empréstimos Ativos")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        # CADASTRAR LIVRO
        if opcao == "1":
            print("\nCadastro de Livro")
            titulo = input("Título: ")
            autor = input("Autor: ")
            ano = int(input("Ano de Publicação: "))
            codigo = input("Código: ")
            biblioteca.cadastrar_livro(titulo, autor, ano, codigo)
            print("Livro cadastrado com sucesso!")

        # CADASTRAR LEITOR
        elif opcao == "2":
            print("\nCadastro de Leitor")
            nome = input("Nome: ")
            cpf = input("CPF: ")
            email = input("Email (opcional): ") or None
            biblioteca.cadastrar_leitor(nome, cpf, email)
            print("Leitor cadastrado com sucesso!")

        # BUSCAR LIVRO
        elif opcao == "3":
            termo = input("\nDigite título ou autor para busca: ")
            livros = biblioteca.buscar_livro(termo)
            if livros:
                print("\nLivros encontrados:")
                for livro in livros:
                    disp = "Disponível" if livro.disponivel else "Indisponível"
                    print(f"- {livro.titulo} ({livro.autor}) - {disp}")
            else:
                print("Nenhum livro encontrado.")

        # FAZER EMPRÉSTIMO
        elif opcao == "4":
            print("\nRealizar Empréstimo")
            codigo = input("Código do livro: ")
            cpf = input("CPF do leitor: ")
            try:
                emprestimo = biblioteca.realizar_emprestimo(codigo, cpf)
                print(f"Empréstimo realizado: {emprestimo.livro.titulo}")
                print(f"Data de devolução: {emprestimo.data_prevista_devolucao.strftime('%d/%m/%Y')}")
            # se alguma exceção acontecer, já mostramos o erro pro usuário
            except (ValueError, LivroIndisponivelError, UsuarioInvalidoError, LimiteEmprestimosExcedidoError) as e:
                print(f"Erro: {str(e)}")

        # FAZER DEVOLUÇÃO
        elif opcao == "5":
            print("\nRealizar Devolução")
            codigo = input("Código do livro: ")
            try:
                emprestimo = biblioteca.realizar_devolucao(codigo)
                print(f"Livro {emprestimo.livro.titulo} devolvido com sucesso!")
            except ValueError as e:
                print(f"Erro: {str(e)}")

        # LISTAR LIVROS
        elif opcao == "6":
            print("\nLista de Livros:")
            for livro in biblioteca.listar_livros():
                disp = "Disponível" if livro.disponivel else "Indisponível"
                print(f"- {livro.titulo} ({livro.autor}) - {disp}")

        # LISTAR EMPRÉSTIMOS ATIVOS
        elif opcao == "7":
            print("\nEmpréstimos Ativos:")
            emprestimos = biblioteca.listar_emprestimos_ativos()
            if emprestimos:
                for emp in emprestimos:
                    print(f"- {emp.livro.titulo} para {emp.leitor.nome}")
                    print(f"  Data prevista devolução: {emp.data_prevista_devolucao.strftime('%d/%m/%Y')}")
            else:
                print("Nenhum empréstimo ativo.")

        # SAIR DO SISTEMA
        elif opcao == "0":
            print("Saindo do sistema...")
            break

        # OPÇÃO INVÁLIDA
        else:
            print("Opção inválida. Tente novamente.")

# aqui o programa começa de fato quando você roda ele
if __name__ == "__main__":
    main()
