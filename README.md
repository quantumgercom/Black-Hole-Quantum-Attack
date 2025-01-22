# Black Hole Quantum Attack

## Visão Geral
Esse repositório tem como objetivo estudar o comportamento de Black Holes Attacks em redes quânticas. Ele comporta experimentos de diferentes métricas e topologias afim de encontrar suas características em cenários distintos.

## Avisos

- Esse repositório foi criado com o objetivo de rodar as simulações em sistemas linux, logo, sistemas diferentes deste tendem a não funcionar.
- As simulações são feitas para serem rodadas em paralelo o que pode estressar consideravelmente algumas máquinas com menos processamento.
- As simulações demandam muitos cálculos e muitas repetições, por isso elas tendem a demorar um tempo demasiadamente longo.

## Quantumnet

Este projeto simula uma rede quântica para transmissão de informações entre um remetente e um destinatário. A rede é projetada com diferentes topologias, abrangendo todas as camadas necessárias para um funcionamento eficiente. O repositório contém os códigos em Python para execução da simulação.

### Descrição do Simulador

O repositório inclui os componentes essenciais da rede e do host, além dos qubits e pares EPR. Pode haver visualização de três tipos de topologia: anel, linha e grade. O projeto, também, abrange todas as camadas necessárias, desde a física até a aplicação, garantindo o funcionamento completo da rede quântica.

### Diretórios do Simulador
- ``quantumnet``: 
  - ``/components`` : arquivos básicos para o realização das simulações.
  - ``/layers`` : arquivos que contém as camadas para o funciomento básico da rede.
  - ``/objects`` : elementos essenciais para a funcionamento dos componentes.

## Simulações 

### Descrição das Simulações

As simulação são divididas em Default simulations e Topology simulations, cada uma com o propósito diferente.

As Default simulations exploram o comportamento do ataque em redes de grade e estuda prioritariamente as métricas do ataque de acordo com o aumento da intensidade.

As Topology simulations focam em como as redes de diferentes topologias reagem ao ataque conforme aumentamos a quantidade de nós.

### Diretórios das Simulações

O repositório contém os diretórios: BHA_functions, Examples, Graphics, Simulations e Simulations_Data. Sendo cada um deles necessário para uma função específica dentro das simulações.

- ``BHA_functions``: Diretório onde abriga as funções principais das simulações
- ``Examples``: Diretório com exemplos de funcionamento das simulações
- ``Graphics``: Diretório voltado a guardar os gráficos dos experimentos
- ``Simulations``: Diretório encarregado de guardar as simulações
- ``Simulations_Data``: Diretório focado em guardar os dados dos experimentos
