# ===== modulo_turmas.py =====
# Versão comentada (modo resumido)
# Cada parte contém breves explicações sobre sua função.

# Importação de módulos
from InquirerPy import inquirer
# Importação de módulos
from rich.panel import Panel
# Importação de módulos
from rich.table import Table
# Importação de módulos
import utils

ARQUIVO_TURMAS = "dados/turmas.json"


# Função: carregar_turmas
def carregar_turmas():
    return utils.carregar_dados_json(ARQUIVO_TURMAS)


# Função: salvar_turmas
def salvar_turmas(turmas):
    utils.salvar_dados_json(ARQUIVO_TURMAS, turmas)


# Função: gerenciar_turmas
def gerenciar_turmas(professor_logado):
    while True:
        utils.limpar_tela()
        utils.console.print(Panel(f"Gerenciamento de Turmas - Professor {professor_logado['nome']}", border_style="blue"))

        escolha = inquirer.select(
            message="Selecione uma opção:",
            choices=[
                "1. Criar nova turma",
                "2. Adicionar aluno à turma",
                "3. Remover aluno da turma",
                "4. Listar minhas turmas",
                "5. Voltar"
            ]
        ).execute()

        if escolha.startswith("1."): criar_turma(professor_logado)
        elif escolha.startswith("2."): adicionar_aluno_turma(professor_logado)
        elif escolha.startswith("3."): remover_aluno_turma(professor_logado)
        elif escolha.startswith("4."): listar_turmas(professor_logado)
        else: break



# Função: criar_turma
def criar_turma(professor_logado):
    utils.limpar_tela()
    nome_turma = inquirer.text(message="Nome da nova turma:").execute()
    if not nome_turma:
        utils.console.print("[red]Nome da turma não pode ser vazio.[/red]")
        utils.pausar_tela()
        return

    turmas = carregar_turmas()
    nova_turma = {"nome": nome_turma, "professor": professor_logado["usuario"], "alunos": []}
    turmas.append(nova_turma)
    salvar_turmas(turmas)

    utils.console.print(f"[green]Turma '{nome_turma}' criada com sucesso![/green]")
    utils.pausar_tela()




# Função: adicionar_aluno_turma
def adicionar_aluno_turma(professor_logado):
    
    # Carrega TODAS as turmas para verificar a duplicidade global
    todas_as_turmas = carregar_turmas() 
    
    # Filtra as turmas do professor logado (apenas para escolha no menu)
    turmas_professor = [t for t in todas_as_turmas if t["professor"] == professor_logado["usuario"]]
    
    if not turmas_professor:
        utils.console.print("[yellow]Você ainda não possui turmas cadastradas.[/yellow]")
        utils.pausar_tela()
        return

    turma_nome = inquirer.select(
        message="Selecione a turma:", 
        choices=[t["nome"] for t in turmas_professor]
    ).execute()

    usuarios = utils.carregar_dados_json(utils.ARQUIVO_USUARIOS)
    alunos = [u for u in usuarios if u["perfil"] == "Aluno"]
    aluno_login_escolhido = inquirer.select(
        message="Selecione o aluno para adicionar:", 
        choices=[a["usuario"] for a in alunos]
    ).execute()
    
    # --- NOVO TRECHO DE VERIFICAÇÃO DE DUPLICIDADE GLOBAL ---
    
    # Verifica se o aluno já está em QUALQUER turma
    for turma_existente in todas_as_turmas:
        if aluno_login_escolhido in turma_existente["alunos"]:
            utils.console.print(f"[bold red]Erro:[/bold red] O aluno '{aluno_login_escolhido}' já está na turma '{turma_existente['nome']}'.")
            utils.pausar_tela()
            return
    
    # --- FIM DO NOVO TRECHO ---

    # Encontra a turma selecionada (dentro da lista geral de turmas para salvar)
    for turma in todas_as_turmas:
        # Nota: Você precisa de uma forma única de identificar a turma. 
        # Assumindo que o par (nome_da_turma, professor) é único:
        if turma["nome"] == turma_nome and turma["professor"] == professor_logado["usuario"]:
            
            # A verificação interna para duplicidade na mesma turma já existe aqui
            if aluno_login_escolhido not in turma["alunos"]:
                turma["alunos"].append(aluno_login_escolhido)
                utils.console.print(f"[green]Aluno '{aluno_login_escolhido}' adicionado à turma '{turma_nome}'.[/green]")
            else:
                # Este trecho só será alcançado se você usar um filtro diferente acima, 
                # mas é bom manter a consistência com o original.
                utils.console.print(f"[yellow]Aluno '{aluno_login_escolhido}' já está nessa turma.[/yellow]")
            break
            
    # Salva TODAS as turmas atualizadas
    salvar_turmas(todas_as_turmas)
    utils.pausar_tela()


# Função: remover_aluno_turma
def remover_aluno_turma(professor_logado):
    turmas = carregar_turmas()
    # filtra só as turmas do professor logado
    turmas_professor = [t for t in turmas if t["professor"] == professor_logado["usuario"]]

    if not turmas_professor:
        utils.console.print("[yellow]Você ainda não possui turmas cadastradas.[/yellow]")
        utils.pausar_tela()
        return

    turma_nome = inquirer.select(
        message="Selecione a turma:",
        choices=[t["nome"] for t in turmas_professor]
    ).execute()

    turma = next((t for t in turmas_professor if t["nome"] == turma_nome), None)
    if not turma or not turma["alunos"]:
        utils.console.print("[yellow]Nenhum aluno nessa turma para remover.[/yellow]")
        utils.pausar_tela()
        return

    aluno_remover = inquirer.select(
        message="Selecione o aluno para remover:",
        choices=turma["alunos"]
    ).execute()

    confirmado = inquirer.confirm(
        message=f"Tem certeza que deseja remover '{aluno_remover}' da turma '{turma_nome}'?",
        default=False
    ).execute()

    if not confirmado:
        utils.console.print("[cyan]Operação cancelada.[/cyan]")
        utils.pausar_tela()
        return

    turma["alunos"].remove(aluno_remover)

    # Atualiza a lista geral de turmas
    for t in turmas:
        if t["nome"] == turma_nome and t["professor"] == professor_logado["usuario"]:
            t["alunos"] = turma["alunos"]

    salvar_turmas(turmas)

    utils.console.print(f"[red]Aluno '{aluno_remover}' removido da turma '{turma_nome}'.[/red]")
    utils.pausar_tela()




# Função: listar_turmas
def listar_turmas(professor_logado):
    turmas = [t for t in carregar_turmas() if t["professor"] == professor_logado["usuario"]]
    utils.limpar_tela()
    utils.console.print(Panel("Suas Turmas", border_style="cyan"))

    if not turmas:
        utils.console.print("Você ainda não criou nenhuma turma.")
    else:
        # Tabela com as melhorias visuais e show_lines=True
        tabela = Table(
            title="Turmas e Alunos", 
            show_header=True, 
            header_style="bold magenta", 
            show_lines=True  # Adiciona linha de separação
        )
        
        # Ajusta as colunas para melhor visualização
        tabela.add_column("Turma", width=15, justify="center")
        tabela.add_column("Alunos", width=50, justify="left") 

        for turma in turmas:
            # Garante que a lista de alunos seja uma string
            alunos = ", ".join(turma["alunos"]) if turma["alunos"] else "Nenhum aluno"
            
            # Adiciona a linha, garantindo que os argumentos são strings
            tabela.add_row(turma["nome"], alunos) # <--- ESSA LINHA DEVE ESTAR CORRETA

        utils.console.print(tabela)
    utils.pausar_tela()
    
