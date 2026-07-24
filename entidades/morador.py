class Morador:

    def __init__(self, nome: str, apartamento: int):

        if not isinstance(nome, str):
            raise TypeError("O nome do morador deve ser um texto (str).")

        if not isinstance(apartamento, int):
            raise TypeError("O apartamento deve ser um número inteiro (int).")

        self.__nome = nome
        self.__apartamento = apartamento

    def get_nome(self) -> str:
        return self.__nome

    def get_apartamento(self) -> int:
        return self.__apartamento

    def __str__(self):
        return f"{self.__nome} - Apto {self.__apartamento}"
