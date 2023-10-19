import math
from simpleai.search import SearchProblem, astar

# Clase que contiene los métodos para resolver el laberinto
class MazeSolver(SearchProblem):
    # Constructor de la clase
    def __init__(self, board):
        # Se define el mapa del laberinto y el punto inicial y de meta
        self.board = board
        self.goal = (0, 0)
        self.define_costs() # Se definen los costos por cada movimiento

        # Recorrer el mapa para buscar el inicio y meta del laberinto
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        super(MazeSolver, self).__init__(initial_state=self.initial)

    # Método para definir los costos por accion en un diccionario
    def define_costs(self):
        # Define le costo de movimiento alrededor del mapa
        cost_regular = 1.0
        cost_diagonal = 1.7

        # Crea un diccionario de costo
        self.costs = {
            "up": cost_regular,
            "down": cost_regular,
            "left": cost_regular,
            "right": cost_regular,
            "up left": cost_diagonal,
            "up right": cost_diagonal,
            "down left": cost_diagonal,
            "down right": cost_diagonal,
        }

    # Método que indica que acciones tomar para resolver el laberinto
    def actions(self, state):
        actions = []
        for action in self.costs.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)

        return actions
    
    # Actualiza el resultado
    def result(self, state, action):
        x, y = state

        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1
            
        new_state = (x, y)

        return new_state
    
    # Método que checa si la meta se alcanzo
    def is_goal(self, state):
        return state == self.goal
    
    # Método que calcula el costo de tomar una acción
    def cost(self, state, action, state2):
        return self.costs[action]
    
    # Heuristica que se usa para llegar a la solución
    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal

        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)

# Función que devuelve el mapa dado, ya resuelto
def get_solved_maze(map):
    # Convierte el mapa a una lista
    map = [list(x) for x in map.split("\n") if x]

    # Crear un objeto maze solver
    problem = MazeSolver(map)

    # Correr el solucionador
    result = astar(problem, graph_search=True)

    # Se extrae el camino de la solucion
    path = [x[1] for x in result.path()]

    # Se almacena el resultado y se retorna
    map_solved = "\n"
    for y in range(len(map)):
        for x in range(len(map[y])):
            if (x, y) == problem.initial:
                map_solved += 'o'
            elif (x, y) == problem.goal:
                map_solved += 'x'
            elif (x, y) in path:
                map_solved += '.'
            else:
                map_solved += map[y][x]
                
        map_solved += "\n"

    return map_solved

# Prueba de la clase
if __name__ == "__main__":
    # Define the map
    map = """
        ##############################
        #      o  #              # x #
        # ####    ########       #   #
        #    #    #              #   #
        #    ###     #####  ######   #
        #      #   ###   #           #
        #      #     #   #  #  #   ###
        #     #####    #    #  #     #
        #              #       #     #
        ##############################
    """
    print(map)
    x = get_solved_maze(map)
    print(x)

