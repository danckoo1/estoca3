import Aux_module as t
from math import floor
import numpy as np

class Scrat:
    '''
    Entidad creada con el fin de contener la logica detras de la ficha, ademas por simplicidad
    posee algunos metodos encargados de la transformacion de posiciones a index en la matriz, 
    por ejemplo transformar A1 a 0 y viceversa.
    '''

    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.original_row = r
        self.original_col = c    #sistema cordenado (fila, columna)
        self.max = 4 #maximo ancho y alto del tablero
        self.bellota_row = 2
        self.bellota_col = 2

    def white(self, row, col):
        '''
        Funcion utilizada para saber si las posiciones en que se encuentra la
        reina son blancas o no.
        '''
        if (row + col) % 2 == 0:
            return True
        return False

    def blue(self, row, col):
        '''
        Funcion utilizada para saber si las posiciones en que se encuentra la
        reina son negras o no.
        '''
        bol = True
        if self.white(row, col):
            bol = False
        return bol

    def espacio_right(self):
        '''
        nos retorna la cantidad de espacios disponibles hacia la derecha desde la posicion
        actual de la reina
        '''
        return self.max - self.col

    def espacio_left(self):
        '''
        nos retorna la cantidad de espacios disponibles hacia la izquierda desde la posicion
        actual de la reina
        '''
        return self.col

    def espacio_up(self):
        '''
        nos retorna la cantidad de espacios disponibles hacia arriba desde la posicion
        actual de la reina
        '''
        return self.max - self.row

    def espacio_down(self):
        '''
        nos retorna la cantidad de espacios disponibles hacia abajo desde la posicion
        actual de la reina
        '''
        return self.row
    
    def movimientos_disp(self):
        '''
        Cumple dos misiones simultaneamente, calcula la cantidad de movimientos viables como un int,
        al mismo tiempo que almacena cuales son dichas posiciones viables para moverse en un listado.
        retorna mov(int), posiciones(list).
        '''
        if self.white(self.row, self.col): #celda blanca
            posiciones = [] # posiciones viables desde la actual
            mov = 0
            color = "white"
            directions = ["up", "down", "left", "right"] 
            for dir_ in directions:
                if dir_ == "up" and self.espacio_up() > 0:
                    posiciones.append((self.row + 1, self.col))
                    mov += 1

                elif dir_ == "down" and self.espacio_down() > 0:
                    posiciones.append((self.row - 1, self.col))
                    mov += 1

                elif dir_ == "left" and self.espacio_left() > 0:
                    posiciones.append((self.row, self.col - 1))
                    mov += 1

                elif dir_ == "right" and self.espacio_right() > 0:
                    posiciones.append((self.row, self.col + 1))
                    mov += 1
        
        elif self.blue(self.row, self.col): #celda azul
            posiciones = [] # posiciones viables desde la actual
            mov_b = 0
            mov_w = 0
            color = "blue"
            directions = ["up", "down", "left", "right", "up_right", "up_left", "down_right", "down_left"] 
            for dir_ in directions:
                if dir_ == "up" and self.espacio_up() > 0:
                    pos = (self.row + 1, self.col)
                    if self.white(*pos):
                        mov_w += 1
                    else:
                        mov_b += 1
                    posiciones.append(pos)

                elif dir_ == "down" and self.espacio_down() > 0:
                    pos = (self.row - 1, self.col)
                    if self.white(*pos):
                        mov_w += 1
                    else:
                        mov_b += 1
                    posiciones.append(pos)

                elif dir_ == "left" and self.espacio_left() > 0:
                    pos = (self.row, self.col - 1)
                    if self.white(*pos):
                        mov_w += 1
                    else:
                        mov_b += 1
                    posiciones.append(pos)

                elif dir_ == "right" and self.espacio_right() > 0:
                    pos = (self.row, self.col + 1)
                    if self.white(*pos):
                        mov_w += 1
                    else:
                        mov_b += 1
                    posiciones.append(pos)

                elif dir_ == "down_right" and self.espacio_down() > 0 and self.espacio_right() > 0:
                    pos = (self.row - 1, self.col + 1)
                    if self.white(*pos):
                        mov_w += 1
                    else:
                        mov_b += 1
                    posiciones.append(pos)

                elif dir_ == "down_left" and self.espacio_down() > 0 and self.espacio_left() > 0:
                    pos = (self.row - 1, self.col - 1)
                    if self.white(*pos):
                        mov_w += 1
                    else:
                        mov_b += 1
                    posiciones.append(pos)

                elif dir_ == "up_right" and self.espacio_up() > 0 and self.espacio_right() > 0:
                    pos = (self.row + 1, self.col + 1)
                    if self.white(*pos):
                        mov_w += 1
                    else:
                        mov_b += 1
                    posiciones.append(pos)

                elif dir_ == "up_left" and self.espacio_up() > 0 and self.espacio_left() > 0:
                    pos = (self.row + 1, self.col - 1)
                    if self.white(*pos):
                        mov_w += 1
                    else:
                        mov_b += 1
                    posiciones.append(pos)
            mov = {"mov_b": mov_b, "mov_w": mov_w}
        return mov, posiciones, color

    def move(self, row, col):
        '''
        Desplaza a la reina a una nueva posicion 
        '''
        self.row = row
        self.col = col
    
    def d2_to_d1(self, row, col):
        return (self.max + 1) * row + col
    
    def g_matrix(self):
        '''
        Crea la matriz P asociada al problema en que cada entrada es un float,
        luego es esta matriz la usada para los calculos.
        '''
        matrix = []
        for row in range(self.max + 1): #0,...,4
            for col in range(self.max + 1): #0,...,4
                self.move(row, col) #movemos la matriz atraves de todo el tablero

                mov, posiciones, color = self.movimientos_disp() 
                probabilidades_row = self.probabilidades(color, posiciones, mov)

                matrix.append(probabilidades_row)
        self.move(self.original_row, self.original_col) #devolvemos la reina a su posicion de partida
        return matrix
    
    def g_matrix_print(self):
        '''
        Misma logica detras del metodo anterior, pero en este caso construimos una 
        matriz en que cada una de sus probabilidades son str, a excepcion de los 0s, 
        para una mejor visualizacion al hacer prints o al guardarla.
        '''
        matrix = []
        for row in range(self.max + 1): #0,...,4
            for col in range(self.max + 1): #0,...,4
                self.move(row, col) #movemos la matriz atraves de todo el tablero
                mov, posiciones, color = self.movimientos_disp() 
                probabilidades_row = self.probabilidades_print(color, posiciones, mov)
                matrix.append(probabilidades_row)
        self.move(self.original_row, self.original_col) #devolvemos la reina a su posicion de partida
        return matrix

    def probabilidades(self, color, posiciones, mov):
        if color == "blue":
            probabilidades_row = [0]*((self.max + 1)**2)
            if (self.bellota_row, self.bellota_col) in posiciones:
                for pos in posiciones:
                    i = self.d2_to_d1(*pos)
                    total = (mov["mov_w"] - 1) + mov["mov_b"] * 2 + 4
                    if self.white(*pos):
                        if pos == (self.bellota_row, self.bellota_col):
                            probabilidades_row[i] = 4/total
                        else:
                            probabilidades_row[i] = 1/total
                    else:
                        probabilidades_row[i] = 2/total
            else:
                for pos in posiciones:
                    i = self.d2_to_d1(*pos)
                    total = mov["mov_w"] + mov["mov_b"] * 2
                    if self.white(*pos):
                        probabilidades_row[i] = 1/total
                    else:
                        probabilidades_row[i] = 2/total
            
        elif color == "white":
            probabilidades_row = [0]*((self.max + 1)**2)
            for pos in posiciones:
                i = self.d2_to_d1(*pos)
                probabilidades_row[i] = 1/mov
        return probabilidades_row
    
    def probabilidades_print(self, color, posiciones, mov):
        if color == "blue":
            probabilidades_row = ["0"]*((self.max + 1)**2)
            if (self.bellota_row, self.bellota_col) in posiciones:
                for pos in posiciones:
                    i = self.d2_to_d1(*pos)                 
                    total = (mov["mov_w"] - 1)  + mov["mov_b"] * 2 + 4
                    if self.white(*pos):
                        if pos == (self.bellota_row, self.bellota_col):
                            probabilidades_row[i] = f"4/{total}"
                        else:
                            probabilidades_row[i] = f"1/{total}"
                    else:
                        probabilidades_row[i] = f"2/{total}"
            else:
                for pos in posiciones:
                    i = self.d2_to_d1(*pos)
                    
                    total = mov["mov_w"] + mov["mov_b"]*2
                    if self.white(*pos):
                        probabilidades_row[i] = f"1/{total}"
                    else:
                        probabilidades_row[i] = f"2/{total}"
            
        elif color == "white":
            probabilidades_row = ["0"]*((self.max + 1)**2)
            for pos in posiciones:
                i = self.d2_to_d1(*pos)
            
                probabilidades_row[i] = f"1/{mov}"
        return probabilidades_row


