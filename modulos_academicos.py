# ===== modulos_academicos.py =====
# Versão comentada (modo resumido)
# Cada parte contém breves explicações sobre sua função.

# Importação de módulos
from InquirerPy import inquirer
# Importação de módulos
from rich.panel import Panel
# Importação de módulos
from rich.text import Text
# Importação de módulos
from rich.live import Live
# Importação de módulos
from rich.spinner import Spinner
# Importação de módulos
import requests
# Importação de módulos
import config 
# Importação de módulos
import utils 



# Função: acessar_materiais
def acessar_materiais():   
    materiais = utils.carregar_dados_json(utils.ARQUIVO_MATERIAIS)
    
    if not materiais:
        utils.limpar_tela()
        utils.console.print("Nenhum material disponível no momento.")
        utils.pausar_tela()
        return

    opcoes_menu = [m['disciplina'] for m in materiais] + ["Voltar"]
    
    while True:
        utils.limpar_tela()
        utils.console.print(Panel("Material Didático", border_style="green"))
        disciplina_escolhida = inquirer.select(
            message="Selecione a disciplina:",
            choices=opcoes_menu
        ).execute()

        if disciplina_escolhida == "Voltar":
            break

        for material in materiais:
            if material['disciplina'] == disciplina_escolhida:
                utils.limpar_tela()
                utils.console.print(Panel(
                    Text(material['conteudo'], justify="left"),
                    title=f"[bold cyan]{disciplina_escolhida}[/bold cyan]"
                ))
                utils.pausar_tela()
                break


# Função: iniciar_chat_ia
def iniciar_chat_ia():
    utils.limpar_tela()
    utils.console.print(Panel("Assistente Acadêmico (IA Google Gemini)", border_style="magenta"))
    utils.console.print("[cyan]Conectado![/cyan] Você pode começar a conversar. Digite 'sair' ou 'fim' para encerrar.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={config.GEMINI_API_KEY}"
    
    historico_conversa = []

    while True:
        pergunta = inquirer.text(message="Você:").execute()
        if not pergunta: continue

        if any(p in pergunta.lower() for p in ["sair", "tchau", "fim"]):
            utils.console.print("[magenta]Assistente:[/magenta] Até mais! Se precisar, é só chamar.")
            utils.time.sleep(2)
            break

        historico_conversa.append({"role": "user", "parts": [{"text": pergunta}]})
        
        payload = {"contents": historico_conversa}

        spinner = Spinner("dots", text=" Assistente está digitando...")
        with Live(spinner, refresh_per_second=10, transient=True):
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                
                resultado = response.json()
                
                resposta_ia = resultado['candidates'][0]['content']['parts'][0]['text']

            except requests.exceptions.RequestException as e:
                resposta_ia = f"Erro de conexão com a API. Verifique sua internet."
            except (KeyError, IndexError):
                resposta_ia = "Ocorreu um erro ao processar a resposta da IA. Verifique se sua chave de API no arquivo 'config.py' está correta e válida."

        utils.console.print(f"[magenta]Assistente:[/magenta] {resposta_ia}")
        
        historico_conversa.append({"role": "model", "parts": [{"text": resposta_ia}]})



# Função: adicionar_material
def adicionar_material():
    utils.limpar_tela()
    utils.console.print(Panel("Gerenciador de Material Didático", border_style="blue"))

    disciplina = inquirer.text(message="Qual o nome da disciplina?").execute()
    conteudo = inquirer.text(
        message="Digite o conteúdo da aula:",
        multiline=True,
        instruction="(Pressione Esc e depois Enter para confirmar)"
    ).execute()

    if not disciplina or not conteudo:
        utils.console.print("\n[red]Operação cancelada. Disciplina e conteúdo não podem ser vazios.[/red]")
        utils.pausar_tela()
        return

    materiais = utils.carregar_dados_json(utils.ARQUIVO_MATERIAIS)
    
    novo_material = {
        "disciplina": disciplina,
        "conteudo": conteudo
    }

    materiais.append(novo_material)
    utils.salvar_dados_json(utils.ARQUIVO_MATERIAIS, materiais)

    utils.console.print(f"\n[green]Material para '{disciplina}' adicionado com sucesso![/green]")
    utils.pausar_tela()


# Função: remover_material
def remover_material():
    utils.limpar_tela()
    utils.console.print(Panel("Remover Material Didático", border_style="red"))

    materiais = utils.carregar_dados_json(utils.ARQUIVO_MATERIAIS)

    if not materiais:
        utils.console.print("\n[yellow]Nenhum material cadastrado para remover.[/yellow]")
        utils.pausar_tela()
        return

    opcoes_disciplinas = [m['disciplina'] for m in materiais] + ["Cancelar"]

    disciplina_a_remover = inquirer.select(
        message="Qual material você deseja remover?",
        choices=opcoes_disciplinas
    ).execute()

    if disciplina_a_remover == "Cancelar":
        return

    confirmado = inquirer.confirm(
        message=f"Tem certeza que deseja remover o material de '{disciplina_a_remover}'?",
        default=False
    ).execute()

    if confirmado:
        novos_materiais = [m for m in materiais if m['disciplina'] != disciplina_a_remover]

        utils.salvar_dados_json(utils.ARQUIVO_MATERIAIS, novos_materiais)

        utils.console.print(f"\n[green]Material de '{disciplina_a_remover}' removido com sucesso![/green]")
    else:
        utils.console.print("\n[yellow]Operação cancelada.[/yellow]")

    utils.pausar_tela()





# Função: gerenciar_materiais
def gerenciar_materiais():
    while True:
        utils.limpar_tela()
        utils.console.print(Panel("Gerenciador de Material Didático", border_style="blue"))

        escolha = inquirer.select(
            message="O que você deseja fazer?",
            choices=[
                "1. Adicionar novo material",
                "2. Remover material existente",
                "3. Voltar ao menu anterior"
            ],
            default=None
        ).execute()

        if not escolha or escolha.startswith("3."):
            break
        elif escolha.startswith("1."):
            adicionar_material()
        elif escolha.startswith("2."):
            remover_material()
