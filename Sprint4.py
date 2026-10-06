import funcoesCalculos as fc
import funcoesPosto as fp
import funcoesIA as fia

# MENU - ESCOLHER A OPCAO QUE DESEJA
def menu():
    while True:
        print("\n===== GERENCIAMENTO ======")
        print("1 - Conectar veículo")
        print("2 - Potencia ")
        print("3 - Registros")
        print("4 - Remover veículo")
        print("5 - Faturamento")
        # Aconselhável usar a opção 6 ao final do dia
        print("6 - IA (Relatorio + Conselhos)")
        print("7 - Sair")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("\nOpção inválida. Digite um número.\n")
            continue

        if opcao == 1:
            fp.conectar_veiculo()
        elif opcao == 2:
            fp.potencia_posto()
        elif opcao == 3:
            fp.dados()
        elif opcao == 4:
            fp.remover_veiculo()
        elif opcao == 5:
            fc.faturamento_total()
        elif opcao == 6:
            fia.inteligencia_artificial()
        elif opcao == 7:
            print("Saindo do sistema...")
            break
        else:
            print("\nOpção inválida. Digite entre 1 a 7.\n")

if __name__ == "__main__":
    menu()