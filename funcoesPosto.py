import estado as s4 
from funcoesCalculos import calcular_tempo, pagamento


# REDISTRIBUIR_POTENCIA - DIVIDE A POTENCIA DO POSTO ENTRE OS CARROS CONECTADOS
def redistribuir_potencia():
    if not s4.sessao:
        return

    potencia_calculada = min(s4.potencia_padrao, s4.limite_posto / len(s4.sessao))
    for veiculo in s4.sessao:
        veiculo["potencia (kW)"] = potencia_calculada
        calcular_tempo(veiculo)


def conectar_veiculo():

    # Bloqueia antes de pedir qualquer dado se o posto já está cheio
    if len(s4.sessao) >= s4.max_veiculos:
        print(f"Posto lotado ({s4.max_veiculos} veículos). Aguarde um veículo sair para conectar outro.\n")
        return

    placa = input("Informe a placa do veículo: ").strip().upper()

    if not placa:
        print("A placa não pode ficar vazia.")
        return

    if placa in [v["placa"] for v in s4.sessao]:
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

    # padroniza o horário. Se digitou "9:5", passa a ser "09:05".
    horario_inicial = f"{horas:02d}:{minutos:02d}"

    veiculo_conectado = {
        "placa": placa,
        "potencia (kW)": s4.potencia_padrao,
        "Potencia da bateria (kWh)": bateria_potencia,
        "Porcentagem": bateria_porcentagem,
        "horario inicio": horario_inicial,
    }
    s4.sessao.append(veiculo_conectado)
    s4.veiculos_cadastrados.append(veiculo_conectado)
    print(f" ===== VEICULO {placa} CONECTADO =====\n")

    if len(s4.sessao) >= s4.max_veiculos:
        print(f"ALERTA: {len(s4.sessao)} VEICULOS JA CONECTADOS (limite do posto)")

    # Redistribui a potência entre todos (isso também calcula o tempo do novo carro)
    redistribuir_potencia()
    pagamento(veiculo_conectado)


# POTENCIA_POSTO - INFORMA A POTENCIA QUE OS CARROS ESTAO UTILIZANDO E INFORMA QUANTOS CARROS ESTAO CONECTADOS
def potencia_posto():
    if not s4.sessao:
        print("Nenhum veículo conectado.")
        return

    redistribuir_potencia()

    n = 0
    for veiculo in s4.sessao:
        n += 1
        print(f"\n====== Registro {n} ======")
        print(f"Veículo: {veiculo['placa']}\nPotencia: {veiculo['potencia (kW)']:.2f} kW.")
        print("===========================\n")

    print(f"Total de veículo(s) conectado(s): {len(s4.sessao)}\nPotencia que o(s) veiculo(s) recebeu(ao): {s4.sessao[0]['potencia (kW)']:.2f} kW.\n")


# DADOS - DADOS DE CADA CARRO REGISTRADO
def dados():
    if not s4.sessao:
        print("Nenhum veículo conectado.")
        return

    n = 1
    for veiculo in s4.sessao:
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
    if not s4.sessao:
        print("Nenhum veículo conectado.")
        return

    placa_remover = input("Informe a placa do veículo a ser removido: ").strip().upper()
    for veiculo in s4.sessao:
        if veiculo["placa"] == placa_remover:
            s4.sessao.remove(veiculo)
            print(f"Veículo {placa_remover} removido com sucesso.\n")
            # Os carros que ficaram passam a receber mais potência
            redistribuir_potencia()
            return

    print(f"Veículo {placa_remover} não encontrado.\n")