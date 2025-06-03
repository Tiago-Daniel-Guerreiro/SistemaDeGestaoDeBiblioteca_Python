import json
import os
import datetime

Max_Livros = 3
CriarDadosPadraoQuandoNaoExistem = True

class Biblioteca:
    def __init__(self):
        self.Livros = []
        self.Alunos = []

    def cadastrar_livro(self, livro):
        for Livro in self.Livros:
            if str(Livro.codigo) == str(livro.codigo):
                print(f"Já existe um livro com o código {livro.codigo}.")
                return
        self.Livros.append(livro)

    def cadastrar_aluno(self, aluno):
        for Aluno in self.Alunos:
            if aluno.matricula == Aluno.matricula:
                print(f"Já existe um aluno com a matrícula {Aluno.matricula}.")
                return
        self.Alunos.append(aluno)

    def consultar_livros_disponiveis(self):
        Livros_Disponiveis = []
        for livro in self.Livros:
            if livro.disponibilidade:
                Livros_Disponiveis.append(livro)
        return Livros_Disponiveis
    
    def emprestar_livro(self, aluno, livro):
        if aluno in self.Alunos and livro in self.Livros:
            return aluno.pegar_livro(livro)
        else:
            return False

    def ProcurarLivroPeloCodigo(self, codigo):
        for livro in self.Livros:
            if str(livro.codigo) == str(codigo):
                return livro
        return None

    def devolver_livro(self, aluno, livro):
        if aluno in self.Alunos and livro in self.Livros:
            return aluno.devolver_livro(livro)
        else:
            return False

    def listar_Livros(self):
        livros_str = []
        for livro in self.Livros:
            livros_str.append(str(livro))
        return livros_str

    def listar_Alunos(self):
        alunos_str = []
        for aluno in self.Alunos:
            alunos_str.append(str(aluno))
        return alunos_str

    def Procurar_Aluno(self, nome, matricula):
        for aluno in self.Alunos:
            if aluno.nome == nome and aluno.matricula == matricula:
                return aluno
        return None

    def Procurar_Aluno_Pelo_Nome(self, nome):
        AlunosComNomeIgual = []
        for aluno in self.Alunos:
            if aluno.nome == nome:
                AlunosComNomeIgual.append(aluno)

        if len(AlunosComNomeIgual) > 0:
            return AlunosComNomeIgual
        else:
            return None

    def to_dict(self):
        livros_dict = []
        for livro in self.Livros:
            livros_dict.append(livro.to_dict())
        alunos_dict = []
        for aluno in self.Alunos:
            alunos_dict.append(aluno.to_dict())
        return {
            "Livros": livros_dict,
            "Alunos": alunos_dict
        }

    def from_dict(self, data):
        livros = []
        for livro_data in data["Livros"]:
            livros.append(Livro("", "", 0).from_dict(livro_data))
        self.Livros = livros

        alunos = []
        for aluno_data in data["Alunos"]:
            alunos.append(Aluno("", 0).from_dict(aluno_data))
        self.Alunos = alunos

class Livro:
    def __init__(self, titulo, autor, codigo):
        self.titulo = titulo
        self.autor = autor
        self.codigo = str(codigo)
        self.disponibilidade = True

    def emprestar(self):
        if self.disponibilidade:
            self.disponibilidade = False
            return True
        return False

    def devolver(self):
        if(self.disponibilidade):
            return False
        else:
            self.disponibilidade = True
            return True
  
    def __str__(self):
        return (
            f"\tTitulo: {self.titulo}\n"
            f"\tAutor: {self.autor}\n"
            f"\tCodigo: {self.codigo}\n"
            f"\tDisponibilidade: {'Disponivel' if self.disponibilidade else 'Não Disponivel'}"
        )

    def to_dict(self):
        return {
            "Titulo": self.titulo,
            "Autor": self.autor,
            "Codigo": self.codigo,
            "Disponibilidade": self.disponibilidade
        }

    def from_dict(self, data):
        self.titulo = data["Titulo"]
        self.autor = data["Autor"]
        self.codigo = data["Codigo"]
        self.disponibilidade = data["Disponibilidade"]
        return self
                            
