import pandas as pd
import sympy as sp
import numpy as np
import os as os
import matplotlib.pyplot as plt
from math import *
from scipy import integrate 
import scipy.integrate as spi 

pd.set_option("display.precision", 10)

# Funcion para crear una tabla
def create_dictionary(columns):
    dictionary = {}
    for c in columns:
        dictionary[c]  = []
    return dictionary

# Funcion para añadir datos en una columna
def add_info(dictionary, columns, data):
    i = 0
    for c in columns:
        dictionary[c].append(data[i])
        i+=1

def legendre_pol(xi, nodes):
    p0 = 1.0
    p1 = xi
    for n in range(1,nodes):
        p = ((2.0*n+1.0)*xi*p1 - n*p0) / (1.0 + n)
        p0 = p1
        p1 = p
        dp = nodes*(p0 - xi*p1) / (1.0 - xi**2)
    return p,dp

# Gauss nodes retorna los pesos a usar
# m son el numero de datos
# tol es la tolerancia de error.
def gauss_nodes(m,tol=10e-9):
    A = np.zeros(m)
    x = np.zeros(m)
    nRoots = int((m + 1)/2) # Numero de raices no negativas
    for i in range(nRoots):
        t = cos(pi*(i + 0.75)/(m + 0.5)) # Valor de x aproximado
        for j in range(30):
            p,dp = legendre_pol(t,m) # Mejorando el valor de x (raiz de legendre), usando los polinomios para 
            dt = -p/dp; t = t + dt # mejorar la precision con Newton Raphson
            if abs(dt) < tol:
                x[i] = t; x[m-i-1] = -t
                A[i] = 2.0/(1.0 - t**2)/(dp**2) # Ecuacion de los pesos
                A[m-i-1] = A[i]
                break
    return x,A # Valores de los pesos y las raices de legendre

# La funcion f debe ser simbolica
# La funcion gaussQuad integra integrales simples
# El argumento f es la funcion simbolica, el argumento "a" representa el limite inferior, el argumento "b" el limite superior
# El argumento m representa el numero de nodos a usar y por ultimo el argumento symb, es la variable (simbolo) por el cual
# realizaremos la integracion numerica.
# Retorn como primer valor el valor de la aproximacion y en segundo valor la tabla de pesos
def gaussQuad(f,a,b,nodes, symb, tol=10e-9):
    # Lambdify hace una funcion f segun una variable symb una
    # funcion lambda de python para ser utilizada.
    func = sp.lambdify(symb,f, modules=["sympy"])
    c1 = (b + a)/2.0
    c2 = (b - a)/2.0
    x,A = gauss_nodes(nodes+1)
    sum = 0.0
    cols = ["Raices", "Pesos"]
    table = create_dictionary(cols)
    
    for i in range(len(x)):
        sum = sum + A[i]*func(c1 + c2*x[i])
        add_info(table, cols, [x[i],A[i]])
    return c2*sum, table


# quadIntegrate es una funcion que integra desde integrales simples a cualquier numero de integrales (pueden ser dobles o triples)
# El argumento variables es un arrglo que contiene las variables por las cuales se integrara(simbolos), en el orden de integracion
# deseado, limits es un arreglo que con tiene arreglos con un par de valores, que son el limite inferior y superior respecto
# al orden de 
# tol almacena la tolerancia permitida del error de decimales
def quadIntegrate(variables, limits, function, nodes, tol=10e-9):
    i = 0
    nodes-=1
    auxFunc = function
    for symb in variables:
        auxFunc, table = gaussQuad(auxFunc, limits[i][0], limits[i][1], nodes, symb, tol)
        i+=1
    return auxFunc, table