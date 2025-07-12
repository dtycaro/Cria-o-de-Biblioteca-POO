# importando as bibliotecas necessárias
import tkinter as tk
from tkinter import ttk, messagebox
# importando a classe Biblioteca e exceções personalizadas
from modelos.biblioteca import Biblioteca
from modelos.excecoes import (
    LivroIndisponivelError,
    UsuarioInvalidoError,
    LimiteEmprestimosExcedidoError,
    LivroNaoEncontradoError,
    EmprestimoNaoEncontradoError
)

# criando a instância da biblioteca (é aqui que todo o sistema funciona)
biblioteca = Biblioteca()

# criando a janela principal
janela = tk.Tk()
janela.title("Sistema de Biblioteca")
janela.geometry("700x500")  # definindo o tamanho da janela

# criando o sistema de abas com Notebook (cada aba será uma função do sistema)
abas = ttk.Notebook(janela)
abas.pack(expand=1, fill="both")

# ------------------- ABA 1: CADASTRAR LIVRO -------------------
aba_livro = tk.Frame(abas)
abas.add(aba_livro, text="Cadastrar Livro")

# criando os campos de entrada para o livro
tk.Label(aba_livro, text="Título:").grid(row=0, column=0, sticky="e")
entry_titulo = tk.Entry(aba_livro)
entry_titulo.grid(row=0, column=1)

tk.Label(aba_livro, text="Autor:").grid(row=1, column=0, sticky="e")
entry_autor = tk.Entry(aba_livro)
entry_autor.grid(row=1, column=1)

tk.Label(aba_livro, text="Ano de Publicação:").grid(row=2, column=0, sticky="e")
entry_ano = tk.Entry(aba_livro)
entry_ano.grid(row=2, column=1)

tk.Label(aba_livro, text="Código:").grid(row=3, column=0, sticky="e")
entry_codigo = tk.Entry(aba_livro)
entry_codigo.grid(row=3, column=1)

# função que será executada ao clicar no botão "Cadastrar"
def cadastrar_livro():
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    ano = entry_ano.get()
    codigo = entry_codigo.get()

    try:
        biblioteca.cadastrar_livro(titulo, autor, int(ano), codigo)
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        entry_titulo.delete(0, tk.END)
        entry_autor.delete(0, tk.END)
        entry_ano.delete(0, tk.END)
        entry_codigo.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# botão para cadastrar o livro
tk.Button(aba_livro, text="Cadastrar Livro", command=cadastrar_livro).grid(row=4, column=0, columnspan=2, pady=10)

# ------------------- ABA 2: CADASTRAR LEITOR -------------------
aba_leitor = tk.Frame(abas)
abas.add(aba_leitor, text="Cadastrar Leitor")

tk.Label(aba_leitor, text="Nome:").grid(row=0, column=0, sticky="e")
entry_nome = tk.Entry(aba_leitor)
entry_nome.grid(row=0, column=1)

tk.Label(aba_leitor, text="CPF:").grid(row=1, column=0, sticky="e")
entry_cpf = tk.Entry(aba_leitor)
entry_cpf.grid(row=1, column=1)

tk.Label(aba_leitor, text="Email:").grid(row=2, column=0, sticky="e")
entry_email = tk.Entry(aba_leitor)
entry_email.grid(row=2, column=1)

