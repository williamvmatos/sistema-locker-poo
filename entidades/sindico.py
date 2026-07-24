from locker.lockers import Locker

class Sindico:

    def __init__(self, nome: str, chave_mestra: int):

        if not isinstance(nome, str):
            raise TypeError("O nome do síndico deve ser um texto (str).")

        if not isinstance(chave_mestra, int):
            raise TypeError("A chave mestra deve ser um número inteiro (int).")

        self.__nome = nome
        self.__chave_mestra = chave_mestra

    def get_nome(self) -> str:
        return self.__nome

    def verificar_chave(self, chave_informada: int) -> bool:

        if not isinstance(chave_informada, int):
            raise TypeError("A chave informada deve ser um número inteiro (int).")

        return chave_informada == self.__chave_mestra

    def abrir_locker(self, locker: Locker, chave_informada: int) -> bool:

        if not isinstance(locker, Locker):
            raise TypeError("locker deve ser um objeto da classe Locker.")

        if not isinstance(chave_informada, int):
            raise TypeError("A chave informada deve ser um número inteiro (int).")

        if chave_informada != self.__chave_mestra:
            print("Chave mestra incorreta. Acesso negado.")
            return False

        return locker.abrir_com_chave_mestra()

    def __str__(self):
        return f"Síndico: {self.__nome}"
