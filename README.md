# Sistema de Gerenciamento de Locker (POO)

Projeto da disciplina de Programação Orientada a Objetos. Um sistema pra gerenciar
lockers de entrega em condomínio: o morador recebe uma senha quando o pacote chega,
e usa ela pra retirar depois. O síndico também tem uma chave mestra pra abrir qualquer
locker em caso de necessidade.

## Conceitos de POO aplicados

- **Herança** — `LockerPequeno`, `LockerGrande` e `LockerRefrigerado` herdam de uma
  classe base `Locker`.
- **Polimorfismo** — cada tipo de locker se comporta de um jeito. O `LockerRefrigerado`,
  por exemplo, sobrescreve o método de armazenar pra simular controle de temperatura,
  além de mudar como ele se identifica.
- **Encapsulamento** — atributos privados (senha, ocupação, entrega) só acessíveis por
  métodos (getters), evitando alteração direta de fora da classe.
- **Composição** — a classe `Entrega` junta um `Morador` e um `Pacote` num objeto só.

## Funcionalidades

- Cadastro e listagem de moradores
- Cadastro de entregas (gera senha automática)
- Retirada de pacote por senha
- Acesso do síndico com chave mestra
- Histórico de operações
- Persistência dos dados em JSON (o sistema lembra o estado mesmo depois de fechar)
- Interface gráfica simples feita com Tkinter, além da versão por menu de texto

## Tecnologias

Python (POO), Tkinter (interface gráfica), JSON (persistência).

## Como rodar

```
python main.py
```

Ou, para abrir a versão com interface gráfica:

```
python gui.py
```
