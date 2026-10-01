# VARIAVEIS GLOBAIS
veiculos_cadastrados = []
sessao      = []
faturamento_lista = []
potencia_padrao = 44.0
limite_posto    = 150.0
max_veiculos = 5

# MENU - ESCOLHER A OPCAO QUE DESEJA 
def menu():
    while True:
        print("\n===== GERENCIAMENTO ======")
        print("1 - Conectar veículo")
        print("2 - Potencia ")
        print("3 - Registros")
        print("4 - Remover veículo")
        print("5 - Faturamento")
        # A conselho usar ao final do dia  o numero 6
        print("6 - IA (Relatorio + Conselhos)")  
        print("7 - Sair")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("\nOpção inválida. Digite um número.\n")
            continue

        if opcao == 1:
            conectar_veiculo()
        elif opcao == 2:
            potencia_posto()
        elif opcao == 3:
            dados()
        elif opcao == 4:
            remover_veiculo()
        elif opcao == 5:
            faturamento_total()
        elif opcao == 6:
            inteligencia_artificial()
        elif opcao == 7:
            print("Saindo do sistema...")
            break
        else:
            print("\nOpção inválida. Digite entre 1 a 7.\n")

# REDISTRIBUIR_POTENCIA - DIVIDE A POTENCIA DO POSTO ENTRE OS CARROS CONECTADOS
def redistribuir_potencia():
    if not sessao:
        return

    potencia_calculada = min(potencia_padrao, limite_posto / len(sessao))
    for veiculo in sessao:
        veiculo["potencia (kW)"] = potencia_calculada
        calcular_tempo(veiculo)

# CONECTAR_VEICULO
def conectar_veiculo():

    # Bloqueia antes de pedir qualquer dado se o posto já está cheio
    if len(sessao) >= max_veiculos:
        print(f"Posto lotado ({max_veiculos} veículos). Aguarde um veículo sair para conectar outro.\n")
        return

    placa = input("Informe a placa do veículo: ").strip().upper()

    if not placa:
        print("A placa não pode ficar vazia.")
        return

    if placa in [v["placa"] for v in sessao]:
        print("Veículo já conectado.\n")
        return

    try:
        bateria_potencia = float(input("Informe a capacidade da bateria (kWh): "))
        bateria_porcentagem = float(input("Informe a porcentagem de carga da bateria (0 a 100): "))

        # Transforma a string em números inteiros, para podermos fazer os cálculos
        horario_inicial = input("Informe o horário de conexão (HH:MM): ")
        horas, minutos = map(int, horario_inicial.split(":"))
    except ValueError:
        print("Valor inválido. Por favor, informe um número (horário no formato HH:MM).")
        return

    if bateria_porcentagem < 0 or bateria_porcentagem > 100:
        print("Valor inválido para a porcentagem de carga da bateria (deve estar entre 0 e 100).")
        return

    if bateria_potencia <= 0 or bateria_potencia > 100:
        print("Valor inválido para a capacidade da bateria (deve ser maior que 0 e no máximo 100).")
        return

    if horas < 0 or horas > 23 or minutos < 0 or minutos > 59:
        print("Valor inválido para o horário de conexão.")
        return

    veiculo_conectado = {
        "placa": placa,
        "potencia (kW)": potencia_padrao,
        "Potencia da bateria (kWh)": bateria_potencia,
        "Porcentagem": bateria_porcentagem,
        "horario inicio": horario_inicial,
    }
    sessao.append(veiculo_conectado)
    veiculos_cadastrados.append(veiculo_conectado)
    print(f" ===== VEICULO {placa} CONECTADO =====\n")

    if len(sessao) >= max_veiculos:
        print(f"ALERTA: {len(sessao)} VEICULOS JA CONECTADOS (limite do posto)")

    # Redistribui a potência entre todos (isso também calcula o tempo do novo carro)
    redistribuir_potencia()
    pagamento(veiculo_conectado)

# POTENCIA_POSTO - INFORMA A POTENCIA QUE OS CARROS ESTAO UTILIZANDO E INFORMA QUANTOS CARROS ESTAO CONECTADOS
def potencia_posto():
    if not sessao:
        print("Nenhum veículo conectado.")
        return

    redistribuir_potencia()

    n = 0
    for veiculo in sessao:
        n += 1
        print(f"\n====== Registro {n} ======")
        print(f"Veículo: {veiculo['placa']}\nPotencia: {veiculo['potencia (kW)']:.2f} kW.")
        print("===========================\n")

    print(f"Total de veículo(s) conectado(s): {len(sessao)}\nPotencia que o(s) veiculo(s) recebeu(ao): {sessao[0]['potencia (kW)']:.2f} kW.\n")


