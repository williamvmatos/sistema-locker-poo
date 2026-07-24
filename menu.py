from sistema.sistema_locker import SistemaLocker
from entidades.sindico import Sindico
from sistema import persistencia

def menu():

    sistema = SistemaLocker()
    sindico = Sindico("Sr. Roberto", chave_mestra=9999)

    while True:

        print("\n===== SISTEMA LOCKER =====")
        print("1 - Cadastrar morador")
        print("2 - Listar moradores")
        print("3 - Cadastrar entrega")
        print("4 - Retirar pacote")
        print("5 - Listar lockers")
        print("6 - Adicionar novo locker")
        print("7 - Ver histórico")
        print("8 - Acesso do síndico (chave mestra)")
        print("9 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            sistema.cadastrar_morador()

        elif opcao == "2":
            sistema.listar_moradores()

        elif opcao == "3":
            sistema.cadastrar_entrega()

        elif opcao == "4":
            sistema.retirar_pacote()

        elif opcao == "5":
            sistema.listar_lockers()

        elif opcao == "6":
            sistema.adicionar_locker()

        elif opcao == "7":
            sistema.listar_historico()

        elif opcao == "8":
            menu_sindico(sistema, sindico)

        elif opcao == "9":
            print("Sistema encerrado.")
            break

        else:
            print("Opção inválida.")

def menu_sindico(sistema, sindico):

    print(f"\n===== ACESSO DO SÍNDICO ({sindico.get_nome()}) =====")

    chave = sistema.ler_numero("Digite a chave mestra: ")

    if not sindico.verificar_chave(chave):
        print("Chave mestra incorreta. Acesso negado.")
        return

    while True:

        print("\n----- ADMINISTRAÇÃO DO SÍNDICO -----")
        print("1 - Ver lockers cadastrados")
        print("2 - Remover morador")
        print("3 - Abrir locker com chave mestra")
        print("4 - Voltar ao menu principal")

        opcao = input("Escolha: ")

        if opcao == "1":
            sistema.listar_lockers()

        elif opcao == "2":
            sistema.remover_morador()

        elif opcao == "3":
            _abrir_locker_com_chave_mestra(sistema)

        elif opcao == "4":
            break

        else:
            print("Opção inválida.")

def _abrir_locker_com_chave_mestra(sistema):

    numero = sistema.ler_numero("Número do locker para abrir: ")

    for locker in sistema.lockers:

        if locker.get_numero() == numero:

            morador_antes = None
            if locker.esta_ocupado():
                morador_antes = locker.get_entrega().get_morador().get_nome()

            sucesso = locker.abrir_com_chave_mestra()

            if sucesso:
                sistema._salvar()
                persistencia.salvar_registro(
                    "ABERTURA CHAVE MESTRA", numero, morador_antes or "-", ""
                )
            return

    print("Locker não encontrado.")
