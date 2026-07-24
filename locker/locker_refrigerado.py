from locker.lockers import Locker

class LockerRefrigerado(Locker):

    TEMPERATURA_IDEAL = 4  # graus Celsius, temperatura de conservação

    def exibir_tipo(self):
        print(f"Locker Refrigerado ({self.TEMPERATURA_IDEAL}°C)")

    def armazenar(self, entrega):
        sucesso = super().armazenar(entrega)

        if sucesso:
            print(f"Temperatura mantida a {self.TEMPERATURA_IDEAL}°C para conservação do produto.")

        return sucesso
