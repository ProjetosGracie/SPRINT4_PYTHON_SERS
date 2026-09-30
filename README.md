# ⚡ ChargeGrid Intelligence

### Sistema inteligente de gerenciamento de estações de carregamento para veículos elétricos

> Projeto acadêmico desenvolvido em **Python**, com foco em gerenciamento de veículos elétricos, distribuição de potência, cálculo de carregamento, faturamento e geração de relatórios.

---

## 📌 Sobre o projeto

O **ChargeGrid Intelligence** é uma aplicação desenvolvida para simular o gerenciamento de uma estação de carregamento de veículos elétricos.

O sistema permite controlar os veículos conectados, distribuir a potência disponível da estação, estimar o tempo necessário para o carregamento, calcular o valor da recarga e acompanhar o faturamento.

Como diferencial, o projeto possui um módulo denominado **Inteligência Artificial**, que reúne funcionalidades de sugestão de horários econômicos, auditoria da distribuição de potência, análise dos veículos conectados e geração de relatórios.

---

## 🎯 Objetivo

Desenvolver uma solução capaz de auxiliar no gerenciamento de uma estação de carregamento de veículos elétricos, considerando:

* ⚡ Limitação da potência disponível;
* 🚗 Quantidade de veículos conectados;
* 🔋 Estado de carga das baterias;
* ⏱️ Estimativa do tempo de carregamento;
* 💰 Tarifação por faixa horária;
* 📊 Controle de faturamento;
* 🤖 Análise e recomendações.

A estação possui uma potência padrão de **44 kW**, limite total de **150 kW** e capacidade para até **5 veículos conectados simultaneamente**.

---

## 🚀 Funcionalidades

### 🚗 Gerenciamento de veículos

O sistema permite:

* Conectar veículos;
* Validar placa;
* Informar capacidade da bateria;
* Informar porcentagem atual da bateria;
* Registrar horário de conexão;
* Consultar veículos conectados;
* Consultar veículos cadastrados;
* Remover veículos após o carregamento.

O sistema também impede a conexão de um veículo quando a estação já atingiu sua capacidade máxima.

---

### ⚡ Gerenciamento de potência

A potência disponível é redistribuída automaticamente entre os veículos conectados.

O cálculo considera a potência padrão e o limite máximo da estação:

```text
Potência por veículo =
min(potência padrão, limite do posto / veículos conectados)
```

Dessa forma, quando um novo veículo entra ou outro é removido, a distribuição é recalculada.

---

### ⏱️ Estimativa de carregamento

Para cada veículo, o sistema calcula:

* Energia necessária para completar a bateria;
* Tempo estimado de carregamento;
* Horário previsto para conclusão.

O cálculo considera a capacidade da bateria, porcentagem atual de carga e potência disponibilizada.

---

### 💰 Sistema de tarifação

O valor da recarga é calculado utilizando:

```text
Valor = Energia consumida × Tarifa
```

A tarifa varia de acordo com o horário em que o veículo é conectado.

| Faixa de horário |      Tarifa |
| ---------------- | ----------: |
| 00h – 06h        | R$ 0,70/kWh |
| 06h – 12h        | R$ 1,20/kWh |
| 12h – 14h        | R$ 1,80/kWh |
| 14h – 18h        | R$ 1,30/kWh |
| 18h – 21h        | R$ 1,80/kWh |
| 21h – 24h        | R$ 1,30/kWh |

---

### 📊 Faturamento

Cada carregamento possui seu valor registrado, permitindo calcular o faturamento acumulado da estação.

O sistema também apresenta individualmente o valor de cada carregamento realizado.

---

## 🤖 Módulo de Inteligência Artificial

O sistema possui um módulo de análise identificado no programa como **IA**.

Ele reúne cinco funcionalidades principais:

```text
┌─────────────────────────────────────┐
│       INTELIGÊNCIA ARTIFICIAL       │
├─────────────────────────────────────┤
│ • Sugestão de horário econômico     │
│ • Auditoria da distribuição         │
│ • Veículos conectados               │
│ • Veículos cadastrados               │
│ • Conselhos de gerenciamento        │
│ • Geração de relatório              │
└─────────────────────────────────────┘
```

