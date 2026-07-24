import random

from entidades.entrega import Entrega

class Locker:

    def __init__(self, numero: int):

        if not isinstance(numero, int):
            raise TypeError("O número do locker deve ser um número inteiro (int).")

        self.__numero = numero
        self.__ocupado = False
        self.__senha = None
        self.__entrega = None

    def get_numero(self) -> int:
        return self.__numero

    def esta_ocupado(self) -> bool:
        return self.__ocupado

    def get_entrega(self):
        return self.__entrega

    def get_senha(self) -> int:
        return self.__senha

    def armazenar(self, entrega: Entrega) -> bool:

        if not isinstance(entrega, Entrega):
            raise TypeError("entrega deve ser um objeto da classe Entrega.")

        if self.__ocupado:
            print("Locker ocupado.")
            return False

        self.__senha = random.randint(1000, 9999)
        self.__entrega = entrega
        self.__ocupado = True

        print("Pacote armazenado.")
        print(f"Senha de retirada: {self.__senha}")
        return True

    def retirar(self, senha: int) -> bool:

        if not isinstance(senha, int):
            raise TypeError("A senha deve ser um número inteiro (int).")

        if not self.__ocupado:
            print("Locker vazio.")
            return False

        if senha == self.__senha:

            print("\nPacote retirado com sucesso!")

            print(
                f"Morador: {self.__entrega.get_morador().get_nome()}"
            )

            print(
                f"Pacote: {self.__entrega.get_pacote().get_descricao()}"
            )

            self.__ocupado = False
            self.__senha = None
            self.__entrega = None
            return True

        else:
            print("Senha incorreta.")
            return False

    def restaurar_estado(self, ocupado: bool, senha, entrega):
        self.__ocupado = ocupado
        self.__senha = senha
        self.__entrega = entrega

    def abrir_com_chave_mestra(self) -> bool:

        if not self.__ocupado:
            print("Locker já está vazio.")
            return False

        print("\nLocker aberto com a chave mestra do síndico!")
        print(f"Morador: {self.__entrega.get_morador().get_nome()}")
        print(f"Pacote: {self.__entrega.get_pacote().get_descricao()}")

        self.__ocupado = False
        self.__senha = None
        self.__entrega = None
        return True

    def exibir_tipo(self):
        print("Locker Comum")