class Aluno:
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = str(matricula)
        self.livros_emprestados_Cod = []

    def listar_livros_emprestados(self):
        global biblioteca
        TitulosDeLivrosEmprestados = []
        for CodLivro in self.livros_emprestados_Cod:
            TitulosDeLivrosEmprestados.append(biblioteca.ProcurarLivroPeloCodigo(CodLivro).titulo + " - " + str(CodLivro))
        return "\n\t\t".join(TitulosDeLivrosEmprestados)

    def pegar_livro(self, livro):
        if len(self.livros_emprestados_Cod) < Max_Livros and livro.emprestar():
            self.livros_emprestados_Cod.append(livro.codigo)
            return True
        else:
            return False
   
    def devolver_livro(self, livro):
        if livro.codigo in self.livros_emprestados_Cod:
            livro.devolver()
            self.livros_emprestados_Cod.remove(livro.codigo)
            return True
        else:
            return False

    def __str__(self):
        global biblioteca
        LivrosEmprestados = []
        for CodLivro in self.livros_emprestados_Cod:
            LivrosEmprestados.append(biblioteca.ProcurarLivroPeloCodigo(CodLivro).titulo) #
        if(len(LivrosEmprestados) == 0):
            LivrosEmprestados.append("Nenhum")
        livros_str = '\n\t\t'.join(LivrosEmprestados)
        return (
            f"\tNome: {self.nome}\n"
            f"\tMatricula: {self.matricula}\n"
            f"\tLivros Emprestados:\n\t\t{livros_str}"
        )

    def to_dict(self):
        return {
            "Nome": self.nome,
            "Matricula": self.matricula,
            "Cod_Livros": self.livros_emprestados_Cod
        }

    def from_dict(self, data):
        self.nome = data["Nome"]
        self.matricula = data["Matricula"]
        self.livros_emprestados_Cod = data["Cod_Livros"]
        return self

class Relatorio:

    def ObterInformacoes(self, InformacoesLivrosEmprestados=False, InformacoesAluno=False, InformacoesLivro=False):
        global biblioteca
        Texto = []
        if InformacoesLivrosEmprestados:
            Texto.append(self.ObterLivrosEmprestados())
        if InformacoesLivro:
            Texto.append("\n".join(self.ObterInformacoesLivros()))
        if InformacoesAluno:
            Texto.append("\n".join(self.ObterInformacoesAlunos()))
        return "\n\n".join(Texto)

    def ObterLivrosEmprestados(self):
        global biblioteca
        total_livros_emprestados = 0   
        for livro in biblioteca.Livros:
            if not livro.disponibilidade:
                total_livros_emprestados += 1
        return f'Total de livros emprestados: {total_livros_emprestados} / {len(biblioteca.Livros)}'

    def ObterInformacoesAlunos(self):
        global biblioteca
        lista_info_alunos = [f'Total de alunos cadastrados: {len(biblioteca.Alunos)}']
        for aluno in biblioteca.Alunos:
            lista_info_alunos.append(str(aluno) + "\n")
        return lista_info_alunos

    def ObterInformacoesLivros(self):
        global biblioteca
        lista_info_livros = [f'Total de livros cadastrados: {len(biblioteca.Livros)}']
        for livro in biblioteca.Livros:
            lista_info_livros.append(str(livro) + "\n")
        return lista_info_livros

    def Gerar_ficheiro_relatorio(self,InformacoesLivrosEmprestados=False, InformacoesAluno=False, InformacoesLivro=False, nome_arquivo="Relatorio"):
        global biblioteca
        texto = self.ObterInformacoes(
            InformacoesLivrosEmprestados,
            InformacoesAluno,
            InformacoesLivro
        )
        if not os.path.exists("Relatorios"):
            os.mkdir("Relatorios") 
        nome_arquivo = "Relatorios/" + nome_arquivo + " - "+ datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(texto)
        local_Ficheiro = "Relatorios/"+nome_arquivo;
        return f"Relatório gerado em {local_Ficheiro}"

