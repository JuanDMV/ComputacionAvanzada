"""
Este codigo calcula las soluciones a la ecuación trascendente
para el coeficiente de transmisión como función de la frecuencia.
Esta ecuacion resulta de las condiciones de frontera en la capa no lineal
Aqui se utilizan 4 núcleos del procesador y los resultados de 
cada uno de ellos se fusionan en un archivo  omvalues_α_parallel.dat
"""

from multiprocessing import Process, Queue
import numpy as np
from scipy.special import ellipj
from scipy.optimize import bisect
import time


#Definicion de las constantes del problema

c = 300. #velocidad de la luz
ε = 10.0 #permitividad del medio lineal
ε0 = 1.0 #Permitividad eléctrica del vacio
μ = 1.036 #permeabilidad magnética del material
μ0 = 1.0 #permeabilidad magnetica del vacio
θ = np.pi/6.0 #angulo de incidencia en el vacío
p0 = np.sqrt(μ0*ε0-np.sin(θ)**2)
p = np.sqrt(μ*ε-np.sin(θ)**2) 
d = 5. #Ancho de la capa en milimetros
η = μ*p0/μ0
α = 18
Trange = np.arange(0.1, 1.005, 0.005)


#Definicion de las funciones elípticas de Jacobi
def sn(x,m):
    return ellipj(x,m)[0]

def cn(x,m):
    return ellipj(x,m)[1]

#Definicion de la ecuación trascendente 
def EqnTrasc(Fd, ω):
    ζf = ω*d/c

    if (α == 0.0):
        F0 = Fd*((η/p)**2 + (1.-(η/p)**2)*np.cos(p*ζf)**2)

    else:
        det = ((2.*p**2 /(α*μ)) + Fd)**2 + (8.*η**2*Fd/(α*μ))
        F1 = -0.5*(np.sqrt(det) + (2*p**2/(α*μ)) + Fd)
        F2 = 0.5*(np.sqrt(det) - (2*p**2/(α*μ)) - Fd)

        if (α > 0):
            κf = np.sqrt(0.5*α*μ*(Fd-F1))
            mf = (Fd-F2)/(Fd - F1)
            F0 = F2 + (Fd-F2)*cn(κf*ζf, mf)**2

        else:
            σ = (Fd - F1)/(F2 - Fd)
            κd1 = np.sqrt(0.5*abs(α)*μ*(F2-F1))
            md1 = (Fd-F1)/(F2-F1)
            F0 = (F1 + F2*σ*cn(κd1*ζf, md1)**2)/(1+σ*cn(κd1*ζf, md1)**2)

    return 4*η**2 - Fd*(3*η**2 + p**2 +0.5*α*μ*Fd) + F0*(p**2 - η**2 + 0.5*α*μ*F0)

#Definición de la función de bisección, la cual se asigna a cada nucleo
def fun(yi,yf,h,que):
    A = []
    for i in Trange:
        a = yi
        while(a <= yf):
            b = a + h
            fa = EqnTrasc(i,a)
            fb = EqnTrasc(i,b)
            if(fa*fb < 0):
                root = bisect(lambda x: EqnTrasc(i,x), a, b)
                A.append([i, root])
                a = b 
            else:
                a = b
    que.put(A)


#Función principal que asigna las tareas a cada nucleo
if __name__ == "__main__":

    tic = time.time()

#Definicion de las colas de cada proceso
    queue1 = Queue()
    queue2 = Queue()
    queue3 = Queue()
    queue4 = Queue()

# Asignacion de los procesos
    process1 = Process(target = fun, args=(1, 80, 0.1, queue1))  
    process2 = Process(target = fun, args=(80.1, 160, 0.1, queue2))
    process3 = Process(target = fun, args=(160.1, 240, 0.1, queue3))
    process4 = Process(target = fun, args=(240.1, 301.1, 0.1, queue4))  
  
#Los procesos inician
    process1.start()  
    process2.start() 
    process3.start()
    process4.start()

#Los procesos terminan
    process1.join()  
    process2.join()  
    process3.join()
    process4.join() 

#Se lee la cola de cada uno de los procesos
    result1 = queue1.get()
    result2 = queue2.get()
    result3 = queue3.get()
    result4 = queue4.get()

    print("Ambos procesos terminaron")
    toc = time.time()
    print(toc-tic)

#Se escriben los resultados en el archivo f
    f = open('omvalues_%d_parallel.dat'%α, 'w')

    for i in range(0, np.shape(result1)[0]):
        f.write("%.4f\t%.4f\n"%(result1[i][0],result1[i][1]))

    for i in range(0, np.shape(result2)[0]):
        f.write("%.4f\t%.4f\n"%(result2[i][0],result2[i][1]))

    for i in range(0, np.shape(result3)[0]):
        f.write("%.4f\t%.4f\n"%(result3[i][0],result3[i][1]))

    for i in range(0, np.shape(result4)[0]):
        f.write("%.4f\t%.4f\n"%(result4[i][0],result4[i][1]))

    f.close()