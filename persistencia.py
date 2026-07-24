import json
import os
from datetime import datetime

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAMINHO_ESTADO = os.path.join(PASTA_PROJETO, "estado.json")
CAMINHO_HISTORICO = os.path.join(PASTA_PROJETO, "historico.json")

def salvar_estado(lockers, moradores):
    dados = {
        "lockers": [],
        "moradores": []
    }

    for locker in lockers:

        entrega_dict = None

        if locker.esta_ocupado() and locker.get_entrega() is not None:
            entrega = locker.get_entrega()
            entrega_dict = {
                "morador_nome": entrega.get_morador().get_nome(),
                "morador_apartamento": entrega.get_morador().get_apartamento(),
                "pacote_codigo": entrega.get_pacote().get_codigo(),
                "pacote_descricao": entrega.get_pacote().get_descricao()
            }

        dados["lockers"].append({
            "numero": locker.get_numero(),
            "tipo": type(locker).__name__,
            "ocupado": locker.esta_ocupado(),
            "senha": locker.get_senha(),
            "entrega": entrega_dict
        })

    for morador in moradores:
        dados["moradores"].append({
            "nome": morador.get_nome(),
            "apartamento": morador.get_apartamento()
        })

    with open(CAMINHO_ESTADO, mode="w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

def carregar_estado():
    if not os.path.exists(CAMINHO_ESTADO):
        return None

    with open(CAMINHO_ESTADO, mode="r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def carregar_historico() -> list:
    if not os.path.exists(CAMINHO_HISTORICO):
        return []

    with open(CAMINHO_HISTORICO, mode="r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_registro(acao, numero_locker, morador, pacote):
    historico = carregar_historico()

    historico.append({
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "acao": acao,
        "locker": numero_locker,
        "morador": morador,
        "pacote": pacote
    })

    with open(CAMINHO_HISTORICO, mode="w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, ensure_ascii=False, indent=2)

def listar_registros():
    historico = carregar_historico()

    print("\n===== HISTÓRICO =====")

    if not historico:
        print("Nenhum registro encontrado ainda.")
        return

    for r in historico:
        print(f"[{r['data_hora']}] {r['acao']} - Locker {r['locker']} - {r['morador']} - {r['pacote']}")
        print("-" * 30)