if __name__ == "__main__":
    '''
    Lo sentimos si el main es poco claro, pero a fin de cuentas es hacer los calculos
    matriciales respectivos, ahi veras a cuales corresponde cada uno
    '''

    ardilla = Scrat(4, 0)
    matrix = np.array(ardilla.g_matrix_print())
    '''
    b y d
    for k in (2,3,5,10,20,100,1000):
        matrix_n = np.linalg.matrix_power(matrix, k)
        f = np.array([0]*25)
        i = ardilla.d2_to_d1(4, 0)
        j = ardilla.d2_to_d1(2, 2)
        f[i] = 1
        fn = np.dot(f, matrix_n)
        pij = fn[j]
        print(f"{k}: {pij}")
    '''
    '''
    matrix1_n = np.linalg.matrix_power(matrix, 4)
    f1 = np.array([0]*25)
    i1 = ardilla.d2_to_d1(4, 0)
    j1 = ardilla.d2_to_d1(4, 4)
    f1[i1] = 1
    fn = np.dot(f1, matrix1_n)
    pij1 = fn[j1]
    
    matrix2_n = np.linalg.matrix_power(matrix, 3)
    f2 = np.array([0]*25)
    i2 = ardilla.d2_to_d1(4, 4)
    j2 = ardilla.d2_to_d1(2, 2)
    f2[i2] = 1
    fn = np.dot(f2, matrix2_n)
    pij2 = fn[j2]

    print(f"{str(pij1)[:8]}*{str(pij2)[:8]} : {pij1*pij2}")
    '''
    '''
    from gurobipy import GRB, Model, quicksum

    ardilla = Scrat(4, 0)
    matrix = np.array(ardilla.g_matrix())

    P = np.transpose(matrix)
    m=Model("xd")
    Pi = m.addVars(25, vtype=GRB.CONTINUOUS, name="pi")
    m.addConstrs((quicksum(P[j][i]*Pi[i] for i in range(25)) == Pi[j] for j in range(25)), name="pi = pit*P")
    m.addConstr(quicksum(Pi[i] for i in range(25)) == 1, name="sum(pi) = 1")
    m.setObjective(1, GRB.MAXIMIZE)
    m.update()
    m.optimize()
    m.write("Pi.sol")
    with open("Pi.sol", "r") as file:
        lines = file.readlines()
    with open("Pi.sol", "w") as file:
        c = -1
        for line in lines[2:]:
            line = line.split(" ")
            row = line[0][3:line[0].index("]")]
            f = int(row)//5
            c +=1
            if c == 5:
                c = 0
            file.write(f"Pi[{f},{c}] = {float(line[1])} \n")

    '''
    '''
    counter = 0
    text = ""
    row = ""
    for estado_final in range(25):
        counter += 1
        k = 1000
        matrix_n = np.linalg.matrix_power(matrix, k)
        f = np.array([0]*25)
        f[0] = 1
        fn = np.dot(f, matrix_n)
        pij = fn[estado_final]
        row = row + f" {pij} &"
        if counter == 5:
            text = text + row[:-1] + "\n"
            row = ""
            counter = 0
    print(text)
    '''
        
             

    