# DADOS - DADOS DE CADA CARRO REGISTRADO
def dados():
    if not sessao:
        print("Nenhum veículo conectado.")
        return

    n = 1
    for veiculo in sessao:
        print(f"\n===== DADOS {n} =====")
        n += 1
        for nome, valor in veiculo.items():
            if isinstance(valor, (int, float)):
                print(f"{nome} - {valor:.2f}")
            else:
                print(f"{nome} - {valor}")
        print("=======================\n")

# REMOVER_VEICULO - REMOVER O VEICULO QUE ACABOU DE CARREGAR
def remover_veiculo():
    if not sessao:
        print("Nenhum veículo conectado.")
        return

    placa_remover = input("Informe a placa do veículo a ser removido: ").strip().upper()
    for veiculo in sessao:
        if veiculo["placa"] == placa_remover:
            sessao.remove(veiculo)
            print(f"Veículo {placa_remover} removido com sucesso.\n")
            # Os carros que ficaram passam a receber mais potência
            redistribuir_potencia()
            return

    print(f"Veículo {placa_remover} não encontrado.\n")

# CALCULAR_TEMPO - CALCULA O TEMPO TOTAL DE UM ÚNICO VEÍCULO
def calcular_tempo(veiculo):
    horario_inicial = veiculo["horario inicio"]

    # Só falta carregar a parte que ainda não está na bateria
    energia_faltante = veiculo["Potencia da bateria (kWh)"] * (100 - veiculo["Porcentagem"]) / 100
    tempo = energia_faltante / veiculo["potencia (kW)"]

    horas, minutos = map(int, horario_inicial.split(":"))

    tempo_horas = int(tempo)
    tempo_minutos = int((tempo - tempo_horas) * 60)

    fim_horas = horas + tempo_horas
    fim_minutos = minutos + tempo_minutos

    # Corrige quando os minutos passam de 60
    if fim_minutos >= 60:
        fim_horas += fim_minutos // 60
        fim_minutos = fim_minutos % 60

    # Corrige quando passa de 24 horas, avisando quantos dias depois termina
    dias_depois = fim_horas // 24
    fim_horas = fim_horas % 24

    horario_termino = f"{fim_horas:02d}:{fim_minutos:02d}"
    if dias_depois > 0:
        horario_termino += f" (+{dias_depois} dia)"

    veiculo["horario final previsto"] = horario_termino
    veiculo["tempo de carregamento"] = tempo

# PAGAMENTO - CALCULA O QUANTO A PESSOA TEM QUE PAGAR E FAZ AS REGRAS
def pagamento(veiculo):

    horas, minutos = map(int, veiculo["horario inicio"].split(":"))

    if 0 <= horas < 6:
        tarifa = 0.70
    elif 6 <= horas < 12:
        tarifa = 1.20
    elif 12 <= horas < 14:
        tarifa = 1.80
    elif 14 <= horas < 18:
        tarifa = 1.30
    elif 18 <= horas < 21:
        tarifa = 1.80
    else:
        tarifa = 1.30

    energia_consumida = (veiculo["Potencia da bateria (kWh)"] * (100 - veiculo["Porcentagem"])) / 100

    # Preço = energia (kWh) x tarifa (R$/kWh). O tempo não entra na conta.
    valor_pagar = energia_consumida * tarifa
    veiculo["valor a pagar"] = valor_pagar
    faturamento_lista.append(veiculo)

# CALCULAR_FATURAMENTO - SÓ SOMA O FATURAMENTO, SEM IMPRIMIR NADA
def calcular_faturamento():
    total = 0
    for veiculo in faturamento_lista:
        total += veiculo["valor a pagar"]
    return total
 
# FATURAMENTO_TOTAL - MOSTRA NA TELA CADA CARREGAMENTO E O FATURAMENTO TOTAL DO POSTO
def faturamento_total():
    if not faturamento_lista:
        print("Nenhum carregamento registrado ainda.")
        return
 
    n = 0
    print("\n======= CALCULANDO FATURAMENTO =======")
    for veiculo in faturamento_lista:
        n += 1
        print(f"Faturamento do {n}º carregamento ({veiculo['placa']}): R$ {veiculo['valor a pagar']:.2f} ...")
    print("======================================\n")
 
    print("====== CALCULO CONCLUIDO ======")
    print(f"Faturamento total: R$ {calcular_faturamento():.2f}\n")

