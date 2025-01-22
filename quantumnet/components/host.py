
from ..objects import Logger, Qubit

class Host():
    def __init__(self, host_id: int, probability_on_demand_qubit_create: float = 0.5, probability_replay_qubit_create: float = 0.5, max_qubits_create: int = 10, memory_size: int = 10) -> None:
        # Sobre a rede
        self._host_id = host_id
        self._connections = []
        # Sobre o host
        self._memory = []
        self._memory_size = memory_size
        self._max_qubits_create = max_qubits_create
        self._probability_on_demand_qubit_create = probability_on_demand_qubit_create
        self._probability_replay_qubit_create = probability_replay_qubit_create
        self._routing_table = {}
        self._routing_table[host_id] = [host_id]
        self._Black_Hole = False
        self._prob_entanglement_swapping = None
        self._prob_target_entanglement_swapping = None
        self._Black_Hole_target = None
        # Sobre a execução
        self.logger = Logger.get_instance()
    def __str__(self):
        return f'{self.host_id}'
    
    @property
    def host_id(self):
        """
        ID do host. Sempre um inteiro.

        Returns:
            int : Nome do host.
        """
        return self._host_id
    
    @property
    def connections(self):
        """
        Conexões do host.

        Returns:
            list : Lista de conexões.
        """
        return self._connections
    
    @property
    def memory(self):
        """
        Memória do host.

        Returns:
            list : Lista de qubits.
        """
        return self._memory
    
    @property
    def routing_table(self):
        """
        Tabela de roteamento do host.
        Returns:
            dict : Tabela de roteamento.
        """
        return self._routing_table
    
    @property
    def black_hole(self):
        """
        Revela se o host é um Black Hole
        """
        return self._Black_Hole

    @property
    def prob_entanglement_swapping(self):
        """
        Taxa de sucesso no entanglement swapping do host
        Returns:
            float: Taxa de sucesso do entanglement swapping
        """
        return self._prob_entanglement_swapping
    
    @property
    def prob_target_entanglement_swapping(self):
        """
        Taxa de sucesso no entanglement swapping do host em relação ao alvo
        Returns:
            float: Taxa de sucesso do entanglement swapping
        """
        return self._prob_target_entanglement_swapping
    
    @property
    def black_hole_target(self):
        """
        Alvos que o host deseja afetar o entanglement swapping
        Returns:
            list: Lista com os alvos
        """
        return self._Black_Hole_target
    
    def get_last_qubit(self):
        """
        Retorna o último qubit da memória.

        Returns:
            Qubit : Último qubit da memória.
        """
        try:
            q = self.memory[-1]
            self.memory.remove(q)
            return q
        except IndexError:
            raise Exception('Não há mais qubits na memória.')
    
    def add_connection(self, host_id_for_connection: int):
        """
        Adiciona uma conexão ao host. Uma conexão é um host_id, um número inteiro.

        Args:
            host_id_for_connection (int): Host ID do host que será conectado.
        """
        
        if type(host_id_for_connection) != int:
            raise Exception('O valor fornecido para host_id_for_connection deve ser um inteiro.')
        
        if host_id_for_connection not in self.connections:
            self.connections.append(host_id_for_connection),

    def add_qubit(self, qubit: Qubit):
        """
        Adiciona um qubit à memória do host.

        Args:
            qubit (Qubit): O qubit a ser adicionado.
        """
        
        self.memory.append(qubit)
        Logger.get_instance().debug(f'Qubit {qubit.qubit_id} adicionado à memória do Host {self.host_id}.')



    def set_routing_table(self, routing_table: dict):
        """
        Define a tabela de roteamento do host.
        Args:
            routing_table (dict): Tabela de roteamento.
        """

        self._routing_table = routing_table

    def info(self):
        """
        Retorna informações sobre o host.
        Returns:
            dict : Informações sobre o host.
        """

        return {
            'host_id': self.host_id,
            'memory': len(self.memory),
            'routing_table': "No registration" if self.routing_table == None else self.routing_table
        }

    def announce_to_controller_app_has_finished(self):
        """
        Informa ao controlador que a aplicação terminou.
        """

        print(f'Host {self.host_id} informou ao controlador que a aplicação terminou.')

    def setBlackHole(self, black_hole: bool) -> None:
        """
        Define se o host é um Black Hole
        """

        self._Black_Hole = black_hole

    def setEntanglementSwappingProb(self, new_probability: float) -> None:
        """
        Define uma nova probabilidade de sucesso para o entanglement swapping do host

        Args:
            new_probability: Float com a nova probabilidade
        """

        self._prob_entanglement_swapping = new_probability

    def setTargetEntanglementSwappingProb(self, new_probability: float) -> None:
        """
        Define uma nova probabilidade de sucesso para o entanglement swapping do host com o alvo

        Args:
            new_probability: Float com a nova probabilidade
        """

        self._prob_target_entanglement_swapping = new_probability

    def addBlackHoleTarget(self, target: 'Host') -> None:
        """
        Adiciona um alvo para o Host atacar durante o entanglement swapping
        """

        if self._Black_Hole_target == None:
            self._Black_Hole_target = [target]
        else:
            self._Black_Hole_target.append(target)