from entidades.morador import Morador
from entidades.pacote import Pacote
from entidades.entrega import Entrega

from locker.locker_pequeno import LockerPequeno
from locker.locker_grande import LockerGrande
from locker.locker_refrigerado import LockerRefrigerado

from sistema import persistencia

class SistemaLocker:

    _TIPOS_LOCKER = {
        "LockerPequeno": LockerPequeno,
        "LockerGrande": LockerGrande,
        "LockerRefrigerado": LockerRefrigerado,
    }

    def __init__(self):

        estado = persistencia.carregar_estado()

        if estado is not None:
            self.lockers = self._reconstruir_lockers(estado["lockers"])
            self.moradores = self._reconstruir_moradores(estado["moradores"])
            print("Estado anterior carregado com sucesso.")
        else:
            self.lockers = [
                LockerPequeno(1),
                LockerGrande(2),
                LockerRefrigerado(3)
            ]
            self.moradores = []

    def _reconstruir_lockers(self, lockers_json: list) -> list:

        lockers = []

        for dados in lockers_json:

            classe = self._TIPOS_LOCKER.get(dados["tipo"], LockerPequeno)
            locker = classe(dados["numero"])

            if dados["ocupado"] and dados["entrega"] is not None:
                e = dados["entrega"]
                morador = Morador(e["morador_nome"], e["morador_apartamento"])
                pacote = Pacote(e["pacote_codigo"], e["pacote_descricao"])
                entrega = Entrega(morador, pacote)
                locker.restaurar_estado(True, dados["senha"], entrega)

            lockers.append(locker)

        return lockers

    def _reconstruir_moradores(self, moradores_json: list) -> list:
        return [
            Morador(m["nome"], m["apartamento"])
            for m in moradores_json
        ]

    def _salvar(self):
        persistencia.salvar_estado(self.lockers, self.moradores)

    def cadastrar_morador(self):

        print("\n===== CADASTRAR MORADOR =====")

        nome = self.ler_nome("Nome do morador: ")
        apartamento = self.ler_numero("Número do apartamento: ")

        for m in self.moradores:
            if m.get_apartamento() == apartamento:
                print(f"Já existe um morador cadastrado no apartamento {apartamento}: {m.get_nome()}.")
                return

        novo_morador = Morador(nome, apartamento)
        self.moradores.append(novo_morador)
        self._salvar()
        persistencia.salvar_registro("MORADOR CADASTRADO", "-", nome, f"Apto {apartamento}")
        print(f"Morador '{nome}' cadastrado com sucesso no apartamento {apartamento}.")

    def remover_morador(self):

        print("\n===== REMOVER MORADOR =====")

        if not self.moradores:
            print("Nenhum morador cadastrado.")
            return

        apartamento = self.ler_numero("Apartamento do morador a remover: ")
        morador = self._buscar_morador_por_apartamento(apartamento)

        if morador is None:
            print(f"Nenhum morador encontrado no apartamento {apartamento}.")
            return

        nome = morador.get_nome()

        lockers_pendentes = [
            locker for locker in self.lockers
            if locker.esta_ocupado()
            and locker.get_entrega().get_morador().get_apartamento() == apartamento
        ]

        self.moradores.remove(morador)
        self._salvar()
        persistencia.salvar_registro("MORADOR REMOVIDO", "-", nome, f"Apto {apartamento}")
        print(f"Morador '{nome}' removido do apartamento {apartamento}.")

        if lockers_pendentes:
            numeros = ", ".join(str(l.get_numero()) for l in lockers_pendentes)
            print(f"Atenção: há pacote(s) pendente(s) para esse morador no(s) locker(s) {numeros}.")
            print("Use a chave mestra para retirar o(s) pacote(s).")

    def listar_moradores(self):

        print("\n===== MORADORES CADASTRADOS =====")

        if not self.moradores:
            print("Nenhum morador cadastrado ainda.")
            return

        for morador in self.moradores:
            print(morador)
            print("-" * 30)

    def _buscar_morador_por_apartamento(self, apartamento: int):

        for morador in self.moradores:
            if morador.get_apartamento() == apartamento:
                return morador

        return None

    def listar_lockers(self):

        print("\n===== LOCKERS =====")

        for locker in self.lockers:

            print(
                f"Locker {locker.get_numero()}",
                end=" - "
            )

            locker.exibir_tipo()

            if locker.esta_ocupado():
                print("Status: Ocupado")
            else:
                print("Status: Livre")

            print("-" * 30)

    def adicionar_locker(self):

        print("\n===== ADICIONAR LOCKER =====")
        print("1 - Pequeno")
        print("2 - Grande")
        print("3 - Refrigerado")

        tipo = input("Escolha o tipo de locker: ")

        if self.lockers:
            proximo_numero = max(locker.get_numero() for locker in self.lockers) + 1
        else:
            proximo_numero = 1

        if tipo == "1":
            novo_locker = LockerPequeno(proximo_numero)
        elif tipo == "2":
            novo_locker = LockerGrande(proximo_numero)
        elif tipo == "3":
            novo_locker = LockerRefrigerado(proximo_numero)
        else:
            print("Tipo inválido. Nenhum locker foi adicionado.")
            return

        self.lockers.append(novo_locker)
        self._salvar()
        persistencia.salvar_registro("LOCKER ADICIONADO", proximo_numero, "-", type(novo_locker).__name__)
        print(f"Locker {proximo_numero} adicionado com sucesso.")

    def ler_numero(self, mensagem: str) -> int:

        while True:
            entrada = input(mensagem)

            try:
                return int(entrada)
            except ValueError:
                print("Entrada inválida. Digite apenas números, por favor.")

    def ler_nome(self, mensagem: str) -> str:

        while True:
            entrada = input(mensagem).strip()

            if entrada == "":
                print("Este campo não pode ficar em branco.")
                continue

            if entrada.isdigit():
                print("Entrada inválida. O nome não pode ser composto só por números.")
                continue

            return entrada

    def ler_texto(self, mensagem: str) -> str:

        while True:
            entrada = input(mensagem).strip()

            if entrada == "":
                print("Este campo não pode ficar em branco.")
                continue

            return entrada

    def cadastrar_entrega(self):

        if not self.moradores:
            print("Nenhum morador cadastrado. Cadastre um morador primeiro (opção 1).")
            return

        apartamento = self.ler_numero("Apartamento do destinatário: ")
        morador = self._buscar_morador_por_apartamento(apartamento)

        if morador is None:
            print(f"Apartamento {apartamento} não encontrado. Cadastre o morador primeiro.")
            return

        print(f"Morador encontrado: {morador.get_nome()}")

        codigo = self.ler_texto("Código do pacote: ")
        descricao = self.ler_texto("Descrição do pacote: ")

        pacote = Pacote(codigo, descricao)
        entrega = Entrega(morador, pacote)

        print("\nLockers disponíveis:")
        for locker in self.lockers:
            status = "Ocupado" if locker.esta_ocupado() else "Livre"
            print(f"  Locker {locker.get_numero()} - ", end="")
            locker.exibir_tipo()
            print(f"    Status: {status}")

        numeros = [locker.get_numero() for locker in self.lockers]
        menor = min(numeros)
        maior = max(numeros)

        numero = self.ler_numero(f"Escolha o locker ({menor}-{maior}): ")

        for locker in self.lockers:

            if locker.get_numero() == numero:
                locker.armazenar(entrega)
                self._salvar()
                persistencia.salvar_registro(
                    "ENTREGA", numero, morador.get_nome(), descricao
                )
                return

        print("Locker não encontrado.")

    def retirar_pacote(self):

        numero = self.ler_numero("Número do locker: ")
        senha = self.ler_numero("Digite a senha: ")

        for locker in self.lockers:

            if locker.get_numero() == numero:

                morador_antes = None
                if locker.esta_ocupado():
                    morador_antes = locker.get_entrega().get_morador().get_nome()

                sucesso = locker.retirar(senha)

                if sucesso and morador_antes:
                    self._salvar()
                    persistencia.salvar_registro(
                        "RETIRADA", numero, morador_antes, ""
                    )
                return

        print("Locker não encontrado.")

    def listar_historico(self):
        persistencia.listar_registros()
