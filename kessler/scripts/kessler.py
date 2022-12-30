from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

X0 = [1000,10] # X[0]: numeber of sattelites, X[1] : number of debris
u = 16.65 # increment of satlites
k1 = 0.0001 # for decrement of satelites destroyed by debris
k2 = 0.0003 # for increment of debris created by satelites' destruction
k3 = 0.001 # for increment of debries create by crash between debries 
k4 = 0.001 # for increment of debries create by naturally destroyed satelites
na = 0.001 # for decrement of satelites destoryed naturally
nb = 0.9 # for decrement of debries destroyed naturally

def dX_dt(X,t):
    output1 = u - (k1*X[0]*X[1]) - na*X[0]
    #output2 = k2*X[0]*X[1] - nb*X[1] # simple model
    output2 = k2*X[0]*X[1] + k3 * X[1] * X[1] + k4*na*X[0] - nb*X[1]  # a model considering crash between debris
    return [output1, output2]

ts = np.linspace(start = 0, stop = 200, num = 10000)
Us = odeint(dX_dt,X0,ts)
ys1 = Us[:,0]
ys2 = Us[:,1]

print(Us[-1])
plt.plot(ts,ys1,"b", label = 'The number of satelites')
plt.plot(ts,ys2,"r", label = 'The number of debris')
plt.legend()
plt.xlabel("Time(year)")
plt.ylabel("The number of objects")
title = "Increment of stalites = "+ str(u)
plt.title(title)
plt.show()

"""
The steady state of X[0] can not over 3000, even though u increases dramatically. I think there exists the orbit capacity defined by space debris. 
The stable numeber of sattelites is n_b/k2. 
This equation is too simple. To make it more resonable, We should imply the stochastic model.
"""
