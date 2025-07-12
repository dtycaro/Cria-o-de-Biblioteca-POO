from abc import ABC, abstractmethod



class Pessoa(ABC):
    def __init__(self, nome, cpf): # criamos a classe pessoa e damos a ela os atributos desejados 
        self.nome = nome
        self.cpf = cpf
 
    def get_nome(self):    # Método para acessar o nome
        return self.nome
    
    def get_cpf(self):     # Método para acessar o cpf
        return self.cpf

    @abstractmethod  # Método abstrato
    def tipo_pessoa(self):
        pass

    def __str__(self):  # Como o objeto será exibido com o print 
        return f"{self.tipo()} - Nome: {self._nome}, CPF: {self._cpf}"


class Leitor(Pessoa): # criamos a classe leitor e damos a ela os atributos desejados
    def __init__(self, nome, cpf, email):
        super().__init__(nome, cpf) # super faz herdar as caracteristicas (nesse caso de pessoa)
        self.email = email

    def get_email(self): # Método para acessar o email
        return self.email

    def tipo_pessoa(self):     # define o tipo como leitor 
        return "Leitor"


class Funcionario(Pessoa):      # criamos a classe pessoa e damos a ela os atributos desejados 
    def __init__(self, nome, cpf, cargo, matricula = None):
        super().__init__(nome, cpf) # super faz herdar as caracteristicas (nesse caso de pessoa)
        self.cargo = cargo
        self.matricula = matricula or cpf[-4:]
    def get_cargo(self):   # Método para acessar o cargo
        return self.cargo

    def tipo_pessoa(self):   # Define o tipo como "Funcionário"
        return "Funcionário"