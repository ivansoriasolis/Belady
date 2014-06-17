'''
Created on 13/06/2014

Simula las peticiones de marcos de pagina con tres clases: memoria, cpu y administrador de memoria, para detectar
la anomalia de Belady al incrementar lo marcos de pagina. 

@author: ivan
'''
from collections import deque
import random

class memoriaPrincipal(list):
    ''' clase que simula la memoria principal dividida en marcos '''
    def __init__(self, marcos=8):
        ''' el numero de marcos por defecto es 8 '''
        self.extend([None for a in range(0,marcos)])
        self.numMarcos=marcos      
    def cargarMarcoFIFO(self, numMarco):
        ''' comportamiento de cola de los marcos asignados'''
        if not self.__contains__(numMarco):
            self.pop(0)
            self.append(numMarco)
            return True
        else:
            return False
    def aumentarMarcos(self, cantidad = 1):
        self.extend([None for a in range(0,cantidad)])
        self.numMarcos += cantidad

class MMU:
    ''' administrador de memoria'''
    fallosPagina = 0;
    def asignarMarcoFIFO(self, numMarcoPedido, memoria):
        if memoria.cargarMarcoFIFO(numMarcoPedido):
            self.fallosPagina +=1
            return True
        else:
            return False
    def borrarMemoria(self, mem):
        for i in range(len(mem)):
            mem[i]=None
        
class CPU:
    ''' simula un CPU que realiza peticiones de memoria'''
    def __init__(self):
        pass
    def generaPeticiones(self, cantidad=10, rango=5):
        for c in range(cantidad):
            yield random.randrange(rango)

class simulador:
    def probarFallos(self, admin, mem, pedidos, detallado = 0):
        for num in pedidos:
            if admin.asignarMarcoFIFO(num, mem):
                descFallo = "FALLO"
            else:
                descFallo = "NO FALLO"
            if detallado:
                print("Marco pedido: ", num, " Reposicion:", mem, descFallo) 
    def anomaliaBelady2(self, parametros,iteraciones=1, aumento=1, detallado= True):
        ''' simula la prueba pedida y devuelve una lista con los resultados esperados'''
        #lectura de parametros de simulacion
        marcos = parametros['marcos']
        petic = parametros['peticiones']
        rango = parametros['rango']
        #declarando memoria, administrador y procesador
        memoria1 = memoriaPrincipal(marcos)
        memoria2 = memoriaPrincipal(marcos+aumento)
        administrador1 = MMU()
        administrador2 = MMU()
        procesador = CPU()
        
        contIteraciones = 1
        contAnomalias = 0
        
        while contIteraciones<=iteraciones:
            peticiones = list(procesador.generaPeticiones(petic, rango))
            administrador1.fallosPagina = 0
            administrador2.fallosPagina = 0
            self.probarFallos(administrador1,memoria1,peticiones,detallado)
            if detallado:
                print("---------------------------------------------------------------")
                print(administrador1.fallosPagina, " FALLOS EN ",len(peticiones) , " PETICIONES PARA ",memoria1.numMarcos, " MARCOS")
            self.probarFallos(administrador2,memoria2,peticiones,detallado)
            if detallado:
                print(administrador2.fallosPagina, " FALLOS EN ",len(peticiones) , " PETICIONES PARA ",memoria2.numMarcos, " MARCOS")
            if administrador2.fallosPagina > administrador1.fallosPagina:
                print("SE PRODUJO ANOMALIA DE BELADY")
                contAnomalias +=1
            else:
                if detallado:
                    print("\nNO SE PRODUJO ANOMALIA DE BELADY\n\n*******************************************************************")
            administrador1.borrarMemoria(memoria1)
            administrador2.borrarMemoria(memoria2)
            contIteraciones +=1
        return contAnomalias 

    
if __name__ == '__main__':
    sim = simulador()       
    
    param = {}
    param['marcos']=int(input("Cantidad de marcos disponibles: "))
    param['peticiones']=int(input("Cantidad de peticiones a probar: "))
    param['rango']=int(input("Rango de numeros de pagina pedidos: "))
    anomalias = sim.anomaliaBelady2(param,aumento=3,iteraciones=100,detallado=True)
    print("ANOMALIAS: ", anomalias)
#     adm1 = MMU()
#     adm2 = MMU()
#     mem1 = memoriaPrincipal(3)
#     mem2 = memoriaPrincipal(4)
#     pedidos = [3, 2, 1, 0, 3, 2, 4, 3, 2, 1, 0, 4 ]
#     sim.probarFallos(adm1, mem1, pedidos, detallado= True)
#     sim.probarFallos(adm2, mem2, pedidos, detallado= True)
#     print("---------------------------------------------------------------")
#     print(adm1.fallosPagina, " FALLOS EN ",len(pedidos) , " PETICIONES PARA ",mem1.numMarcos, " MARCOS")
#     print(adm2.fallosPagina, " FALLOS EN ",len(pedidos) , " PETICIONES PARA ",mem2.numMarcos, " MARCOS")
#     if adm2.fallosPagina > adm1.fallosPagina:
#         print("SE PRODUJO ANOMALIA DE BELADY")
#     else:
#         print("NO SE PRODUJO ANOMALIA DE BELADY")
    


        


