# =============================================================
# NEOWORK LIGHT - Sistema Simplificado de Conexão Profissional
# Tema: O Futuro do Trabalho – Conectando pessoas e empresas
# =============================================================

import sys

# -------------------------------------------------------------
# Banco de dados em memória
# -------------------------------------------------------------
usuarios = {}
empresas = {}
vagas = {}
proximo_id_empresa = 1
proximo_id_vaga = 1

# -------------------------------------------------------------
# Funções utilitárias
# -------------------------------------------------------------
def titulo(txt):
    print("\n" + "=" * 65)
    print(f"  {txt}")
    print("=" * 65)

def entrada(texto):
    valor = input(texto).strip()
    while not valor:
        print("⚠️  Este campo não pode ficar vazio.")
        valor = input(texto).strip()
    return valor

def limpar_lista(texto):
    return [t.strip().lower() for t in texto.split(",") if t.strip()]

def match_score(vaga_skills, user_skills):
    """Calcula compatibilidade (0–100%)"""
    if not vaga_skills or not user_skills:
        return 0
    v = set(vaga_skills)
    u = set(user_skills)
    inter = len(v & u)
    total = len(v | u)
    return round((inter / total) * 100, 1)

# -------------------------------------------------------------
# Cadastro de usuários e empresas
# -------------------------------------------------------------
def cadastrar_usuario():
    titulo("Cadastro de Usuário")
    try:
        username = entrada("Nome de usuário (único): ").lower()
        if username in usuarios:
            print("❌ Já existe um usuário com esse nome.")
            return
        nome = entrada("Nome completo: ")
        idade = entrada("Idade: ")
        area = entrada("Área de atuação: ")
        competencias = limpar_lista(entrada("Competências (separe por vírgula): "))
        proposito = entrada("Propósito profissional: ")

        usuarios[username] = {
            "nome": nome,
            "idade": idade,
            "area": area,
            "competencias": competencias,
            "proposito": proposito,
        }
        print(f"\n✅ Usuário '{nome}' cadastrado com sucesso!")
    except Exception as e:
        print(f"❌ Erro no cadastro: {e}")

def cadastrar_empresa():
    global proximo_id_empresa
    titulo("Cadastro de Empresa")
    try:
        nome = entrada("Nome da empresa: ")
        setor = entrada("Setor de atuação: ")
        descricao = entrada("Descrição breve: ")
        empresa_id = f"E{proximo_id_empresa:03d}"
        empresas[empresa_id] = {
            "nome": nome,
            "setor": setor,
            "descricao": descricao,
        }
        proximo_id_empresa += 1
        print(f"\n✅ Empresa '{nome}' cadastrada com sucesso! (ID: {empresa_id})")
    except Exception as e:
        print(f"❌ Erro no cadastro: {e}")

# -------------------------------------------------------------
# Criação de vagas e visualização de candidatos
# -------------------------------------------------------------
def criar_vaga():
    global proximo_id_vaga
    titulo("Criar Nova Vaga")
    if not empresas:
        print("⚠️ Nenhuma empresa cadastrada. Cadastre uma antes.")
        return
    for id_emp, emp in empresas.items():
        print(f"{id_emp} - {emp['nome']} ({emp['setor']})")
    emp_id = entrada("Digite o ID da empresa: ").upper()
    if emp_id not in empresas:
        print("❌ Empresa não encontrada.")
        return

    titulo_vaga = entrada("Título da vaga: ")
    descricao = entrada("Descrição da vaga: ")
    competencias = limpar_lista(entrada("Competências desejadas (separe por vírgula): "))

    vaga_id = f"V{proximo_id_vaga:03d}"
    vagas[vaga_id] = {
        "empresa_id": emp_id,
        "titulo": titulo_vaga,
        "descricao": descricao,
        "competencias": competencias,
    }
    proximo_id_vaga += 1
    print(f"\n✅ Vaga '{titulo_vaga}' criada com sucesso! (ID: {vaga_id})")

