import estado as s4


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
        horario_termino += f" (+{dias_depois} dia(s))"  

    veiculo["horario final previsto"] = horario_termino
    veiculo["tempo de carregamento"] = tempo


# PAGAMENTO - CALCULA O QUANTO A PESSOA TEM QUE PAGAR E FAZ AS REGRAS
def pagamento(veiculo):

    horas= map(int, veiculo["horario inicio"].split(":"))

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
    s4.faturamento_lista.append(veiculo)


# CALCULAR_FATURAMENTO - SÓ SOMA O FATURAMENTO, SEM IMPRIMIR NADA
def calcular_faturamento():
    total = 0
    for veiculo in s4.faturamento_lista:
        total += veiculo["valor a pagar"]
    return total


# FATURAMENTO_TOTAL - MOSTRA NA TELA CADA CARREGAMENTO E O FATURAMENTO TOTAL DO POSTO
def faturamento_total():
    if not s4.faturamento_lista:
        print("Nenhum carregamento registrado ainda.")
        return

    n = 0
    print("\n======= CALCULANDO FATURAMENTO =======")
    for veiculo in s4.faturamento_lista:
        n += 1
        print(f"Faturamento do {n}º carregamento ({veiculo['placa']}): R$ {veiculo['valor a pagar']:.2f} ...")
    print("======================================\n")

    print("====== CALCULO CONCLUIDO ======")
    print(f"Faturamento total: R$ {calcular_faturamento():.2f}\n")