def cadastrar_leitor():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    email = entry_email.get()

    try:
        biblioteca.cadastrar_leitor(nome, cpf, email)
        messagebox.showinfo("Sucesso", "Leitor cadastrado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_email.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

tk.Button(aba_leitor, text="Cadastrar Leitor", command=cadastrar_leitor).grid(row=3, column=0, columnspan=2, pady=10)

# ------------------- ABA 3: BUSCAR LIVRO -------------------
aba_busca = tk.Frame(abas)
abas.add(aba_busca, text="Buscar Livro")

tk.Label(aba_busca, text="Buscar por título ou autor:").pack()
entry_busca = tk.Entry(aba_busca)
entry_busca.pack()

listbox_busca = tk.Listbox(aba_busca, width=80)
listbox_busca.pack(pady=10)

def buscar_livro():
    termo = entry_busca.get()
    listbox_busca.delete(0, tk.END)
    livros = biblioteca.buscar_livro(termo)
    if livros:
        for livro in livros:
            status = "Disponível" if livro.disponivel else "Indisponível"
            listbox_busca.insert(tk.END, f"{livro.titulo} - {livro.autor} ({livro.ano_publicacao}) - {status}")
    else:
        listbox_busca.insert(tk.END, "Nenhum livro encontrado.")

tk.Button(aba_busca, text="Buscar", command=buscar_livro).pack(pady=5)

# ------------------- ABA 4: EMPRÉSTIMO -------------------
aba_emprestimo = tk.Frame(abas)
abas.add(aba_emprestimo, text="Realizar Empréstimo")

tk.Label(aba_emprestimo, text="Código do Livro:").grid(row=0, column=0)
entry_codigo_emp = tk.Entry(aba_emprestimo)
entry_codigo_emp.grid(row=0, column=1)

tk.Label(aba_emprestimo, text="CPF do Leitor:").grid(row=1, column=0)
entry_cpf_emp = tk.Entry(aba_emprestimo)
entry_cpf_emp.grid(row=1, column=1)

def realizar_emprestimo():
    codigo = entry_codigo_emp.get()
    cpf = entry_cpf_emp.get()
    try:
        emprestimo = biblioteca.realizar_emprestimo(codigo, cpf)
        data = emprestimo.data_prevista_devolucao().strftime("%d/%m/%Y")
        messagebox.showinfo("Sucesso", f"Empréstimo realizado!\nDevolução até: {data}")
    except (LivroIndisponivelError, UsuarioInvalidoError, LimiteEmprestimosExcedidoError, LivroNaoEncontradoError) as e:
        messagebox.showerror("Erro", str(e))

tk.Button(aba_emprestimo, text="Emprestar Livro", command=realizar_emprestimo).grid(row=2, column=0, columnspan=2, pady=10)

# ------------------- ABA 5: DEVOLUÇÃO -------------------
aba_devolucao = tk.Frame(abas)
abas.add(aba_devolucao, text="Devolver Livro")

tk.Label(aba_devolucao, text="Código do Livro:").pack()
entry_codigo_dev = tk.Entry(aba_devolucao)
entry_codigo_dev.pack()

def realizar_devolucao():
    codigo = entry_codigo_dev.get()
    try:
        biblioteca.realizar_devolucao(codigo)
        messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
    except EmprestimoNaoEncontradoError as e:
        messagebox.showerror("Erro", str(e))

tk.Button(aba_devolucao, text="Devolver", command=realizar_devolucao).pack(pady=10)

# ------------------- ABA 6: LISTAR LIVROS -------------------
aba_listar_livros = tk.Frame(abas)
abas.add(aba_listar_livros, text="Listar Livros")

listbox_livros = tk.Listbox(aba_listar_livros, width=80)
listbox_livros.pack(pady=10)

def atualizar_lista_livros():
    listbox_livros.delete(0, tk.END)
    for livro in biblioteca.listar_livros():
        status = "Disponível" if livro.disponivel else "Indisponível"
        listbox_livros.insert(tk.END, f"{livro.titulo} - {livro.autor} ({livro.ano_publicacao}) - {status}")

tk.Button(aba_listar_livros, text="Atualizar Lista", command=atualizar_lista_livros).pack()

# ------------------- ABA 7: LISTAR EMPRÉSTIMOS ATIVOS -------------------
aba_ativos = tk.Frame(abas)
abas.add(aba_ativos, text="Empréstimos Ativos")

listbox_ativos = tk.Listbox(aba_ativos, width=80)
listbox_ativos.pack(pady=10)

def atualizar_emprestimos_ativos():
    listbox_ativos.delete(0, tk.END)
    emprestimos = biblioteca.listar_emprestimos_ativos()
    if emprestimos:
        for emp in emprestimos:
            data = emp.data_prevista_devolucao().strftime("%d/%m/%Y")
            listbox_ativos.insert(tk.END, f"{emp.livro.titulo} para {emp.leitor.get_nome()} - Devolução: {data}")
    else:
        listbox_ativos.insert(tk.END, "Nenhum empréstimo ativo.")

tk.Button(aba_ativos, text="Atualizar Lista", command=atualizar_emprestimos_ativos).pack()

# iniciando o loop principal da interface
janela.mainloop()
