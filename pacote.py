class Pacote:

    def __init__(self, codigo: str, descricao: str):

        if not isinstance(codigo, str):
            raise TypeError("O código do pacote deve ser um texto (str).")

        if not isinstance(descricao, str):
            raise TypeError("A descrição do pacote deve ser um texto (str).")

        self.__codigo = codigo
        self.__descricao = descricao

    def get_codigo(self) -> str:
        return self.__codigo

    def get_descricao(self) -> str:
        return self.__descricao

    def __str__(self):
        return f"Código: {self.__codigo} | {self.__descricao}"