class Biblioteca_JSON:
    def GuardarDados(self):
        global biblioteca
        dados = biblioteca.to_dict()
        with open("DadosBiblioteca.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def CarregarDados(self):
        global biblioteca
        try:
            with open("DadosBiblioteca.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                biblioteca.from_dict(dados)
        except FileNotFoundError:
            biblioteca = Biblioteca()

    def Verificar_Se_Dados_Existem(self):
        global biblioteca
        try:
            with open("DadosBiblioteca.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                return bool(dados.get("Livros")) or bool(dados.get("Alunos"))
        except FileNotFoundError:
            return False

class GestorDeDadosBiblioteca:
    def __init__(self):
        self.Gestor_JSON = Biblioteca_JSON()
        self.Gestor_Relatorio = Relatorio()

    def CarregarDadosPadrão(self):
        global biblioteca
        biblioteca = Biblioteca()
        biblioteca.cadastrar_livro(Livro("Python para Iniciantes", "Autor A", 1))
        biblioteca.cadastrar_livro(Livro("Aprendendo Java", "Autor B", 2))
        biblioteca.cadastrar_livro(Livro("Estruturas de Dados", "Autor C", 3))
        biblioteca.cadastrar_aluno(Aluno("João", "123"))
        biblioteca.cadastrar_aluno(Aluno("Maria", "456"))
        aluno1 = biblioteca.Alunos[0]
        aluno2 = biblioteca.Alunos[1]
        livro1 = biblioteca.Livros[0]
        livro2 = biblioteca.Livros[1]
        biblioteca.emprestar_livro(aluno1, livro1)
        biblioteca.emprestar_livro(aluno2, livro2)
        biblioteca.devolver_livro(aluno1, livro1)

    def GuardarDados(self):
        self.Gestor_JSON.GuardarDados()

    def CarregarDados(self):
        self.Gestor_JSON.CarregarDados()

    def Criar_Relatorio(self, nome_arquivo="Relatorio.txt"):
         self.Gestor_Relatorio.Gerar_ficheiro_relatorio(True,True,True,nome_arquivo)

    def VerificarFicheiroJSON_ContemDados_E_CarregarOuCriar(self):
        global biblioteca
        if self.Gestor_JSON.Verificar_Se_Dados_Existem():
            self.Gestor_JSON.CarregarDados()
            print("Dados carregados do ficheiro JSON.")
        else:
            if(CriarDadosPadraoQuandoNaoExistem):
                self.CarregarDadosPadrão()
                self.Gestor_JSON.GuardarDados()
                print("Ficheiro não existia ou estava vazio. Dados padrão carregados e guardados.")

class Console_Biblioteca:

    def menu():
        while True:
            print("\nSistema de Gestão de Biblioteca")
            print("1. Cadastrar Livro")
            print("2. Cadastrar Aluno")
            print("3. Consultar Livros Disponíveis")
            print("4. Emprestar Livro")
            print("5. Devolver Livro")
            print("6. Criar Relatório")
            print("7. Abrir Relatório")
            print("8. Listar Relatórios")
            print("9. Listar Livros")
            print("10. Listar Alunos")
            print("0. Sair")

            try:
                opcao = input("Escolha uma opção: ")
            except EOFError:
                print("\nEntrada não disponível. Encerrando o sistema.")
                break

            if (opcao == "1"):
                Console_Biblioteca.__cadastrar_livro()
            elif (opcao == "2"):
                Console_Biblioteca.__cadastrar_aluno()
            elif (opcao == "3"):
                Console_Biblioteca.__consultar_livros_disponiveis()
            elif (opcao == "4"):
                Console_Biblioteca.__emprestar_livro()
            elif (opcao == "5"):
                Console_Biblioteca.__devolver_livro()
            elif (opcao == "6"):
                Console_Biblioteca.__CriarRelatorio()            
            elif (opcao == "7"):
                Console_Biblioteca.__AbrirRelatorio()            
            elif (opcao == "8"):
                Console_Biblioteca.__ListarRelatorios()
            elif (opcao == "9"):
                Console_Biblioteca.__ListarLivros()            
            elif (opcao == "10"):
                Console_Biblioteca.__ListarAlunos()
            elif (opcao == "0"):
                Gestor_Biblioteca.GuardarDados()
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def __cadastrar_livro():
        global biblioteca
        titulo = input(f"Digite o título do novo livro: ")
        autor = input(f"Digite o autor do livro {titulo}: ")
        codigo = input(f"Digite o código do livro {titulo}: ")

        if biblioteca.ProcurarLivroPeloCodigo(codigo):
            print("Já existe um livro com esse código.")
            return

        livro = Livro(titulo, autor, codigo)
        biblioteca.cadastrar_livro(livro)
        print("Livro cadastrado com sucesso!")
    
    def __cadastrar_aluno():
        global biblioteca
        nome = input("Introduza o nome do novo aluno(a): ")
        matricula = input(f"Introduza a matrícula do aluno(a) {nome}: ")
        aluno = Aluno(nome, matricula)
        biblioteca.cadastrar_aluno(aluno)
        print("Aluno(a) cadastrado com sucesso!")
    
    def __consultar_livros_disponiveis():
        global biblioteca
        livros_disponiveis = biblioteca.consultar_livros_disponiveis()
        if livros_disponiveis:
            print("Livros disponíveis:")
            for livro in livros_disponiveis:
                print(f"{livro}\n")
        else:
            print("Nenhum livro disponível no momento.")

    def __emprestar_livro():
        global biblioteca
        aluno = Console_Biblioteca.__ObterAlunoDeLista()
        if aluno == None:
            print("Aluno(a) não encontrado.")
            return

        livro = Console_Biblioteca.__ObterLivroDeLista()
        if livro == None:
            print("Livro não encontrado.")
            return

        if biblioteca.emprestar_livro(aluno, livro):
            print(f"Livro '{livro.titulo}' emprestado com sucesso para {aluno.nome}.")
        else:
            print(f"Não foi possível emprestar o livro '{livro.titulo}' para {aluno.nome}.")

    def __devolver_livro():
        global biblioteca
        aluno = Console_Biblioteca.__ObterAlunoDeLista()

        if aluno == None:
            print("Aluno(a) não encontrado.")
            return
        livro = Console_Biblioteca.__ObterLivro_Emprestado_De_Lista(aluno)

        if livro == None:
            print("Livro não encontrado.")
            return

        if biblioteca.devolver_livro(aluno, livro):
            print(f"Livro '{livro.titulo}' devolvido com sucesso por {aluno.nome}.")
        else:
            print(f"Não foi possível devolver o livro '{livro.titulo}' do aluno {aluno.nome}.")

    def __ListarLivros():
        global biblioteca
        livros = biblioteca.listar_Livros()
        if len(livros) > 0:
            print("Livros cadastrados:")
            for livro in livros:
                print(f"{livro}\n")
        else:
            print("Nenhum livro cadastrado.")

    def __ObterLivroDeLista():
        global biblioteca
        Console_Biblioteca.__ListarLivros()

        codigo = input("Digite o código do livro: ")

        livro = biblioteca.ProcurarLivroPeloCodigo(codigo)
        if livro == None:
            print("Livro não encontrado.")
            return None
        return livro

    def __ObterLivro_Emprestado_De_Lista(aluno):
        print(aluno.listar_livros_emprestados())
        codigo = None
        while codigo is None:
            try:
                codigo = int(input("Digite o código do livro emprestado: "))
            except ValueError:
                print("Código inválido. Por favor, digite um número inteiro.")
                codigo = None

        livro = biblioteca.ProcurarLivroPeloCodigo(codigo)
        if livro == None:
            print("Livro não encontrado.")
            return None
        return livro
    
    def __ListarAlunos():
        global biblioteca
        alunos = biblioteca.listar_Alunos()
        if len(alunos) > 0:
            print("Alunos(as) cadastrados:")
            for aluno in alunos:
                print(f"{aluno}\n")
        else:
            print("Nenhum aluno(a) cadastrado.")

    def __ObterAlunoDeLista():
        global biblioteca
        Console_Biblioteca.__ListarAlunos()

        nome = input("Digite o nome do aluno(a): ")
        aluno = biblioteca.Procurar_Aluno_Pelo_Nome(nome)

        if(aluno != None and len(aluno) > 1):
            matricula = input("Digite a matricula do aluno(a): ")
            aluno = biblioteca.Procurar_Aluno(nome, matricula)

        if aluno == None:
            print("Aluno(a) não encontrado.")
            return None

        if type(aluno) is list:
            return aluno[0]
        
        return aluno

    def __ListarRelatorios():
        diretorio = "Relatorios"
        if not os.path.exists(diretorio):
            print("Nenhum relatório encontrado.")
            return
        arquivos = [f for f in os.listdir(diretorio)]
        if not arquivos:
            print("Nenhum relatório encontrado.")
            return
        print("Relatórios disponíveis:")
        for i, nome in enumerate(arquivos, 1):
            print(f"{i}. {nome}")

    def __CriarRelatorio():
        global Gestor_Biblioteca
        print("\nConfiguração do Relatório:")

        # [Informações Alunos, Informações Livros Emprestados, Informações Detalhadas]
        opcoes = [False, False, False]

        while True:
            print("\nSelecione as opções:")
            print(f"1. Informações Alunos: {'Sim' if opcoes[0] else 'Não'}")
            print(f"2. Informações Livros Emprestados: {'Sim' if opcoes[1] else 'Não'}")
            print(f"3. Informações Detalhadas: {'Sim' if opcoes[2] else 'Não'}")
            print("4. Criar Relatório")
            print("5. Cancelar")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                opcoes[0] = not opcoes[0]
            elif escolha == "2":
                opcoes[1] = not opcoes[1]
            elif escolha == "3":
                opcoes[2] = not opcoes[2]
            elif escolha == "4":
                nome_arquivo = input("Digite o nome do relatório (sem extensão): ")
                resultado = Gestor_Biblioteca.Gestor_Relatorio.Gerar_ficheiro_relatorio(
                    InformacoesLivrosEmprestados=opcoes[1],
                    InformacoesAluno=opcoes[0],
                    InformacoesLivro=opcoes[2],
                    nome_arquivo=nome_arquivo
                )
                print(resultado)
                break
            elif escolha == "5":
                print("Operação cancelada.")
                break
            else:
                print("Opção inválida.")

    def __AbrirRelatorio():
        diretorio = "Relatorios"
        if not os.path.exists(diretorio):
            print("Nenhum relatório encontrado.")
            return
        arquivos = [f for f in os.listdir(diretorio)]
        if not arquivos:
            print("Nenhum relatório encontrado.")
            return
        Console_Biblioteca.__ListarRelatorios()
        try:
            escolha = int(input("Introduza o número do ficheiro para abrir: "))
            if 1 <= escolha <= len(arquivos):
                caminho = os.path.join(diretorio, arquivos[escolha - 1])
                with open(caminho, "r", encoding="utf-8") as f:
                    print(f"\nConteúdo de {arquivos[escolha - 1]}:\n")
                    print(f.read())
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida.")


if __name__ == "__main__":
    global biblioteca
    global Gestor_Biblioteca
    biblioteca = Biblioteca()
    Gestor_Biblioteca = GestorDeDadosBiblioteca()
    Gestor_Biblioteca.VerificarFicheiroJSON_ContemDados_E_CarregarOuCriar()
    Gestor_Biblioteca.Criar_Relatorio()
    Console_Biblioteca.menu()
