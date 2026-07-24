from entidades.morador import Morador
from entidades.pacote import Pacote

class Entrega:

    def __init__(self, morador: Morador, pacote: Pacote):

        if not isinstance(morador, Morador):
            raise TypeError("morador deve ser um objeto da classe Morador.")

        if not isinstance(pacote, Pacote):
            raise TypeError("pacote deve ser um objeto da classe Pacote.")

        self.__morador = morador
        self.__pacote = pacote

    def get_morador(self) -> Morador:
        return self.__morador

    def get_pacote(self) -> Pacote:
        return self.__pacote
