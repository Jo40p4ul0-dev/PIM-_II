# ===== menus.py =====
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
# Importação de módulos
import autenticacao
# Importação de módulos
import modulos_academicos



# Função: menu_coordenador
def menu_coordenador(usuario_logado):
    while True:
        utils.limpar_tela()
        utils.console.print(Panel(f"Bem-vindo(a), Coordenador(a) {usuario_logado['nome']}!", title="[bold]Menu do Coordenador[/bold]", border_style="yellow"))
        
        escolha = inquirer.select(
            message="Selecione uma opção:",
            choices=["1. Cadastrar Professor", "2. Listar Usuários", "3. Sair (Logout)"],
            default=None
        ).execute()

        if not escolha: break
        elif escolha.startswith("1."): autenticacao.cadastrar_usuario("Professor")
        elif escolha.startswith("2."): listar_usuarios()
        elif escolha.startswith("3."): break


# Função: menu_professor
def menu_professor(usuario_logado):
    while True:
        utils.limpar_tela()
        utils.console.print(Panel(f"Bem-vindo(a), Professor(a) {usuario_logado['nome']}!", title="[bold]Menu do Professor[/bold]", border_style="blue"))
        
        escolha = inquirer.select(
            message="Selecione uma opção:",
            choices=[
                "1. Cadastrar Aluno", 
                "2. Listar Alunos", 
                "3. Gerenciar Material Didático",
                "4. Gerenciar Turmas",
                "5. Sair (Logout)"
            ],
            default=None
        ).execute()
        
        if not escolha: 
            break
        elif escolha.startswith("1."): 
            autenticacao.cadastrar_usuario("Aluno")
        elif escolha.startswith("2."): 
            listar_usuarios(perfil_filtro="Aluno")
        elif escolha.startswith("3."): 
            modulos_academicos.gerenciar_materiais()
        elif escolha.startswith("4."): 
# Importação de módulos
            import modulo_turmas
            modulo_turmas.gerenciar_turmas(usuario_logado)
        elif escolha.startswith("5."): 
            break




# Função: menu_aluno
def menu_aluno(usuario_logado):
    while True:
        utils.limpar_tela()
        utils.console.print(Panel(f"Bem-vindo(a), Aluno(a) {usuario_logado['nome']}!", title="[bold]Portal do Aluno[/bold]", border_style="green"))
        
        escolha = inquirer.select(
            message="Selecione uma opção:",
            choices=["1. Acessar Material Didático", "2. Falar com o Assistente", "3. Sair (Logout)"],
            default=None
        ).execute()

        if not escolha: break
        elif escolha.startswith("1."): modulos_academicos.acessar_materiais()
        elif escolha.startswith("2."): modulos_academicos.iniciar_chat_ia()
        elif escolha.startswith("3."): break


# Função: listar_usuarios
def listar_usuarios(perfil_filtro=None):
    usuarios = utils.carregar_dados_json(utils.ARQUIVO_USUARIOS)
    utils.limpar_tela()
    
    titulo = "Lista de Todos os Usuários"
    usuarios_a_mostrar = usuarios
    if perfil_filtro:
        titulo = f"Lista de {perfil_filtro}s"
        usuarios_a_mostrar = [u for u in usuarios if u.get('perfil') == perfil_filtro]

    utils.console.print(Panel(titulo, border_style="cyan"))
    
    if not usuarios_a_mostrar:
        utils.console.print("\nNenhum usuário encontrado.")
    else:
        tabela = Table(show_header=True, header_style="bold magenta")
        tabela.add_column("Nome Completo", width=30)
        tabela.add_column("Perfil")

        for u in usuarios_a_mostrar:
            tabela.add_row(u.get('nome', ''), u.get('perfil', ''))
        
        utils.console.print(tabela)

    utils.pausar_tela()

