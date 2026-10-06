import estado as s4 
from funcoesCalculos import calcular_faturamento


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


# AUDITORIA_DISTRIBUICAO - COMPARA A DISTRIBUICAO DE POTENCIA ENTRE OS VEICULOS
def auditoria_distribuicao():

    print("\n[Auditoria] Verificando distribuição de potência entre veículos...")

    encontrou_alerta = False
    for indice_atual in range(len(s4.sessao)):
        for indice_comparado in range(indice_atual + 1, len(s4.sessao)):
            veiculo_atual = s4.sessao[indice_atual]
            veiculo_comparado = s4.sessao[indice_comparado]

            # abs() troca o "if diferença < 0" manual
            diferenca_bateria = abs(veiculo_atual["Porcentagem"] - veiculo_comparado["Porcentagem"])
            diferenca_potencia = abs(veiculo_atual["potencia (kW)"] - veiculo_comparado["potencia (kW)"])

            print(f" - Comparando {veiculo_atual['placa']} ({veiculo_atual['Porcentagem']}% de bateria) com {veiculo_comparado['placa']} ({veiculo_comparado['Porcentagem']}% de bateria)\nDiferença de bateria: {diferenca_bateria:.1f} pontos\nDiferença de potência: {diferenca_potencia:.2f} kW")

            if diferenca_bateria <= 10 and diferenca_potencia > 5:
                print(f" === ALERTA: bateria parecida, mas potência bem diferente entre {veiculo_atual['placa']} e {veiculo_comparado['placa']} ===")
                encontrou_alerta = True

    if not encontrou_alerta:
        print("Nenhuma inconsistência encontrada na distribuição atual.")


# VEICULOS AINDA CONECTADOS
def veiculos_conectados():
    n = 1
    for veiculo in s4.sessao:
        print(n, " - ", veiculo["placa"])
        n += 1
    print(f"\nTotal de Veiculos conectados: {len(s4.sessao)}")


# VEICULOS CADASTRADOS
def veiculos_registrados():
    n = 1
    for veiculo in s4.veiculos_cadastrados:
        print(n, " - ", veiculo["placa"])
        n += 1
    print(f"\nTotal de Veiculos cadastrados: {len(s4.veiculos_cadastrados)}")


# CONSELHO
def conselho():
    pode = s4.max_veiculos - len(s4.sessao)

    if pode <= 0:
        print("Espere para poder conectar, Porque??\n1 - O tempo de carregamento aumenta\n2 - Os clientes vão ficar nervosos com a demora\n3 - Posto pode superaquecer ")
    else:
        print("Pode conectar mais ", pode, " carros")


# CRIA UM RELATORIO
def criando_arquivo():
    dia = input("Informe a data: ")
    faturamento = calcular_faturamento()

    # encoding evita problema com acentos em alguns sistemas
    with open("registro.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Relatorio: {dia}\n")
        arquivo.write(f"Veiculos Cadastrados: {len(s4.veiculos_cadastrados)}\n")
        arquivo.write(f"Faturamento: R$ {faturamento:.2f}\n\n")

    deseja = input("Deseja ver o relatorio (S/N): ").strip().upper()
    if deseja == "S":
        with open("registro.txt", "r", encoding="utf-8") as arquivo:
            print("\n")
            for linha in arquivo:
                print(linha.strip())
    else:
        print()


# INTELIGENCIA_ARTIFICIAL
def inteligencia_artificial():
    if not s4.sessao and not s4.faturamento_lista:
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