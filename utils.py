# ===== utils.py =====
# Versão comentada (modo resumido)
# Cada parte contém breves explicações sobre sua função.

# Importação de módulos
import json 
# Importação de módulos
import os
# Importação de módulos
import time
# Importação de módulos
from rich.console import Console
# Importação de módulos
from rich.panel import Panel   
# Importação de módulos
import bcrypt

console = Console()
DIRETORIO_DADOS = "dados" 
ARQUIVO_USUARIOS = os.path.join(DIRETORIO_DADOS, "usuarios.json")
ARQUIVO_MATERIAIS = os.path.join(DIRETORIO_DADOS, "materiais_didaticos.json")



# Função: limpar_tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Função: pausar_tela
def pausar_tela(mensagem="\nPressione Enter para continuar..."):
    input(mensagem)


# Função: carregar_dados_json
def carregar_dados_json(caminho_do_arquivo):
    if not os.path.exists(caminho_do_arquivo):
        return []
    try:
        with open(caminho_do_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


# Função: salvar_dados_json
def salvar_dados_json(caminho_do_arquivo, dados):
    with open(caminho_do_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


# Função: gerar_hash_senha
def gerar_hash_senha(senha):
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")




# Função: inicializar_sistema
def inicializar_sistema():
    if os.path.exists(os.path.join(DIRETORIO_DADOS, ".inicializado")):
        return

    limpar_tela()
    console.print("[yellow]Executando a configuração inicial do sistema...[/yellow]")
    
    if not os.path.exists(DIRETORIO_DADOS):
        os.makedirs(DIRETORIO_DADOS) 
        console.print(f"Diretório '[cyan]{DIRETORIO_DADOS}[/cyan]' criado.")

    if not os.path.exists(ARQUIVO_USUARIOS): 
        coordenador_padrao = {
            "nome": "Coordenador Padrão",
            "usuario": "coord",
            "senha": gerar_hash_senha("admin123"),
            "perfil": "Coordenador"
        }
        salvar_dados_json(ARQUIVO_USUARIOS, [coordenador_padrao]) 
        
        console.print(Panel(
            "[bold green]Arquivo de usuários não encontrado.[/bold green]\n"
            "Um usuário [bold]Coordenador[/bold] padrão foi criado:\n\n"
            "Login: [cyan]coord[/cyan]\n"
            "Senha: [cyan]admin123[/cyan]\n\n"
            "Use estas credenciais para o primeiro acesso.",
            title="[bold yellow]Aviso de Configuração Inicial[/bold yellow]",
            border_style="yellow"
        ))
        pausar_tela() 

    if not os.path.exists(ARQUIVO_MATERIAIS):
        materiais_iniciais = [
            {
                "disciplina": "Algoritmos em Python", 
                "conteudo": (
                    "**Aula 1: Listas e Dicionários em Python**\n\n"
                    "**Listas** são coleções ordenadas e mutáveis de itens. Pense nelas como um armário com prateleiras numeradas.\n"
                    "- Criação: `minha_lista = [1, 'Python', 3.14]`\n"
                    "- Adicionar item no final: `minha_lista.append('novo')`\n"
                    "- Acessar item pelo índice: `print(minha_lista[0])` (acessa o primeiro item)\n\n"
                    "**Dicionários** são coleções de pares 'chave: valor'. São como uma agenda, onde você busca por um nome (chave) para encontrar uma informação (valor).\n"
                    "- Criação: `meu_dicionario = {'nome': 'Júlio', 'curso': 'ADS'}`\n"
                    "- Acessar valor pela chave: `print(meu_dicionario['nome'])`\n"
                    "- Adicionar/Modificar par: `meu_dicionario['idade'] = 34`\n\n"
                    "Use listas para sequências de itens e dicionários para associar informações."
                )
            },
            {
                "disciplina": "Engenharia de Software", 
                "conteudo": (
                    "**Aula 1: Metodologias Ágeis (Scrum)**\n\n"
                    "**Scrum** é um framework para gerenciar projetos complexos, baseado em ciclos curtos de trabalho chamados **Sprints** (geralmente de 2 a 4 semanas).\n\n"
                    "**Pilares do Scrum:**\n"
                    "1. **Transparência:** Todos têm visibilidade do progresso.\n"
                    "2. **Inspeção:** O trabalho é verificado frequentemente.\n"
                    "3. **Adaptação:** O plano é ajustado conforme necessário.\n\n"
                    "**Papéis Principais:**\n"
                    "- **Product Owner (PO):** Define o que será construído.\n"
                    "- **Scrum Master:** Garante que o time siga o processo e remove impedimentos.\n"
                    "- **Time de Desenvolvimento:** Constrói o produto.\n\n"
                    "O objetivo é entregar valor de forma rápida e contínua."
                )
            }
        ]
        salvar_dados_json(ARQUIVO_MATERIAIS, materiais_iniciais)

    with open(os.path.join(DIRETORIO_DADOS, ".inicializado"), "w") as f:
        f.write("ok")
    
    console.print("[green]Configuração inicial concluída![/green]\n")
    time.sleep(2)
