"""
Este codigo calcula las soluciones a la ecuación trascendente
para el coeficiente de transmisión como función del parametro a|E_i|**2.
Esta ecuacion resulta de las condiciones de frontera en la capa no lineal
Aqui se utiliza 1 núcleo del procesador y los resultados se escriben
en un archivo  alvalues_n_nonparallel.dat
"""


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
n = 14 #orden del cero en el caso lineal
λ = 2.*d*p/n #longitud de onda incidente 
f = c/λ #frecuencia de la onda incidente
ω = 2.0*np.pi*f #frecuencia angular
η = μ*p0/μ0
ζf = ω*d/c
αlim = (η**2 - p**2)/μ
Trange = np.arange(0.1, 1.003, 0.001)

#Definicion de las funciones elípticas de Jacobi
def sn(x,m):
    return ellipj(x,m)[0]

def cn(x,m):
    return ellipj(x,m)[1]

#Definicion de la ecuación trascendente 
def EqnTrasc(Fd, α):

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

#Definicion de la funcion de biseccion
def fun(yi,yf,h):
    A = []
    for i in Trange:
        a = yi
        while(a <= yf):
            b = a + h
            fa = EqnTrasc(i,a)
            fb = EqnTrasc(i,b)
            if(fa*fb < 0):
                root = bisect(lambda x: EqnTrasc(i,x), a, b)
                A.append([root, i])
                a = b 
            else:
                a = b
    return A

tic = time.time()
# Llamado a la función de bisección
Result = fun(αlim,15,0.01)
toc = time.time()

#Escritura de los datos en el archivo f
f = open('alvalues_%d_nonparallel.dat'%n, "w")
for i in range(0, np.shape(Result)[0]):
    f.write("%.4f\t%.4f\n"%(Result[i][0],Result[i][1]))
f.close()

print(toc-tic)