A sugestão de horário compara as tarifas cadastradas e identifica a faixa com menor valor.

> **Observação:** no código atual, o módulo é denominado “Inteligência Artificial”, mas suas funcionalidades são implementadas por regras e cálculos determinísticos em Python.

---

## 🔎 Auditoria da distribuição

O sistema possui uma rotina de auditoria que compara os veículos conectados.

Ela verifica diferenças entre:

* Porcentagem de bateria;
* Potência recebida.

Quando dois veículos possuem níveis de bateria próximos, mas recebem uma diferença significativa de potência, o sistema gera um alerta.

---

## 📄 Geração de relatórios

O projeto também permite gerar um arquivo:

```text
registro.txt
```

O relatório registra:

* Data;
* Quantidade de veículos cadastrados;
* Faturamento total.

O usuário pode optar por visualizar os registros diretamente pelo terminal.

---

## 🧩 Arquitetura do sistema

O projeto foi estruturado utilizando funções específicas para cada responsabilidade:

```text
                    ┌──────────────┐
                    │     MENU     │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   🚗 Veículos        ⚡ Potência        💰 Faturamento
        │                  │                  │
        ▼                  ▼                  ▼
  Cadastro/remoção   Redistribuição      Tarifação
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                    🤖 Módulo de IA
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Sugestão      Auditoria    Relatórios
```

---

## 🗂️ Estrutura de dados

Os veículos são representados utilizando **dicionários Python**, contendo informações como:

```python
{
    "placa": "...",
    "potencia (kW)": 44.0,
    "Potencia da bateria (kWh)": 60.0,
    "Porcentagem": 30.0,
    "horario inicio": "10:30"
}
```

Esses registros são armazenados em listas responsáveis por manter os veículos cadastrados e os veículos atualmente conectados.

---

## 🛠️ Tecnologias

| Tecnologia                 | Utilização                      |
| -------------------------- | ------------------------------- |
| 🐍 Python                  | Desenvolvimento da aplicação    |
| 📦 Listas                  | Armazenamento dos registros     |
| 🗃️ Dicionários            | Representação dos veículos      |
| 🔧 Funções                 | Organização das funcionalidades |
| 📄 TXT                     | Armazenamento dos relatórios    |
| ➗ Operações matemáticas    | Potência, tempo e faturamento   |
| 🔀 Estruturas condicionais | Regras de negócio               |
| 🔄 Laços de repetição      | Processamento dos registros     |

---

## 📈 Regras principais do sistema

| Regra                         |       Valor |
| ----------------------------- | ----------: |
| Potência padrão               |       44 kW |
| Limite do posto               |      150 kW |
| Máximo de veículos conectados |           5 |
| Menor tarifa cadastrada       | R$ 0,70/kWh |
| Maior tarifa cadastrada       | R$ 1,80/kWh |

---

## 💡 Principais conceitos aplicados

O desenvolvimento do projeto permitiu aplicar conceitos fundamentais de programação:

* Variáveis e estruturas de dados;
* Listas e dicionários;
* Funções;
* Modularização;
* Estruturas condicionais;
* Laços de repetição;
* Tratamento de exceções;
* Validação de dados;
* Manipulação de arquivos;
* Operações matemáticas;
* Regras de negócio.

---

## 🔮 Possíveis evoluções

O projeto pode futuramente evoluir para uma solução mais completa através de:

* Banco de dados;
* Interface gráfica;
* Dashboard;
* API;
* Sistema de autenticação;
* Histórico de carregamentos;
* Integração com estações reais;
* Monitoramento em tempo real;
* Algoritmos de otimização de potência;
* Modelos de IA baseados em dados históricos.

---

## 🎓 Contexto acadêmico

Projeto desenvolvido como atividade acadêmica com foco na aplicação prática de **Python, estruturas de dados, lógica de programação e desenvolvimento de uma solução para o gerenciamento de veículos elétricos**.

---

## 📌 Status

🟢 **Em desenvolvimento**

O projeto possui uma implementação funcional em Python e pode receber novas funcionalidades e melhorias de arquitetura ao longo do desenvolvimento.

---

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e educacionais.
