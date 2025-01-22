from quantumnet.components import Network, Host
from quantumnet.objects import Logger, Qubit

from random import randint, choice, uniform
from copy import copy

# For collect data
import pandas as pd

# For async run
import asyncio
from concurrent.futures import ProcessPoolExecutor

# For collect Data
from BHA_functions.datacollector import DataCollector

# For the simulation BenchMark
from datetime import datetime

class Color:
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[36m'
    PURPLE = '\033[35m'
    CLEAR = '\033[0m'

def initNetwork(
                topology: str,
                number_nodes: int,
                topology_args: tuple,
                simulation_log: bool = False,
                simulator_log: bool = False,
                ) -> Network:
    """
    Will initiate the network

    Args:
        topology: Set network's topology
        number_nodes: If the topology is not a grade, it will be the number of nodes in the network
        topology_args: Is a tuple with all args to selected the topology
        simulation_log: If True will activate logs of simulation
        simulator_log: If True will activate logs of simulator

    Returns:
        Network: Will return the Network
    """
    # Defining the network
    network = Network()

    # Defining the topology
    topology = topology.lower()

    if topology in ('grade', 'mesh'):
        network.set_ready_topology(topology, *topology_args)
    elif topology in ('linha', 'line', 'estrela', 'star', 'anel', 'ring'):
        network.set_ready_topology(topology, number_nodes)
    else:
        network.set_ready_topology(topology, number_nodes, *topology_args)

    # Draw simulation
    if simulation_log:
        network.draw()
    
    # Log of simulator
    if simulator_log:
        Logger.activate(Logger)
        
    return network

def selectBlackHoles(network: Network, 
                    num_black_holes: int,
                    black_hole_target: bool,
                    log: bool = False) -> list:
    """
    Randomly choose Black Holes

    Args:
        network: Network to wich the nodes belong
        num_black_holes: Number of Black Holes
        black_hole_target: If True each black hole will have one target, else, each Black Hole will attack the entire network
        log: If True will activate logs of simulation

    Returns:
        List: List with all Black Holes
    """
    all_hosts = copy(network.get_all_sorted_hosts())
    black_hole_list = []
    if num_black_holes > 0 and num_black_holes < len(all_hosts):
        for host in range(0, num_black_holes):
            valid = False
            while not valid:
                black_hole = choice(all_hosts)
                if black_hole not in black_hole_list:
                    black_hole.setBlackHole(black_hole=True)
                    valid = True

            black_hole_list.append(black_hole)


        if black_hole_target:
            for black_hole in black_hole_list:
                valid = False
                while not valid:
                    target = choice(all_hosts)
                    if target not in black_hole_list:
                        black_hole.addBlackHoleTarget(target=target)
                        valid = True

    if log:
        id_list = [black_hole.host_id for black_hole in black_hole_list]
        print(f"A lista de Black Holes é: {id_list}")

    return black_hole_list

def selectAliceBob(network: Network, 
                    black_hole_list: list,
                    log: bool = False) -> tuple[Host, Host]:
    """
    Will define the nodes: Alice, Bob

    Args:
        network: Network to wich the nodes belong
        black_hole_list: List with all Black Holes
        log: If True will activate logs of simulation

    Returns:
        (Host, Host): Will return respectively: Alice host, Bob host
    """
    valid = False
    while not valid:
        alice_id = randint(0, len(network.hosts)-1)
        alice = network.get_host(alice_id)
        if alice not in black_hole_list:
            valid = True
    if log:
        print(f"O id de Alice é: {Color.PURPLE}{alice}{Color.CLEAR}")

    valid = False
    while not valid:
        bob_id = randint(0, len(network.hosts)-1)
        bob = network.get_host(bob_id)
        if bob_id != alice_id:
            valid = True
    if log:
        print(f"O id de Bob é: {Color.BLUE}{bob}{Color.CLEAR}")

    return alice, bob

def getRoute(network: Network,
                alice: Host, 
                bob: Host,
                log: bool = False) -> list:
    """
    Will define the route of Alice to Bob

    Args:
        network: Network to wich the nodes belong
        alice: Sender host
        bob: Receiver host
        log: If True will activate logs of simulation

    Returns:
        List: List with the rotes of Alice to Bob
    """

    # Defining the route of Alice to Bob
    route = network.networklayer.short_route_valid(Alice=alice.host_id, Bob=bob.host_id)
    if log:
        print(f"Alice: {Color.PURPLE}{alice}{Color.CLEAR} deseja se comunicar com Bob: {Color.BLUE}{bob}{Color.CLEAR} pela rota {route}")
    
    return route

def setNetworkSwappProb(network: Network, 
                        network_prob: float,  
                        malicious_hosts_prob: float,
                        black_hole_target: bool) -> None:
    """
    Will set network's probability of success of entanglement swapping

    Args:
        network: Network to wich the nodes belong
        network_prob: Network's entanglement swapping probability
        malicious_hosts_prob: Malicious host probability
        black_hole_target: If True each black hole will have one target, else, each Black Hole will attack the entire network
    """
    for temp_host in network.hosts.values():

        if temp_host.black_hole and black_hole_target == False:
            temp_host.setEntanglementSwappingProb(malicious_hosts_prob)

        elif temp_host.black_hole and black_hole_target == True:
            temp_host.setEntanglementSwappingProb(network_prob)
            temp_host.setTargetEntanglementSwappingProb(malicious_hosts_prob)
    
        else:
            temp_host.setEntanglementSwappingProb(network_prob)

def addQubits(host_A: Host, 
                host_B: Host, 
                counter: int) -> int:
    """
    Will add qubits to both hosts

    Args:
        host_A: Host that wants to add the qubit
        host_B: Host that wants to add the qubit
        counter: Counter to index qubits

    Returns:
        Counter: Return updated counter
    """
    temp_qubit_counter = counter
    
    qubit = Qubit(temp_qubit_counter, uniform(0.8, 1))
    host_A.add_qubit(qubit)

    qubit = Qubit(temp_qubit_counter+1, uniform(0.8, 1))
    host_B.add_qubit(qubit)

    temp_qubit_counter += 2

    return temp_qubit_counter
    
# Creating entanglement between neighbors hosts
def createEntanglements(route: list, 
                        network: Network,
                        number_of_entanglements: int,
                        log: bool = False) -> None:
    """
    Create entangleds pairs between the hosts of route

    Args:
        route: list with Host_A and Host_B
        network: Network to wich the nodes belong
        number_of_entanglements: Number of desired pairs
        log: If True will activate logs of simulation
    """
    # Used qubits
    qubit_counter = 0

    # Loop to create new entanglements
    for entanglement in range(0, number_of_entanglements):
        
        # Save the qubit index to create new qubits
        temp_qubit_counter = qubit_counter

        # Create new entanglement to every host in the route
        host_A = network.get_host(route[0])
        host_B = network.get_host(route[1])

        # Will trying until entangled be successfully created
        entangled = False
        while not entangled:

            # If dont't have qubit on memory will add
            if host_A.memory == [] or host_B.memory == []:
                temp_qubit_counter = addQubits(host_A=host_A, host_B=host_B, counter=temp_qubit_counter)
            if log:
                print(f"Tentativa de entanglement entre {host_A} e {host_B}")

            # Trying do entanglement between host_A and host_B
            entangled = network.physical.entanglement_creation_heralding_protocol(host_A, host_B)

            if not entangled:
                temp_qubit_counter = addQubits(host_A=host_A, host_B=host_B, counter=temp_qubit_counter)
                
        # Update counter to qubit index
        qubit_counter += temp_qubit_counter

    if log:
        print(f"Foram criados {qubit_counter} qubits a mais para a realização dos {entanglement+1} entanglements")

def replenishNetwork(network: Network, 
                    edges: list, 
                    number_of_entanglements: int,
                    log: bool) -> None:
    """
    Will replenish the network resources

    Args:
        network: Network to wich the nodes belong
        edges: Physical edges of network
        number_of_entanglements: Number of entangled pair will be create to replanish network
        log: If True will activate logs of simulation
    """
    if log:
        print("Repondo os recursos da rede")
    for edge in edges:
        createEntanglements(route=edge, network=network, number_of_entanglements=number_of_entanglements, log=log)

def createRequest(network: Network, 
                  alice: Host, 
                  bob: Host, 
                  attempts: int, 
                  route: list,
                  log: bool = False) -> tuple[int, int]:
    """
    Will create a request from Alice to Bob

    Args:
        network: Network to wich the nodes belong
        alice: Sender host
        bob: Receiver host
        attempts: Number of attempts on a request
        route: Route of Alice to Bob
        log: If True will activate logs of simulation

    Returns:
        (int, int): Will return entanglement result and counter of attempts
    """
    counter = 0
    for attempt in range(0, attempts):
        entangled = network.networklayer.entanglement_swapping(alice.host_id, bob.host_id, route=route)
        if entangled != 0:
            break
        counter += 1

    if log:        
        print(f"Alice irá se comunicar com Bob pela Rota: {route}")
        if entangled == -1:
            print(f"{Color.RED}Não é possível realizar o entanglement swapping{Color.CLEAR}")
        elif entangled == 0:
            print(f"O entanglement falhou com o total de {Color.RED}{attempts}{Color.CLEAR} tentativas")
        else:
            print(f"O entanglement foi um sucesso depois de {Color.RED}{counter}{Color.CLEAR} tentativas")

        network.get_host(alice.host_id).announce_to_controller_app_has_finished()

    return entangled, counter

def collectDataFrame(data: dict, 
                     index: int) -> pd.DataFrame:
    """
    Will create a pandas DataFrame to analyze data of simulation

    Args:
        data: Dict with all simulation informations
        index: Index of DataFrame row

    Returns:
        DataFrame: DataFrame with all simulation informations
    """
    success = impossible = fail = attempts = 0
    for run in data['Requests']:
        if data['Requests'][run]['Entangled'] == 1:
                success += 1
        elif data['Requests'][run]['Entangled'] == -1:
                impossible += 1
        elif data['Requests'][run]['Entangled'] == 0:
                fail += 1
    
        attempts += data['Requests'][run]['Attempts']
        
    runs = len(data['Requests'].keys())

    success_tax = (success/runs) * 100
    impossible_tax = (impossible/runs) * 100
    fail_tax = (fail/runs) * 100
    avg_attempts = attempts/runs

    data_df = {
    "Requests":[runs],
    "Topology":[data['Topology']],
    "Number of Nodes":[data['Number of Nodes']],
    "Success Tax":[success_tax],
    "Swapp Error Tax":[fail_tax],
    "Impossible Swapp Tax":[impossible_tax],
    "Average Attempts":[avg_attempts],
    "Used Eprs":[data['Used Eprs']],
    "Avg Fidelity Route":[data["Avg Fidelity Route"]],
    "Black Holes":[len(data["Black Holes"])]
    }

    data_df = pd.DataFrame(data_df, index=[index])

    return data_df

def simulation(
        topology: str,
        number_nodes: int,
        topology_args: tuple,
        entanglements_replanished: int = 10, 
        requests: int = 100,
        attempts_per_request: int = 2,
        network_prob: float | None = None, 
        num_black_holes: int = 1, 
        black_hole_prob: float | None = None,
        black_hole_target: bool = False,
        data_Frame_index: int = 1,
        simulation_log: bool = False,
        simulator_log: bool = False,
        ) -> dict:
        """Run the simulation with the desired parameters

            Args:
                topology: Set network's topology
                number_nodes: If the topology is not a grade, it will be the number of nodes in the network
                *topology_args: Args of selected topology
                entanglements_replanished: Number of entangled pair will be create to replanish network
                requests: Number of requests in simulation
                attempts_per_request: Number of attempts on a request
                network_prob: Network's entanglement swapping probability
                num_black_holes: Number of Black Holes in the network
                black_hole_prob: Malicious host probability
                black_hole_target: If True each black hole will have one target, else, each Black Hole will attack the entire network
                data_Frame_index: Index of pandas DataFrame
                simulation_log: If True will activate logs of simulation
                simulator_log: If True will activate logs of simulator


            Returns:
                (Dict, DataFrame): Return all information of run on simulation with a dict and a pandas DataFrame"""

        # Create network
        network = initNetwork(
                              topology=topology,
                              number_nodes=number_nodes, 
                              topology_args=topology_args,
                              simulation_log=simulation_log,
                              simulator_log=simulator_log,
                              )

        # Set real edges
        real_edges = network.edges

        # Select Black Hole list
        black_hole_list = selectBlackHoles(network=network, num_black_holes=num_black_holes, black_hole_target=black_hole_target, log=simulation_log)

        # Select network Prob
        setNetworkSwappProb(network=network, 
                            network_prob=network_prob,
                            malicious_hosts_prob=black_hole_prob, 
                            black_hole_target=black_hole_target)
        
        # Dict with requests data
        data = {}

        # Add Network's topology
        data['Topology'] = network.topology

        # Add Number of nodes
        data['Number of Nodes'] = len(network.hosts)

        # Add Black Hole list
        data["Black Holes"] = [host.host_id for host in black_hole_list]

        if black_hole_target:
                data["Black Holes Target"] = {black_hole.host_id:black_hole.black_hole_target[0].host_id for black_hole in black_hole_list}

        # Add Used Eprs in data
        data["Used Eprs"] = None

        # Add average fidelity of route
        data["Avg Fidelity Route"] = 0

        # Add hash to requests
        data["Requests"] = {}

        # Run requests
        for request in range(0, requests):
                
                # Will Replanish the resources 
                if request != 0 and request % 10 == 0:
                        replenishNetwork(network=network, edges=real_edges, 
                                         number_of_entanglements=entanglements_replanished, log=False)
                        if simulation_log:
                                print(f"{Color.GREEN}Rede foi reabastecida no request: {request}{Color.CLEAR}")

                # Defining the nodes
                alice, bob = selectAliceBob(network=network, black_hole_list=black_hole_list, log=simulation_log)

                # Defining route
                route = getRoute(network=network, alice=alice, bob=bob)

                # Create request
                entangled, attempts_counter = createRequest(network=network, alice=alice, 
                                                            bob=bob, attempts=attempts_per_request, 
                                                            route=route, log=simulation_log)

                # Collect request data
                data['Requests'][f"request:{request+1}"] = {"Alice & Bob": [alice.host_id, bob.host_id], 
                                                            "Route": route, 
                                                            "Entangled": entangled, 
                                                            "Attempts": attempts_counter}

        # Add eprs data
        data["Used Eprs"] = network.get_total_useds_eprs()

        # Collect data of Average fidelity route
        data["Avg Fidelity Route"] = network.avg_fidelity_route

        # Collect to the Data Frame
        data_df = collectDataFrame(data=data, index=data_Frame_index)
        
        return data, data_df


async def runSimulations(
        runs: int, 
        topology: str,
        number_nodes: int,
        topology_args: tuple,
        entanglements_replanished: int = 10, 
        requests: int = 100,
        attempts_per_request: int = 2,
        network_prob: float | None = None, 
        num_black_holes: int = 1, 
        black_hole_prob: float | None = None,
        black_hole_target: bool = False,
        ) -> pd.DataFrame:
    '''
    Will run some simulations and collect data with pandas DataFrame        

    Args:
        runs: Number of times of simulation will run
        topology: Set network's topology
        number_nodes: If the topology is not a grade, it will be the number of nodes in the network
        topology_args: Tuple with all args of the selected topology 
        entanglements_replanished: Number of entangled pair will be create to replanish network
        requests: Number of requests in simulation
        attempts_per_request: Number of attempts on a request
        network_prob: Network's entanglement swapping probability
        num_black_holes: Number of Black Holes in the network
        black_hole_prob: Malicious host probability
        black_hole_target: If True each black hole will have one target, else, each Black Hole will attack the entire network

    Returns:
        DataFrame: Will return pandas DataFrame with all data storage
    '''
    simulations_df = None
    for run in range(0, runs):
        await asyncio.sleep(0)
        data, temp_data_df = simulation(
            topology=topology,
            number_nodes=number_nodes,
            topology_args=topology_args,
            entanglements_replanished=entanglements_replanished,
            requests=requests,
            attempts_per_request=attempts_per_request,
            network_prob=network_prob,
            num_black_holes=num_black_holes,
            black_hole_prob=black_hole_prob,
            black_hole_target = black_hole_target,
            data_Frame_index=run,
            simulation_log=False,
            )
        if simulations_df == None:
            simulations_df = [temp_data_df]
        else:
            simulations_df.append(temp_data_df)

    return pd.concat(simulations_df)


async def asyncSimulations(number_tasks: int, **kwargs) -> DataCollector:
    """
    Will partition all simulation in async tasks

    Args:
        number_tasks: Number of partitions
        **kwargs: Args of simulations
    
    Returns:
        DataCollector: DataCollector with all simulations data
    """
    
    runs = kwargs['runs']
    if runs < number_tasks:
        number_tasks = runs
    runs_per_task = int(runs/number_tasks)

    args = [arg for arg in kwargs.values()]
    args[0] = runs_per_task

    module = runs % number_tasks

    tasks = []
    for task in range(0, number_tasks):
        temp_args = copy(args)
        if task < module and module > 0:
            temp_args[0] = runs_per_task + 1
        tasks.append(asyncio.create_task(runSimulations(*temp_args)))

    print(f"As simulações foram divididas em {len(tasks)} tasks")
    
    # return await asyncio.gather(*tasks)
    results = await asyncio.gather(*tasks)
    
    simulations_df = pd.concat(results)
    simulations_df.reset_index(inplace=True)
    simulations_df.pop('index')

    return DataCollector(simulations_df)


def runSimulations_Linux(
        runs: int, 
        topology: str,
        number_nodes: int,
        topology_args: tuple,
        entanglements_replanished: int = 10, 
        requests: int = 100,
        attempts_per_request: int = 2,
        network_prob: float | None = None, 
        num_black_holes: int = 1, 
        black_hole_prob: float | None = None,
        black_hole_target: bool = False,
        ) -> pd.DataFrame:
    '''
    Will run some simulations and collect data with pandas DataFrame        

    Args:
        runs: Number of times of simulation will run
        topology: Set network's topology
        number_nodes: If the topology is not a grade, it will be the number of nodes in the network
        topology_args: Tuple with all args of the selected topology 
        entanglements_replanished: Number of entangled pair will be create to replanish network
        requests: Number of requests in simulation
        attempts_per_request: Number of attempts on a request
        network_prob: Network's entanglement swapping probability
        num_black_holes: Number of Black Holes in the network
        black_hole_prob: Malicious host probability
        black_hole_target: If True each black hole will have one target, else, each Black Hole will attack the entire network

    Returns:
        DataFrame: Will return pandas DataFrame with all data storage
    '''
    simulations_df: list | None = None
    for run in range(0, runs):
        data, temp_data_df = simulation(
            topology=topology,
            number_nodes=number_nodes,
            topology_args=topology_args,
            entanglements_replanished=entanglements_replanished,
            requests=requests,
            attempts_per_request=attempts_per_request,
            network_prob=network_prob,
            num_black_holes=num_black_holes,
            black_hole_prob=black_hole_prob,
            black_hole_target = black_hole_target,
            data_Frame_index=run,
            simulation_log=False,
            )
        
        if simulations_df == None:
            simulations_df = [temp_data_df]
        else:
            simulations_df.append(temp_data_df)

    return pd.concat(simulations_df)


def asyncSimulations_Linux(cores: int, **params) -> DataCollector:
    """
    Will partition all simulation in async processes

    Args:
        number_tasks: Number of partitions
        **params: Args of simulations
    
    Returns:
        DataCollector: DataCollector with all simulations data
    """

    runs = params['runs']
    if runs < cores:
        cores = runs
    runs_per_task = int(runs/cores)

    args: list = [
        runs_per_task,
        params['topology'],
        params['number_nodes'],
        params['topology_args'],
        params['entanglements_replanished'],
        params['requests'],
        params['attempts_per_request'],
        params['network_prob'],
        params['num_black_holes'],
        params['black_hole_prob'],
        params['black_hole_target']
    ]

    module = runs % cores

    tasks = []
    with ProcessPoolExecutor(max_workers=cores) as executor:
        for task in range(0, cores):
            temp_args = copy(args)
            if task < module and module > 0:
                temp_args[0] = runs_per_task + 1
            tasks.append(executor.submit(runSimulations_Linux, *temp_args))

    results = [task.result() for task in tasks]
    print(f"As simulações foram divididas em {len(tasks)} processos")
        
    simulations_df = pd.concat(results)
    simulations_df.reset_index(inplace=True)
    simulations_df.pop('index')

    return DataCollector(simulations_df)


if __name__ == "__main__":
    start = datetime.now()
    simulations_params = {
        'runs':100,
        'topology':'Ba',
        'number_nodes':20,
        'topology_args':(3,),
        'entanglements_replanished':10,
        'requests':100,
        'attempts_per_request':2,
        'network_prob':0.8,
        'num_black_holes':2,
        'black_hole_prob':0.1,
        'black_hole_target':True,
    }

    simulations_dc = asyncSimulations_Linux(cores=12, **simulations_params)
    print(f"As {simulations_params['runs']} simulações finalizaram no tempo de: {datetime.now()-start}")

    print(simulations_dc.df)