# Redes Quânticas Sob Ataque: Black Hole Repeaters

## Resumo do Artigo

Esse repositório está vinculado ao artigo "Redes Quânticas Sob Ataque: Black Hole Repeaters" e tem como objetivo estudar o comportamento de Black Holes Attacks em redes quânticas. Ele comporta experimentos de diferentes métricas e topologias a fim de encontrar suas características em cenários distintos com uma modelagem de possíveis ataques _Black Holes_.

Os experimentos são uma forma de simular possíveis implementações de redes quânticas na vida real utilizando diferentes topologias de criação. Por meio dessa modelagem é possível avaliar meios de ataque e possíveis formas de identificação dos mesmos.

Além disso, esse artigo visa entender melhor como redes distintas lidam com esse tipo de atque que apresenta um comportamento discreto e com uma alta dificuldade no seu reconhecimento. Essa falta de conhecimento pode ocasionar em um aumento dos gastos de recursos em redes quânticas de entanglement swapping e, em casos mais severos, pode exaurir os caros recursos quânticos, inviabilizando todos os serviços da rede.

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

## Organização de Dependências

Essas são as principais dependências do projeto, utilizando o gerenciador de pacotes pip torna-se o suficiente para baixar todas. 

### Recomendações

Recomenda-se utilizar alguma interface python de ambiente virtualizado, exemplos são: venv, virtualenv, conda e etc...

Caso opte por não utilizar um ambiente virtual de python, substitua o comando **pip** por **pip3** ou como está definido no _PATH_ do seu sistema.

### Exemplo utilizando venv

O próprio python ao ser instalado traz consigo a capacidade de criar _virtual envarioments_ (ambientes virtuais python), por isso, utilizarei **venv** como exemplo.

Utilize o instalador de pacotes da sua distribuição linux, no caso, utlizarei a distribuição Ubuntu como exemplo e baixarei a versão 3.12 do python.

```
sudo apt-get update && sudo apt-get install python3.12-venv
```

Agora utilzamos o python para criar a venv (virtual envarioment)

Utilize o **python** e o **pip** com o nome que está definido no _PATH_ do seu sistema, em geral, ele tende a ter o nome de **python3** e **pip3** em distribuições linux.

```
python3 -m venv .venv
```

Esse comando criará um diretório chamado de ".venv", o qual está a versão do python definida anteriormente

Por fim, é necessário ativar a venv com o comando `source`.

```
source .venv/bin/activate
```
 
 Com esses passos será possível utilizar o python e o pip da venv.

### Dependências

As dependências do repositório são:

```
python >= 3.12
matplotlib==3.9.2  
networkx==3.4.2  
pandas==2.2.3  
ipykernel==6.29.5
```

Utilize o comando `pip install -r requirements.txt` o qual irá baixar as dependências descritas no _requirements.txt_ do repositório.

Em caso de preferência, rode o comando abaixo para baixar todos os pacotes manualmente.

```
pip install matplotlib==3.9.2 networkx==3.4.2 pandas==2.2.3 ipykernel==6.29.5
```

## Execução das simulações

As simulações ficam dentro do repositório `Simulations/` e nelas será possível acessar os notebooks necessários para a utilização dos códigos.

### Como utilizar o notebook

Para a utilização do código, é necessário a execução das células na ordem em que elas aparecem e com isso será possível analisar os resultados dos experimentos.

É importante lembrar que algumas simulações podem demorar mais de 3 horas em caso de computadores mais fracos. Caso conheça mais do seu sistema, é possível mudar o parâmetro **CORES** dentro do notebook para utilizar mais processos em paralelo. Porém, evite utilizar 100% das Threads do seu sistema, recomenda-se utilizar no máximo o _total de Threads do sistema - 2_, para evitar que o sistema operacional dê alguma falha.

![CORES3](https://github.com/user-attachments/assets/9870fcdf-da8a-4a3b-86fd-bbbc72b59bef)