def ver_candidatos():
    titulo("Visualizar Candidatos (com compatibilidade automática)")
    if not usuarios:
        print("⚠️ Nenhum usuário cadastrado.")
        return
    if not vagas:
        print("⚠️ Nenhuma vaga criada.")
        return

    # Mostra as vagas existentes
    for v_id, v in vagas.items():
        emp = empresas[v["empresa_id"]]["nome"]
        print(f"{v_id} - {v['titulo']} ({emp})")

    vaga_id = entrada("Digite o ID da vaga para ver candidatos: ").upper()
    vaga = vagas.get(vaga_id)
    if not vaga:
        print("❌ Vaga não encontrada.")
        return

    print(f"\n🏢 Empresa: {empresas[vaga['empresa_id']]['nome']}")
    print(f"📋 Vaga: {vaga['titulo']}")
    print(f"🎯 Competências desejadas: {', '.join(vaga['competencias'])}")
    print("-" * 65)

    candidatos = []
    for username, user in usuarios.items():
        score = match_score(vaga["competencias"], user["competencias"])
        if score > 0:
            candidatos.append((score, username, user))

    if not candidatos:
        print("Nenhum candidato com competências compatíveis.")
        return

    candidatos.sort(reverse=True, key=lambda x: x[0])

    for score, uname, user in candidatos:
        print(f"{user['nome']} ({user['area']}) — Compatibilidade: {score}%")
        print(f"   Competências: {', '.join(user['competencias'])}")
        print(f"   Propósito: {user['proposito']}")
        print("-" * 65)

# -------------------------------------------------------------
# Contato empresa → candidato
# -------------------------------------------------------------
def contatar_candidato():
    titulo("Contatar Candidato (Simulação)")
    if not empresas:
        print("⚠️ Nenhuma empresa cadastrada.")
        return
    if not usuarios:
        print("⚠️ Nenhum usuário cadastrado.")
        return

    # Mostrar empresas
    for id_emp, emp in empresas.items():
        print(f"{id_emp} - {emp['nome']} ({emp['setor']})")
    emp_id = entrada("Digite o ID da empresa: ").upper()
    if emp_id not in empresas:
        print("❌ Empresa não encontrada.")
        return

    # Mostrar candidatos
    for uname, u in usuarios.items():
        print(f"- {uname} : {u['nome']} ({u['area']})")
    uname = entrada("Digite o nome de usuário do candidato: ").lower()
    if uname not in usuarios:
        print("❌ Candidato não encontrado.")
        return

    mensagem = entrada("Mensagem para o candidato: ")
    print(f"\n✅ Mensagem enviada de '{empresas[emp_id]['nome']}' para '{usuarios[uname]['nome']}'.")
    print(f"🗨️  Conteúdo: {mensagem}")

# -------------------------------------------------------------
# Listagens gerais
# -------------------------------------------------------------
def listar_empresas_e_vagas():
    titulo("Empresas e Vagas")
    if not empresas:
        print("⚠️ Nenhuma empresa cadastrada.")
        return
    for eid, e in empresas.items():
        print(f"\n🏢 {e['nome']} ({e['setor']}) — {e['descricao']}")
        vagas_emp = [v for v in vagas.values() if v["empresa_id"] == eid]
        if not vagas_emp:
            print("   Nenhuma vaga cadastrada.")
        else:
            for v in vagas_emp:
                print(f"   💼 {v['titulo']} — {', '.join(v['competencias'])}")

def listar_usuarios():
    titulo("Usuários Cadastrados")
    if not usuarios:
        print("⚠️ Nenhum usuário cadastrado.")
        return
    for u in usuarios.values():
        print(f"👤 {u['nome']} ({u['area']})")
        print(f"   Competências: {', '.join(u['competencias'])}")
        print(f"   Propósito: {u['proposito']}")
        print("-" * 60)

# -------------------------------------------------------------
# Menu principal
# -------------------------------------------------------------
def menu_principal():
    while True:
        titulo("NEOWORK LIGHT - Conectando Pessoas e Empresas")
        print("1. Cadastrar Usuário")
        print("2. Cadastrar Empresa")
        print("3. Criar Vaga")
        print("4. Ver Candidatos (com match automático)")
        print("5. Contatar Candidato")
        print("6. Listar Empresas e Vagas")
        print("7. Listar Usuários")
        print("8. Sair")

        op = input("Escolha uma opção: ").strip()
        if op == "1": cadastrar_usuario()
        elif op == "2": cadastrar_empresa()
        elif op == "3": criar_vaga()
        elif op == "4": ver_candidatos()
        elif op == "5": contatar_candidato()
        elif op == "6": listar_empresas_e_vagas()
        elif op == "7": listar_usuarios()
        elif op == "8":
            print("\n👋 Encerrando o sistema. Até logo!")
            break
        else:
            print("❌ Opção inválida, tente novamente.")

# -------------------------------------------------------------
# Execução principal
# -------------------------------------------------------------
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário. Encerrando...")
        sys.exit(0)
