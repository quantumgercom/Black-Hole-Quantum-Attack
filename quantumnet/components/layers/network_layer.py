import networkx as nx
from quantumnet.components import Host
from quantumnet.objects import Logger, Epr
from random import uniform

class NetworkLayer:
    def __init__(self, network, link_layer, physical_layer):
        """
        Inicializa a camada de rede.
        
        args:
            network : Network : Rede.
            link_layer : LinkLayer : Camada de enlace.
            physical_layer : PhysicalLayer : Camada física.
        """
        self._network = network
        self._physical_layer = physical_layer
        self._link_layer = link_layer
        self.logger = Logger.get_instance()
        self.avg_size_routes = 0  # Inicializa o tamanho médio das rotas
        self.used_eprs = 0  # Inicializa o contador de EPRs utilizados
        self.used_qubits = 0  # Inicializa o contador de Qubits utilizados
        self.routes_used = {}  # Inicializa o dicionário de rotas usadas 

    def __str__(self):
        """ Retorna a representação em string da camada de rede. 
        
        returns:
            str : Representação em string da camada de rede."""
        return 'Network Layer'

    def get_used_eprs(self):
        """Retorna a contagem de EPRs utilizados na camada de rede."""
        self.logger.debug(f"Eprs usados na camada {self.__class__.__name__}: {self.used_eprs}")
        return self.used_eprs
    
    def get_used_qubits(self):
        self.logger.debug(f"Qubits usados na camada {self.__class__.__name__}: {self.used_qubits}")
        return self.used_qubits

    def short_route_valid(self, Alice: int, Bob: int, increment_timeslot=True) -> list:
        """
        Escolhe a melhor rota entre dois hosts com critérios adicionais.

        args:
            Alice (int): ID do host de origem.
            Bob (int): ID do host de destino.
            increment_timeslot (bool): Indica se o timeslot deve ser incrementado.
            
        returns:
            list or None: Lista com a melhor rota entre os hosts ou None se não houver rota válida.
        """
        if increment_timeslot:
            self._network.timeslot()  # Incrementa o timeslot sempre que uma rota é verificada
            self.logger.log(f'Timeslot {self._network.get_timeslot()}: Buscando rota válida entre {Alice} e {Bob}.')

        if Alice is None or Bob is None:
            self.logger.log('IDs de hosts inválidos fornecidos.')
            return None

        if not self._network.graph.has_node(Alice) or not self._network.graph.has_node(Bob):
            self.logger.log(f'Um dos nós ({Alice} ou {Bob}) não existe no grafo.')
            return None
        
        
         #TODO: CRIEI UM FILTRO PARA REMOVER AS ARESTAS QUE FORAM SWAPPED
            # Filtrar arestas criadas por entanglement swapping
        filtered_graph = self._network.graph.copy()
        for edge in list(filtered_graph.edges(data=True)):
            if edge[2].get('swapped', False):  # Ignorar arestas marcadas como swapped
                filtered_graph.remove_edge(edge[0], edge[1])

        try:
            shortest_path = list(nx.shortest_path(filtered_graph, Alice, Bob))  # Pegando apenas um melhor caminho
            fidelities = [] 
            for i in range(len(shortest_path) - 1): # Coletando as fidelidades da rota
                epr_pairs = self._network.get_eprs_from_edge(shortest_path[i], shortest_path[i+1])
                fidelities.extend([epr.get_current_fidelity() for epr in epr_pairs])
            if fidelities != []:
                f_route = sum(fidelities) / len(fidelities)
                # print(f"AQUI AS FIDELIDADES: {fidelities}")

                if self._network.avg_fidelity_route == -1.0:
                    self._network.avg_fidelity_route = f_route
                else:
                    self._network.avg_fidelity_route = (f_route + self._network.avg_fidelity_route) / 2

        except nx.NetworkXNoPath:
            self.logger.log(f'Sem rota encontrada entre {Alice} e {Bob}')
            return None

        valid_path = True
        for i in range(len(shortest_path) - 1):
            node = shortest_path[i]
            next_node = shortest_path[i + 1]
            if len(self._network.get_eprs_from_edge(node, next_node)) < 1:
                self.logger.log(f'Sem pares EPRs entre {node} e {next_node} na rota {shortest_path}')
                valid_path = False
                break

            if valid_path:
                self.logger.log(f'Rota válida encontrada: {shortest_path}')

                # Armazena a rota se for a primeira vez que é usada
                if (Alice, Bob) not in self.routes_used:
                    self.routes_used[(Alice, Bob)] = shortest_path.copy()

                return shortest_path

        self.logger.log('Nenhuma rota válida encontrada.')
        return None

    def entanglement_swapping(self, Alice: int = None, Bob: int = None, route: list = None) -> bool:
        """
        Realiza o Entanglement Swapping em toda a rota determinada pelo short_route_valid.
        
        args:
            Alice (int, optional): ID do host de origem. Se não fornecido, usa o primeiro nó da rota válida.
            Bob (int, optional): ID do host de destino. Se não fornecido, usa o último nó da rota válida.
            route (list, required): A rota a qual o host de origem irá se comunicar com o host de destino
                
        returns:
            int: Retorna 1 em caso de sucesso, 0 em caso de falha e -1 em caso de falha por rota inválida/falta de recursos
        """

        # Verifica se uma rota válida foi encontrada e se ela tem pelo menos 2 nós
        if route is None or len(route) < 2:
            self.logger.log('Não foi possível determinar uma rota válida.')
            return -1

        # Define Alice e Bob como o primeiro e o último nó da rota, respectivamente
        Alice = route[0]
        Bob = route[-1]

        # Itera sobre a rota realizando o entanglement swapping para cada segmento da rota
        while len(route) > 1:
            # Incrementa o timeslot antes de cada operação de entanglement swapping
            self._network.timeslot()
            self.logger.log(f'Timeslot {self._network.get_timeslot()}: Realizando Entanglement Swapping.')

            node1 = route[0]    # Primeiro nó na rota
            node2 = route[1]    # Segundo nó na rota
            node3 = route[2] if len(route) > 2 else None  # Terceiro nó na rota (se existir)

            # Verifica se existe um canal entre node1 e node2
            if not self._network.graph.has_edge(node1, node2):
                self.logger.log(f'Canal entre {node1}-{node2} não existe')
                return -1

            try:
                # Obtém o primeiro par EPR entre node1 e node2
                epr1 = self._network.get_eprs_from_edge(node1, node2)[0]
            except IndexError:
                # Se não houver pares EPR suficientes, loga a falha e retorna False
                self.logger.log(f'Não há pares EPRs suficientes entre {node1}-{node2}')
                return -1

            # Se houver um terceiro nó, realiza o swapping entre node1, node2 e node3
            if node3 is not None:
                # Verifica se existe um canal entre node2 e node3
                if not self._network.graph.has_edge(node2, node3):
                    self.logger.log(f'Canal entre {node2}-{node3} não existe')
                    return -1

                try:
                    # Obtém o primeiro par EPR entre node2 e node3
                    epr2 = self._network.get_eprs_from_edge(node2, node3)[0]
                except IndexError:
                    # Se não houver pares EPR suficientes, loga a falha e retorna False
                    self.logger.log(f'Não há pares EPRs suficientes entre {node2}-{node3}')
                    return -1

                # Mede a fidelidade dos pares EPR
                fidelity1 = epr1.get_current_fidelity()
                fidelity2 = epr2.get_current_fidelity()
                
                # Calcula a probabilidade de sucesso do entanglement swapping
                success_prob = fidelity1 * fidelity2 + (1 - fidelity1) * (1 - fidelity2)

                # Lista dos nós da que vão realizar o entanglement
                list_nodes = [self._network.get_host(node1), self._network.get_host(node2), self._network.get_host(node3)]

                # irá adicionar uma taxa definida no nó para caso este apresente uma
                list_prob = []

                # Se for bha e a Alice for o target, então alterar a fidelidade, se não, deixa como está
                for node in list_nodes:
                    node_target = node.black_hole_target
                    if node_target == None:
                        node_target = []
                    if node.black_hole and self._network.get_host(Alice) in node_target:
                        list_prob.append(node.prob_target_entanglement_swapping)
                    else:
                        list_prob.append(node.prob_entanglement_swapping)

                tax = 1
                for temp_tax in list_prob:
                    if temp_tax is not None:
                        tax *= temp_tax
                success_prob *= tax
                
                # Verifica se o swapping foi bem-sucedido com base na probabilidade de sucesso
                if uniform(0, 1) > success_prob:
                    self.logger.log(f'Entanglement Swapping falhou entre {node1}-{node2} e {node2}-{node3}')
                    # Remove os pares Eprs utilizados
                    self._network.physical.remove_epr_from_channel([epr1], (node1, node2))
                    self._network.physical.remove_epr_from_channel([epr2], (node2, node3))
                    # Atualiza o contador de Eprs utilizados
                    self.used_eprs += 2
                    return 0

                # Calcula a nova fidelidade do par EPR virtual
                new_fidelity = (fidelity1 * fidelity2) / ((fidelity1 * fidelity2) + (1 - fidelity1) * (1 - fidelity2))
                epr_virtual = Epr((node1, node3), new_fidelity)

                # Se o canal entre node1 e node3 não existir, adiciona um novo canal
                if not self._network.graph.has_edge(node1, node3):
                    self._network.graph.add_edge(node1, node3, eprs=[], swapped=True)
                else:
                    # Caso já exista a aresta, apenas atualiza o atributo swapped
                    self._network.graph.edges[(node1, node3)]['swapped'] = True   #TODO: ADICIONEI  O SWAPPED AQUI

                # Adiciona o par EPR virtual ao canal entre node1 e node3
                self._network.physical.add_epr_to_channel(epr_virtual, (node1, node3))
                # Remove os pares EPR antigos dos canais entre node1-node2 e node2-node3
                self._network.physical.remove_epr_from_channel([epr1], (node1, node2))
                self._network.physical.remove_epr_from_channel([epr2], (node2, node3))

                # Atualiza o contador de EPRs utilizados
                self.used_eprs += 2

                # Remove o segundo nó da rota, pois o swapping foi realizado
                route.pop(1)
            else:
                # Se não há um terceiro nó, apenas remove o segundo nó da rota
                route.pop(1)

        # Loga o sucesso do entanglement swapping
        self.logger.log(f'Entanglement Swapping concluído com sucesso entre {Alice} e {Bob}')
        return 1

    def get_avg_size_routes(self):
        """
        Calcula o tamanho médio das rotas utilizadas, considerando o número de saltos (arestas) entre os nós.
        
        returns:
            float: Tamanho médio das rotas utilizadas.
        """
        total_size = 0
        num_routes = 0
        
        # Itera sobre as rotas armazenadas no dicionário
        for route in self.routes_used.values():
            total_size += len(route) - 1  # Soma o número de arestas (saltos), que é o número de nós menos 1
            num_routes += 1  # Conta o número de rotas
        
        # Calcula a média, se houver rotas válidas
        if num_routes > 0:
            self.avg_size_routes = total_size / num_routes
        else:
            # Retorna 0 se não houver rotas válidas
            self.avg_size_routes = 0.0
        
        return self.avg_size_routes