# SUGERIR_HORARIO_ECONOMICO
def sugerir_horario_economico():
    tarifas_por_faixa = {
        "Madrugada (00h-06h)": 0.70,
        "Manhã (06h-12h)": 1.20,
        "Pico almoço (12h-14h)": 1.80,
        "Tarde (14h-18h)": 1.30,
        "Pico noite (18h-21h)": 1.80,
        "Noite (21h-24h)": 1.30,
    }
    print("\n[Sugestão de horário] Comparando as tarifas de cada faixa:")

    menor_tarifa = None
    faixa_mais_barata = None
    for faixa, tarifa in tarifas_por_faixa.items():
        print(f" - {faixa}: R$ {tarifa:.2f}/kWh")

        if menor_tarifa is None or tarifa < menor_tarifa:
            menor_tarifa = tarifa
            faixa_mais_barata = faixa

    print(f"Faixa mais econômica: '{faixa_mais_barata}' (R$ {menor_tarifa:.2f}/kWh). Priorize conectar veículos nesse período.")

# # AUDITORIA_DISTRIBUICAO - COMPARA A DISTRIBUICAO DE POTENCIA ENTRE OS VEICULOS
def auditoria_distribuicao():

    print("\n[Auditoria] Verificando distribuição de potência entre veículos...")

    encontrou_alerta = False
    for indice_atual in range(len(sessao)):
        for indice_comparado in range(indice_atual + 1, len(sessao)):
            veiculo_atual = sessao[indice_atual]
            veiculo_comparado = sessao[indice_comparado]
            diferenca_bateria = veiculo_atual["Porcentagem"] - veiculo_comparado["Porcentagem"]

            if diferenca_bateria < 0:
                diferenca_bateria = -diferenca_bateria

            diferenca_potencia = veiculo_atual["potencia (kW)"] - veiculo_comparado["potencia (kW)"]

            if diferenca_potencia < 0:
                diferenca_potencia = -diferenca_potencia

            print(f" - Comparando {veiculo_atual['placa']} ({veiculo_atual['Porcentagem']}% de bateria) com {veiculo_comparado['placa']} ({veiculo_comparado['Porcentagem']}% de bateria)\nDiferença de bateria: {diferenca_bateria:.1f} pontos\nDiferença de potência: {diferenca_potencia:.2f} kW")

            if diferenca_bateria <= 10 and diferenca_potencia > 5:
                print(f" === ALERTA: bateria parecida, mas potência bem diferente entre {veiculo_atual['placa']} e {veiculo_comparado['placa']} ===")
                encontrou_alerta = True

    if not encontrou_alerta:
        print("Nenhuma inconsistência encontrada na distribuição atual.")


# VEICULOS AINDA CONECTADOS
def veiculos_conectados():
 n = 1
 for placa in sessao:
    print(n," - ",placa["placa"])
    n+= 1
 print(f"\nTotal de Veiculos conectados: {len(sessao)}")

# VEICULOS CADASTRADOS
def veiculos_registrados():
 n = 1
 for placa in veiculos_cadastrados:
    print(n," - ",placa["placa"])
    n+=1
 print(f"\nTotal de Veiculos cadastrados: {len(veiculos_cadastrados)}")

# CONSELHO
def conselho():
    pode = 5 - len(sessao)

    if len(sessao) >= 5:
        print("Espere para poder conectar, Porque??\n1 - O tempo de carregamento aumenta\n2 - Os clientes vão ficar nervosos com a demora\n3 - Posto pode superaquecer ")
    else:
        print("Pode conectar mais ",pode," carros")

# CRIA UM RELATORIO
def criando_arquivo():
    dia = input("Informe a data: ")
    faturamento = calcular_faturamento()

    with open("registro.txt", "a") as arquivo:
        
        arquivo.write(f"Relatorio: {dia}\n")
        arquivo.write(f"Veiculos Cadastrados: {str(len(veiculos_cadastrados))}\n")
        arquivo.write(f"Faturamento: R$ {faturamento:.2f}\n\n")

    deseja = input("Deseja ver o relatorio (S/N): ").upper()
    if deseja == "S":
        with open("registro.txt","r") as arquivo:
            print("\n")
            for linha in arquivo:
             print(linha.strip())
    else:
        print()



# INTELIGENCIA_ARTIFICIAL
def inteligencia_artificial():
    if not sessao and not faturamento_lista:
        print("Nenhum dado para gerar relatório.")
        return
    print("======== INTELIGENCIA ARTIFICIAL =========")
    print("\n========== MÓDULO DE IA: SUGESTÃO ==========")
    sugerir_horario_economico()
    print("\n========= MÓDULO DE IA: AUDITORIA =========")
    auditoria_distribuicao()
    print("\n====== MÓDULO DE IA: VEICULOS CONECTADOS  ======")
    veiculos_conectados()
    print("\n====== MÓDULO DE IA: VEICULOS CADASTRADOS  ======")
    veiculos_registrados()
    print("\n========== MÓDULO DE IA: CONSELHOS  ===========")
    conselho()
    print("\n========== CRIANDO RELATORIO ==========")
    criando_arquivo()
    print("\n================================================\n")


menu()