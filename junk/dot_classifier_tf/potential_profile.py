# Module to create potential profiles
import numpy as np

def gauss(x,mean,sigma,peak):
    return peak*np.exp(-(x-mean)**2/(2*sigma**2))

def wire_profile(x,(peak,mean,h,rho)):
    '''
    V(x-mean) = peak * log(sqrt(h^2 + x^2)/rho)
    '''
    return peak*np.log((1.0/(rho))*np.sqrt((x-mean)**2 + h**2))

def single_dot_V_x_gauss(x,d,b1,b2):
    '''
    Input:
    x : 1d linear grid
    d : dot potential paramters
    b1,b2 : barrier parameters:
    
    Output:
    V(x) : potential landscape 
    
    The dot potential is modelled as a parabolic well with depth V_d and 
    size dot_size. The two barriers are modelled as Gaussaians. The 
    parameters are passed as the following tuples.
    
     d = (dot_size,V_d)
    b1 = (V_b1,mu_b1,sigma_b1)
    b2 = (V_b2,mu_b2,sigma_b2)
    
    Note: It is responsiblity of the caller to ensure that the dot_size is
    within the range of x.
    '''
    
    (dot_size,V_d) = d
    (V_b1,mu_b1,sigma_b1) = b1
    (V_b2,mu_b2,sigma_b2) = b2
    
    V = np.zeros(len(x))

    # dot potential
    k = 2*np.abs(V_d)/(dot_size**2)
    # outside the dot, the parabolic potential should be zero, faster 
    # way to ensure that rather than iterating with an if condition
    x_dot = np.array(map(lambda x:x if np.abs(x) < dot_size else dot_size,x))
    V += 0.5*k*x_dot**2 + V_d
    
    # barriers
    V += gauss(x,mu_b1,sigma_b1,V_b1)
    V += gauss(x,mu_b2,sigma_b2,V_b2)
    
    return V

def single_dot_V_x_wire(x,d,b1,b2):
    '''
    Input:
    x : 1d linear grid
    d : dot potential paramters
    b1,b2 : barrier parameters:
    
    Output:
    V(x) : potential landscape 
   
    The dot potential is modelled as a potential form cylindrical metal gates. V ~ ln(r) potential.
    
     d = (V_d,mu_d,h_dot,rho_dot)
    b1 = (V_b1,mu_b1,h_1,hro_1)
    b2 = (V_b2,mu_b2,h_2,rho_2)
   
    Note: It is responsiblity of the caller to ensure that the dot_size is
    within the range of x.
    '''
    V = np.zeros(len(x))

    # dot potential
    V += wire_profile(x,d) 
    # barriers
    V += wire_profile(x,b1)
    V += wire_profile(x,b2)
    
    return V

def V_x_wire(x,list_b):
    '''
    Input:
    x : 1d linear grid
    list_b : list of gate parameters as (V,mu,h,rho) where V(x) = V*ln(sqrt(h^2 + x^2)/rho)
    
    Output:
    V(x) : potential profile
    '''
    
    V = np.zeros(len(x))
    for i in range(len(list_b)): 
        V += wire_profile(x,list_b[i])
        
    return V
