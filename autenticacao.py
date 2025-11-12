# ===== autenticacao.py =====
# Versão comentada (modo resumido)
# Cada parte contém breves explicações sobre sua função.


# Importação de módulos
import bcrypt
# Importação de módulos
from InquirerPy import inquirer##biblioteca de seta
# Importação de módulos
from InquirerPy.validator import EmptyInputValidator##biblioteca de validaçao "vazio"
# Importação de módulos
from rich.panel import Panel##cores

# Importação de módulos
import utils



# Função: checar_senha
def checar_senha(senha_digitada, senha_hasheada):
    return bcrypt.checkpw(senha_digitada.encode("utf-8"), senha_hasheada.encode("utf-8"))


# Função: login
def login():
    usuarios = utils.carregar_dados_json(utils.ARQUIVO_USUARIOS)
    utils.limpar_tela()
    utils.console.print(Panel("[bold cyan]Login no Sistema Acadêmico[/bold cyan]", border_style="cyan"))
    
    nome_usuario_digitado = inquirer.text(
        message="Digite seu nome de usuário:",
        validate=EmptyInputValidator("O nome de usuário não pode ser vazio.")
    ).execute()
    
    senha_digitada = inquirer.secret(
        message="Digite sua senha:",
        validate=EmptyInputValidator("A senha não pode ser vazia.")
    ).execute()

    for usuario in usuarios:
        if usuario["usuario"] == nome_usuario_digitado and checar_senha(senha_digitada, usuario["senha"]):
            utils.console.print(f"\n[bold green]Login bem-sucedido! Bem-vindo(a), {usuario['nome']}![/bold green]")
            utils.time.sleep(2) 
            return usuario 

    utils.console.print("\n[bold red]Erro: Usuário ou senha inválidos.[/bold red]")
    utils.pausar_tela()
    return None 


# Função: cadastrar_usuario
def cadastrar_usuario(perfil_a_cadastrar):
    usuarios = utils.carregar_dados_json(utils.ARQUIVO_USUARIOS) 
    utils.limpar_tela()
    utils.console.print(Panel(f"[bold]Cadastro de Novo {perfil_a_cadastrar}[/bold]", border_style="magenta"))

    nome = inquirer.text(message="Nome completo:", validate=EmptyInputValidator()).execute()
    usuario_login = inquirer.text(message="Nome de usuário (para login):", validate=EmptyInputValidator()).execute()
    
    if any(u['usuario'] == usuario_login for u in usuarios):
        utils.console.print("\n[bold red]Erro: Nome de usuário já existe! Tente outro.[/bold red]")
        utils.pausar_tela()
        return 

    senha = inquirer.secret(message="Senha:", validate=EmptyInputValidator()).execute()
    confirmar_senha = inquirer.secret(message="Confirme a senha:", validate=EmptyInputValidator()).execute()

    if senha != confirmar_senha:
        utils.console.print("\n[bold red]Erro: As senhas não coincidem![/bold red]")
        utils.pausar_tela()
        return 

    novo_usuario = {
        "nome": nome,
        "usuario": usuario_login ,
        "senha": utils.gerar_hash_senha(senha),
        "perfil": perfil_a_cadastrar
    }
    
    usuarios.append(novo_usuario) 
    utils.salvar_dados_json(utils.ARQUIVO_USUARIOS, usuarios)
    
    utils.console.print(f"\n[bold green]{perfil_a_cadastrar} '{nome}' cadastrado com sucesso![/bold green]")
    utils.pausar_tela()
