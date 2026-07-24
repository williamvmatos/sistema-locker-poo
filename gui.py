import tkinter as tk
from tkinter import messagebox, simpledialog

from sistema.sistema_locker import SistemaLocker
from entidades.sindico import Sindico

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Sistema Locker")
        self.geometry("700x500")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        self.sistema = SistemaLocker()
        self.sindico = Sindico("Sr. Roberto", chave_mestra=9999)

        self._montar_tela()

    def _montar_tela(self):

        painel = tk.Frame(self, bg="#2c3e50", width=200)
        painel.pack(side="left", fill="y")
        painel.pack_propagate(False)

        tk.Label(
            painel,
            text="SISTEMA\nLOCKER",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 14, "bold"),
            pady=20
        ).pack()

        botoes = [
            ("Cadastrar Morador",  self._cadastrar_morador),
            ("Listar Moradores",   self._listar_moradores),
            ("Cadastrar Entrega",  self._cadastrar_entrega),
            ("Retirar Pacote",     self._retirar_pacote),
            ("Listar Lockers",     self._listar_lockers),
            ("Adicionar Locker",   self._adicionar_locker),
            ("Ver Histórico",      self._ver_historico),
            ("Acesso do Síndico",  self._acesso_sindico),
        ]

        for texto, comando in botoes:
            tk.Button(
                painel,
                text=texto,
                command=comando,
                bg="#3498db",
                fg="white",
                font=("Arial", 10),
                relief="flat",
                padx=10,
                pady=8,
                width=18,
                cursor="hand2"
            ).pack(pady=4, padx=10)

        area = tk.Frame(self, bg="#f0f0f0")
        area.pack(side="right", fill="both", expand=True)

        tk.Label(
            area,
            text="Saída do sistema",
            bg="#f0f0f0",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.saida = tk.Text(
            area,
            font=("Courier", 10),
            bg="white",
            relief="solid",
            state="disabled"
        )
        self.saida.pack(fill="both", expand=True, padx=10, pady=10)

        self._escrever("Sistema iniciado. Escolha uma ação no painel à esquerda.\n")

        if self.sistema.moradores or len(self.sistema.lockers) > 3:
            self._escrever("Estado anterior carregado do arquivo estado.json.\n")

    def _escrever(self, texto: str):
        self.saida.configure(state="normal")
        self.saida.insert("end", texto)
        self.saida.see("end")
        self.saida.configure(state="disabled")

    def _pedir_texto(self, titulo, pergunta) -> str:
        valor = simpledialog.askstring(titulo, pergunta, parent=self)
        return valor.strip() if valor else ""

    def _pedir_numero(self, titulo, pergunta) -> int:
        while True:
            valor = simpledialog.askstring(titulo, pergunta, parent=self)

            if valor is None:
                return None

            try:
                return int(valor.strip())
            except ValueError:
                messagebox.showerror("Entrada inválida", "Digite apenas números inteiros.")

    def _cadastrar_morador(self):

        nome = self._pedir_texto("Cadastrar Morador", "Nome do morador:")
        if not nome:
            return
        if nome.isdigit():
            messagebox.showerror("Inválido", "O nome não pode ser só números.")
            return

        apartamento = self._pedir_numero("Cadastrar Morador", "Número do apartamento:")
        if apartamento is None:
            return

        for m in self.sistema.moradores:
            if m.get_apartamento() == apartamento:
                messagebox.showwarning("Duplicado", f"Já existe morador no apartamento {apartamento}: {m.get_nome()}.")
                return

        from entidades.morador import Morador
        from sistema import persistencia

        novo = Morador(nome, apartamento)
        self.sistema.moradores.append(novo)
        self.sistema._salvar()
        persistencia.salvar_registro("MORADOR CADASTRADO", "-", nome, f"Apto {apartamento}")

        self._escrever(f"[MORADOR] '{nome}' cadastrado no apartamento {apartamento}.\n")

    def _listar_moradores(self):

        self._escrever("\n--- MORADORES CADASTRADOS ---\n")

        if not self.sistema.moradores:
            self._escrever("Nenhum morador cadastrado ainda.\n")
            return

        for m in self.sistema.moradores:
            self._escrever(f"  {m}\n")

    def _cadastrar_entrega(self):

        if not self.sistema.moradores:
            messagebox.showwarning("Atenção", "Cadastre um morador primeiro.")
            return

        apartamento = self._pedir_numero("Cadastrar Entrega", "Apartamento do destinatário:")
        if apartamento is None:
            return

        morador = self.sistema._buscar_morador_por_apartamento(apartamento)
        if morador is None:
            messagebox.showerror("Não encontrado", f"Apartamento {apartamento} não cadastrado.")
            return

        codigo = self._pedir_texto("Cadastrar Entrega", "Código do pacote:")
        if not codigo:
            return

        descricao = self._pedir_texto("Cadastrar Entrega", "Descrição do pacote:")
        if not descricao:
            return

        numeros = [l.get_numero() for l in self.sistema.lockers]
        numero = self._pedir_numero(
            "Cadastrar Entrega",
            f"Número do locker ({min(numeros)}-{max(numeros)}):"
        )
        if numero is None:
            return

        from entidades.pacote import Pacote
        from entidades.entrega import Entrega
        from sistema import persistencia

        pacote = Pacote(codigo, descricao)
        entrega = Entrega(morador, pacote)

        for locker in self.sistema.lockers:
            if locker.get_numero() == numero:
                sucesso = locker.armazenar(entrega)
                if sucesso:
                    self.sistema._salvar()
                    persistencia.salvar_registro("ENTREGA", numero, morador.get_nome(), descricao)
                    senha = locker.get_senha()
                    self._escrever(f"[ENTREGA] Locker {numero} | {morador.get_nome()} | {descricao}\n")
                    messagebox.showinfo("Senha de retirada", f"Anote a senha: {senha}")
                else:
                    messagebox.showerror("Erro", "Locker ocupado ou inválido.")
                return

        messagebox.showerror("Erro", "Locker não encontrado.")

    def _retirar_pacote(self):

        numero = self._pedir_numero("Retirar Pacote", "Número do locker:")
        if numero is None:
            return

        senha = self._pedir_numero("Retirar Pacote", "Senha de retirada:")
        if senha is None:
            return

        from sistema import persistencia

        for locker in self.sistema.lockers:
            if locker.get_numero() == numero:
                morador_antes = None
                if locker.esta_ocupado():
                    morador_antes = locker.get_entrega().get_morador().get_nome()

                sucesso = locker.retirar(senha)

                if sucesso:
                    self.sistema._salvar()
                    persistencia.salvar_registro("RETIRADA", numero, morador_antes, "")
                    self._escrever(f"[RETIRADA] Locker {numero} | {morador_antes}\n")
                    messagebox.showinfo("Sucesso", "Pacote retirado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Senha incorreta ou locker vazio.")
                return

        messagebox.showerror("Erro", "Locker não encontrado.")

    def _listar_lockers(self):

        self._escrever("\n--- LOCKERS ---\n")

        for locker in self.sistema.lockers:
            status = "Ocupado" if locker.esta_ocupado() else "Livre"
            self._escrever(f"  Locker {locker.get_numero()} | {type(locker).__name__} | {status}\n")

    def _adicionar_locker(self):

        tipo = self._pedir_texto(
            "Adicionar Locker",
            "Tipo de locker:\n1 - Pequeno\n2 - Grande\n3 - Refrigerado\n\nDigite 1, 2 ou 3:"
        )

        from locker.locker_pequeno import LockerPequeno
        from locker.locker_grande import LockerGrande
        from locker.locker_refrigerado import LockerRefrigerado
        from sistema import persistencia

        if self.sistema.lockers:
            proximo = max(l.get_numero() for l in self.sistema.lockers) + 1
        else:
            proximo = 1

        mapa = {"1": LockerPequeno, "2": LockerGrande, "3": LockerRefrigerado}

        if tipo not in mapa:
            messagebox.showerror("Inválido", "Digite 1, 2 ou 3.")
            return

        novo_locker = mapa[tipo](proximo)
        self.sistema.lockers.append(novo_locker)
        self.sistema._salvar()
        persistencia.salvar_registro("LOCKER ADICIONADO", proximo, "-", type(novo_locker).__name__)

        self._escrever(f"[LOCKER] Locker {proximo} ({type(novo_locker).__name__}) adicionado.\n")

    def _ver_historico(self):

        from sistema import persistencia

        self._escrever("\n--- HISTÓRICO ---\n")

        historico = persistencia.carregar_historico()

        if not historico:
            self._escrever("Nenhum registro ainda.\n")
            return

        for r in historico:
            self._escrever(f"  [{r['data_hora']}] {r['acao']} | Locker {r['locker']} | {r['morador']} | {r['pacote']}\n")

    def _acesso_sindico(self):

        chave = self._pedir_numero("Síndico", "Digite a chave mestra:")
        if chave is None:
            return

        if not self.sindico.verificar_chave(chave):
            messagebox.showerror("Acesso negado", "Chave mestra incorreta.")
            return

        self._abrir_painel_sindico()

    def _abrir_painel_sindico(self):

        janela = tk.Toplevel(self)
        janela.title(f"Administração — {self.sindico.get_nome()}")
        janela.geometry("300x230")
        janela.resizable(False, False)
        janela.configure(bg="#2c3e50")

        tk.Label(
            janela,
            text="ADMINISTRAÇÃO\nDO SÍNDICO",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=15
        ).pack()

        botoes = [
            ("Ver Lockers Cadastrados",     self._listar_lockers),
            ("Remover Morador",             self._sindico_remover_morador),
            ("Abrir Locker (Chave Mestra)", self._sindico_abrir_locker),
        ]

        for texto, comando in botoes:
            tk.Button(
                janela,
                text=texto,
                command=comando,
                bg="#3498db",
                fg="white",
                font=("Arial", 10),
                relief="flat",
                padx=10,
                pady=8,
                width=24,
                cursor="hand2"
            ).pack(pady=4)

    def _sindico_remover_morador(self):

        if not self.sistema.moradores:
            messagebox.showinfo("Remover Morador", "Nenhum morador cadastrado.")
            return

        apartamento = self._pedir_numero("Remover Morador", "Apartamento do morador a remover:")
        if apartamento is None:
            return

        morador = self.sistema._buscar_morador_por_apartamento(apartamento)
        if morador is None:
            messagebox.showerror("Não encontrado", f"Nenhum morador no apartamento {apartamento}.")
            return

        from sistema import persistencia

        nome = morador.get_nome()
        lockers_pendentes = [
            l for l in self.sistema.lockers
            if l.esta_ocupado()
            and l.get_entrega().get_morador().get_apartamento() == apartamento
        ]

        self.sistema.moradores.remove(morador)
        self.sistema._salvar()
        persistencia.salvar_registro("MORADOR REMOVIDO", "-", nome, f"Apto {apartamento}")

        self._escrever(f"[SÍNDICO] Morador '{nome}' removido do apartamento {apartamento}.\n")

        if lockers_pendentes:
            numeros = ", ".join(str(l.get_numero()) for l in lockers_pendentes)
            aviso = f"Há pacote(s) pendente(s) no(s) locker(s) {numeros}. Use a chave mestra para retirar."
            self._escrever(f"[SÍNDICO] Atenção: {aviso}\n")
            messagebox.showwarning("Pacote pendente", aviso)
        else:
            messagebox.showinfo("Sucesso", f"Morador '{nome}' removido.")

    def _sindico_abrir_locker(self):

        numero = self._pedir_numero("Abrir Locker", "Número do locker para abrir:")
        if numero is None:
            return

        from sistema import persistencia

        for locker in self.sistema.lockers:
            if locker.get_numero() == numero:

                morador_antes = None
                if locker.esta_ocupado():
                    morador_antes = locker.get_entrega().get_morador().get_nome()

                sucesso = locker.abrir_com_chave_mestra()

                if sucesso:
                    self.sistema._salvar()
                    persistencia.salvar_registro("ABERTURA CHAVE MESTRA", numero, morador_antes or "-", "")
                    self._escrever(f"[SÍNDICO] Locker {numero} aberto com chave mestra.\n")
                    messagebox.showinfo("Sucesso", "Locker aberto pelo síndico.")
                else:
                    messagebox.showerror("Erro", "Locker já está vazio.")
                return

        messagebox.showerror("Erro", "Locker não encontrado.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
