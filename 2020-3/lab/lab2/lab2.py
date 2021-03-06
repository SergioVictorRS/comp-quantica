import qiskit
import numpy as np

from qiskit import execute, Aer, QuantumRegister, QuantumCircuit


def rzryrz(U):
    '''
    Lab2 - questão 1
    :param U: matriz unitária 2 x 2
    :return: [alpha, beta, gamma e delta]
            U = e^(1j * alpha) * Rz(beta) * Ry(gamma) * Rz(delta)
    '''

    # -----------------
    # Seu código aqui

    for m_delta in range(63): #aproximadamente 2pi*10
      for m_gamma in range(63):
        for m_beta in range(63):
          for m_alpha in range(63):
             print("alpha: ", m_alpha/10, "beta: ", m_beta/10, "gamma: ", m_gamma/10)
          
             alpha = m_alpha/10
             beta = m_beta/10
             gamma = m_gamma/10
             delta = m_delta/10
             
	     
             b00 = np.cos(gamma/2)*(np.exp(1j*(delta + alpha/2 + beta/2)))
             b10 = -1*np.sin(gamma/2)*(np.exp(1j*(delta - alpha/2 + beta/2)))
             b01 = np.sin(gamma/2)*(np.exp(1j*(delta + alpha/2 - beta/2)))
             b11 = np.cos(gamma/2)*(np.exp(1j*(delta - alpha/2 - beta/2)))
             
             print([[b00, b01],[b10, b11]])

             #gera matriz B e compara com a original U
             if(np.allclose(b00, U[0][0])):   #compara u00 com resultado de b00
                if(np.allclose(b10, U[1][0])):# compara u10 com resultado de b10
                  if(np.allclose(b01, U[0][1])):#compara u01 com resultado de b01
                    if(np.allclose(b11, U[1][1])):#compara u11 com resultado de b11
                      print("alpha: ", alpha, "beta: ", beta, "gamma: ", gamma, "delta: ", delta)
                      return [alpha, beta, gamma, delta]

def operador_controlado(V):
    '''
    Lab2 - questão 2
    :param V: matriz unitária 2 x 2
    :return: circuito quântico com dois qubits aplicando o
             o operador V controlado.
    '''

    circuito = qiskit.QuantumCircuit(2)
    
    #-----------------
    # Seu código aqui
    vetor = rzryrz(V)
    
    alpha = vetor[0]
    beta = vetor[1]
    gamma = vetor[2]
    delta = vetor[3]
    
    circuito.rz(beta, 1)
    circuito.ry(gamma/2, 1)
    circuito.cx(0, 1)
    circuito.ry((gamma/2)*(-1), 1)
    circuito.rz((-1)*(delta+beta)/2, 1)
    circuito.cx(0, 1)
    circuito.rz((delta-beta)/2, 1)

    # -----------------

    return circuito


def toffoli():
    '''
    Lab2 - questão 3
    :param n: número de controles
    :param V:
    :return: circuito quântico com n+1 qubits + n-1 qubits auxiliares
            que aplica o operador nCV.
    '''
    controles = qiskit.QuantumRegister(2)
    alvo = qiskit.QuantumRegister(1)
    
    #------------------------
    # Seu código aqui
    #utilizando os operados T, T-adjoint e CNOT
    circuito = qiskit.QuantumCircuit(controles, alvo)
    circuito.h(alvo)
    circuito.cx(controles[1], alvo)
    circuito.tdg(alvo) #conjugada de t
    circuito.cx(controles[0], alvo)
    circuito.t(alvo)
    circuito.cx(controles[1], alvo)
    circuito.tdg(alvo)
    circuito.cx(controles[0], alvo)
    circuito.t(controles[1])
    circuito.t(alvo)
    circuito.cx(controles[0], controles[1])
    circuito.h(alvo)
    circuito.t(controles[0])
    circuito.tdg(controles[1])
    circuito.cx(controles[0], controles[1])
    
    
    # ------------------------

    return circuito

def inicializa_3qubits(vetor_dimensao8):
    '''
    Lab2 - questão 4
    '''

    circuito = qiskit.QuantumCircuit(3) #3 qubits

    # ------------------------
    # Seu código aqui
    #usando o algoritmo da arvore
    a1 = vetor_dimensao8[0]
    a2 = vetor_dimensao8[1]
    a3 = vetor_dimensao8[2]
    a4 = vetor_dimensao8[3]
    a5 = vetor_dimensao8[4]
    a6 = vetor_dimensao8[5]
    a7 = vetor_dimensao8[6]
    a8 = vetor_dimensao8[7]
    
    b1 = np.sqrt(np.power(a1, 2)+np.power(a2, 2))
    b2 = np.sqrt(np.power(a3, 2)+np.power(a4, 2))
    b3 = np.sqrt(np.power(a5, 2)+np.power(a6, 2))
    b4 = np.sqrt(np.power(a7, 2)+np.power(a8, 2))
    
    c1 = np.sqrt(np.power(b1, 2)+np.power(b2, 2))
    c2 = np.sqrt(np.power(b3, 2)+np.power(b4, 2))
    
    d = np.sqrt(np.power(c1, 2)+np.power(c2, 2))
    
    alpha0 = 2*np.arcsin(c2/d)
    alpha1 = 2*np.arcsin(b2/c1)
    alpha2 = 2*np.arcsin(b4/c2)
    alpha3 = 2*np.arcsin(a2/b1)
    alpha4 = 2*np.arcsin(a4/b2)
    alpha5 = 2*np.arcsin(a6/b3)
    alpha6 = 2*np.arcsin(a8/b4)
    
    #implementacao do circuito dados alpha1..alpha6
    
    circuito.ry(alpha0, 0)
    circuito.x(0)
    circuito.cry(alpha1, 0, 1)
    circuito.x(0)
    circuito.cry(alpha2, 0, 1)
    circuito.x(0)
    circuito.x(1)
    circuito.cry(alpha3, 1, 2)
    circuito.x(1)
    circuito.cry(alpha4, 0, 1)
    circuito.x(0)
    circuito.x(1)
    circuito.cry(alpha5, 0, 1)
    circuito.x(1)
    circuito.cry(alpha6, 0, 1)
    
    
    # ------------------------

    return circuito

def inicializa(vetor):
    '''
    Lab2 - questão 5 - opcional
    '''
    circuito = qiskit.QuantumCircuit()

    return circuito
    


'''
QUESTAO 1
alpha = 0
beta = 0
gamma = 1
delta = 0

a = np.cos(gamma/2)*(np.exp(1j*(delta + alpha/2 + beta/2)))
c = -1*np.sin(gamma/2)*(np.exp(1j*(delta - alpha/2 + beta/2)))
b = np.sin(gamma/2)*(np.exp(1j*(delta + alpha/2 - beta/2)))
d = np.cos(gamma/2)*(np.exp(1j*(delta - alpha/2 - beta/2)))

rzryrz([[a,b],[c, d]])
'''
'''
#QUESTAO 2
circuito = operador_controlado([[1,0],[0,1]])
print(circuito)
'''

'''
QUESTAO 3
toffoli()
'''


#QUESTAO 4
circuito = inicializa_3qubits([1,1,1,1,1,1,1,1])
print(circuito)

