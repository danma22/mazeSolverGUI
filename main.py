import sys
from mazeSolver import get_solved_maze
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# Clase que representa el grid widget donde se dibujan los elementos del laberinto
class GridWidget(QWidget):
    # Constructor de la clase
    def __init__(self, map=None ,parent=None):
        super().__init__(parent)
        
        self.map = map # se guarda el mapa
        self.setMinimumSize(parent.width+1, parent.height+1) # El tamaño mínimo del widget

        self.source_position = None # Posición del source
        self.target_position = None # Posición del target
        self.obstacle_positions = [] # Lista de las posiicones de las celdas obstaculos
        self.path_positions = [] # Lista de las posiciones del camino encontrado

        self.setting_source = False # Indica si se cambiara la posicion del source
        self.setting_target = False # Indica si se cambiara la posicion del target
        self.map2grid() # Se transforma el mapa en un grid que pueda leer la clase

    # Método que otorga a la clase una variable grid, matriz con todos los caractares del mapa
    def map2grid(self):
        # Dividir el mapa en líneas individuales
        map_lines = self.map.strip().split('\n')
        map_lines = [linea.strip() for linea in map_lines]
        
        # Obtener el número de filas y columnas
        self.rows = len(map_lines)
        self.cols = len(map_lines[0]) if map_lines else 0
        
        # Se crea el grid vacio para almacenar los caracteres
        self.grid = [[' '] * self.cols for _ in range(self.rows)]
        
        # Rellenar el grid con los caracteres del mapa
        for i, row in enumerate(map_lines):
            for j, col in enumerate(row):
                # El caracter o indica que es el source
                if col == 'o':
                    self.source_position = (i, j)

                # El caracter x indica que es el target
                if col == 'x':
                    self.target_position = (i, j)

                # El caracter # indica que es una pared y se agrega a la lista de obstaculos
                if col == '#':
                    self.obstacle_positions.append((i, j))

                self.grid[i][j] = col
 
    # Método que define el valor del mapa de acuerdo a las posiciones del grid
    def grid2map(self):
        # Se restablece el valor del mapa
        self.map = "\n"
        # El grid se recorre y se agrega cada caracter en un nuevo mapa
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.map += self.grid[i][j]
            self.map += "\n"

    # Método que se llama al actualizar la vista con update, dibuja el grid y las celdas de color
    def paintEvent(self, event):
        painter = QPainter(self)

        # Se establece las dimensiones de las celdas
        cell_width = int(self.width() / self.cols)
        cell_height = int(self.height() / self.rows)

        # Dibuja los bordes de la cuadricula
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        painter.setPen(pen)

        for i in range(self.cols + 1):
            x = i * cell_width
            painter.drawLine(int(x), 0, int(x), int(self.height()))

        for i in range(self.rows + 1):
            y = i * cell_height
            painter.drawLine(0, int(y), int(self.width()), int(y))
            
        # Dibuja los colores de las celdas de acuerdo al tipo de las mismas
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == "#": # Dibujar el obstaculo o pared
                    obstacle_x = j * cell_width
                    obstacle_y = i * cell_height
                    painter.setBrush(QColor("black"))
                    painter.drawRect(obstacle_x, obstacle_y, cell_width, cell_height)
                    
                elif cell == ".": # Dibujar el camino
                    path_x = j * cell_width
                    path_y = i * cell_height
                    painter.setBrush(QColor("yellow"))
                    painter.drawRect(path_x, path_y, cell_width, cell_height)  
                    
                elif cell == "o": # Dibujar el punto source
                    source_x = j * cell_width
                    source_y = i * cell_height
                    painter.setBrush(QColor("green"))
                    painter.drawRect(source_x, source_y, cell_width, cell_height)
                    
                elif cell == "x": # Dibujar el punto target
                    target_x = j * cell_width
                    target_y = i * cell_height
                    painter.setBrush(QColor("brown"))
                    painter.drawRect(target_x, target_y, cell_width, cell_height)

        painter.end()

    # Método que cambia el estado de la variable que indica que se cambiará la posicion del source
    def set_source_position(self):
        # Activa o desactia source setting
        self.setting_source = not self.setting_source
        self.setting_target = False
        self.update()  # Actualiza la vista para dibujar la celda source

    # Método que cambia el estado de la variable que indica que se cambiará la posicion del target
    def set_target_position(self):
        # Activa o desactia target setting
        self.setting_target = not self.setting_target
        self.setting_source = False
        self.update()  # Actualiza la vista para dibujar la celda target

    # Método del evento de presionar clic. Se enfoca en dibujar una celda target o source 
    def mousePressEvent(self, event):
        # Cambiar posicion del source
        if self.setting_source:
            # Obtener la posición del clic en el grid
            ancho_celda = int(self.width() / self.cols)
            alto_celda = int(self.height() / self.rows)
            col = event.pos().x() // ancho_celda
            row = event.pos().y() // alto_celda

            # Verificar si la posición pulsada ya es una posición de target o una posición de obstaculo
            if (row, col) != self.target_position and (row, col) not in self.obstacle_positions:
                # Verificar si la posición pulsada ya es una posición de source
                if (row, col) != self.source_position:
                    # Restablecer el valor anterior
                    if self.source_position is not None:
                        r, c = self.source_position
                        self.grid[r][c] = " "

                    # Establecer la posición de source
                    self.source_position = (row, col)
                    self.grid[row][col] = "o"

            self.update()  # Actualizar la vista para dibujar el punto de origen

        # Cambiar posicion del target
        elif self.setting_target:
            # Obtener la posición del clic en el grid
            ancho_celda = int(self.width() / self.cols)
            alto_celda = int(self.height() / self.rows)
            col = event.pos().x() // ancho_celda
            row = event.pos().y() // alto_celda

            # Verificar si la posición pulsada ya es una posición de source o una posición de obstaculo
            if (row, col) != self.source_position and (row, col) not in self.obstacle_positions:
                # Verificar si la posición pulsada ya es una posición de target
                if (row, col) != self.target_position:
                    # Restablecer el valor anterior
                    if self.target_position is not None:
                        r, c = self.target_position
                        self.grid[r][c] = " "

                    # Establecer la posición de target
                    self.target_position = (row, col)
                    self.grid[row][col] = "x"

            self.update()  # Actualizar la vista para dibujar los puntos de destino

    # Método que llama a la función para solucionar el laberinto y dibujar un nuevo grid y mapa
    def draw_solved_maze(self):
        # Se obtiene el nuevo mapa de acuerdo al grid
        self.grid2map()
        # Se obtiene el mapa ya resuelto
        self.map = get_solved_maze(self.map)
        # Se pasa el mapa a grid para que pueda ser dibujado el path
        self.map2grid()
        # Se actualiza la vista para reflejar la cuadricula resuelta
        self.update()

    # Método para limpiar la posición de target y source del grid
    def clear_grid(self):
        # Reestablece las propiedades de las celdas de source y target
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] != '#':
                    self.grid[i][j] = ' '

        # Se resetean los valores de target y source
        self.source_position = None
        self.target_position = None

        self.update()  # Actuaiza la vista para reflejar la cuadricula limpia


# Clase que representa la ventana de la aplicacions
class MazeSolverWindow(QWidget):
    # Constructor de la clase
    def __init__(self):
        super().__init__()
        self.title = 'Maze Solver Algorithm' # Titulo

        # Número de filas y columnas que tendrá el laberinto
        self.rows = 10
        self.columns = 30

        # Longitud estimada de la ventana
        self.width = self.columns * 25
        self.height = self.rows * 25

        # Mapa por default a resolver
        # Los caracteres de # indican que es la pared u obstaculo
        # El caracter o indica que es punto de partida o source del laberinto
        # El caracter x indica que es punto de destino o target del laberinto
        # Al momento de resolverse, los caracteres . indican el camino para solucionar el laberinto
        self.defaultMap = """
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

        # Varible que almacena el grid de la aplicacion
        self.grid_widget = GridWidget(map=self.defaultMap, parent=self)

        self.initUI() # Se inicializan los componentes de la interfaz

    # Método para dibujar los widgets de la ventana
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)
        self.setWindowIcon(QIcon('images/logo3.png'))

        layoutVertical = QVBoxLayout()
        self.setLayout(layoutVertical)
        
        # Grid Widget
        layoutVertical.addWidget(self.grid_widget)
        
        # Control Layout para los botones
        control_layout = QGridLayout()
        layoutVertical.addLayout(control_layout)

        # Todos los botones a usar
        self.set_source_button = QRadioButton("Set Source")
        self.set_target_button = QRadioButton("Set Target")
        self.clear_grid_button = QPushButton("Clear Grid")
        self.solve_maze_button = QPushButton("Solve Maze")
        
        #Estilo de los radio buttons
        self.set_source_button.setStyleSheet("QRadioButton::indicator"
                                            "{"
                                            "width : 20px;"
                                            "height : 20px;"
                                            "}")
        self.set_target_button.setStyleSheet("QRadioButton::indicator"
                                            "{"
                                            "width : 20px;"
                                            "height : 20px;"
                                            "}")

        # Posición de cada boton en el layout de control
        control_layout.addWidget(self.set_source_button, 0, 0)
        control_layout.addWidget(self.set_target_button, 0, 1)
        control_layout.addWidget(self.clear_grid_button,3,1)
        control_layout.addWidget(self.solve_maze_button,3,0)

        # Relación con sus métodos designados
        self.set_source_button.toggled.connect(self.grid_widget.set_source_position)
        self.set_target_button.toggled.connect(self.grid_widget.set_target_position)
        self.clear_grid_button.clicked.connect(self.clear_grid_clicked)
        self.solve_maze_button.clicked.connect(self.solve_maze)
        
        self.show() # Se muestra la ventana

    # Método para llamar a resolver el laberinto de la clase GridWidget
    def solve_maze(self):
        self.solve_maze_button.setEnabled(False) # Se desactiva el botón para evitar errores

        # En caso de no seleccionar un punto de partida no se realiza la accion
        if self.grid_widget.source_position is None:
            QMessageBox.warning(self, "Error", "Selecciona una celda de partida")
            return
        
        # En caso de no seleccionar un punto de destino no se realiza la accion
        if self.grid_widget.target_position is None:
            QMessageBox.warning(self, "Error", "Selecciona una celda de destino")
            return

        self.grid_widget.draw_solved_maze()

    # Método para llamar al método para limpiar el grid
    def clear_grid_clicked(self):
        self.grid_widget.clear_grid()
        self.solve_maze_button.setEnabled(True)

        self.set_source_button.setAutoExclusive(False)
        self.set_target_button.setAutoExclusive(False)

        # Limpiar los radio buttons
        self.set_source_button.setChecked(False)
        self.set_target_button.setChecked(False)

        self.set_source_button.setAutoExclusive(True)
        self.set_target_button.setAutoExclusive(True)


# Inicio de la ventana
if __name__ == '__main__':
    app = QApplication(sys.argv)
    astar_animation = MazeSolverWindow()
    sys.exit(app.exec_())