import time

import numpy
import math
import matplotlib.pyplot as plt
import scipy.special
from scipy.special import sph_harm


def hydrogen_wf(n,l,m,X,Y,Z):
    # R = radial coordinate
    R = numpy.sqrt(X**2+Y**2+Z**2)
    # angle theta between Z axis and R radial coordinate
    Theta = numpy.arccos(Z/R)
    # angle phi between Z axis and R coordinate
    Phi = numpy.arctan2(Y,X)
    
    
    rho = 2.*R/n
    # sph_harm = spherical harmonic oscilator
    s_harm=sph_harm(m, l, Phi, Theta)
    
    l_poly = scipy.special.genlaguerre(n-l-1,2*l+1)(rho)
    
    prefactor = numpy.sqrt((2./n)**3*math.factorial(n-l-1)/(2.*n*math.factorial(n+l)))
    wf = prefactor*numpy.exp(-rho/2.)*rho**l*s_harm*l_poly
    wf = numpy.nan_to_num(wf)
    return wf

def get_sample():
    # steps in space
    dz=0.1
    zmin=-5
    zmax=5
    x = numpy.arange(zmin,zmax,dz)
    y = numpy.arange(zmin,zmax,dz)
    z = numpy.arange(zmin,zmax,dz)

    #X, Y, Z are 3d arrays that tell us the values of x, y, z at every point in space
    X,Y,Z = numpy.meshgrid(x,y,z)

    print('x coordinate',x)
    print('y coordinate',y)
    print('z coordinate',z)

    print('X coordinate',X)
    print('Y coordinate',Y)
    print('Z coordinate',Z)


    #n : principal quantum number (main quantum number)
    # l : angular momentum quantum number (momentum quantum nubmer)
    # m : angular momentum projection quantum number (magnetic quantum nubmer)

    # can vary by atom type
    # for s1 orbital n=1 l=0 m=0 (hydrogen atom)
    # for s1 orbital n=2 l=1 m=0 (hydrogen atom)



    n=1
    l=0
    m=0
    #hydrogen wavefunction coordinates and quantum numbers
    data = hydrogen_wf(n,l,m,X,Y,Z)
    data = abs(data)**2

    R = numpy.sqrt(X**2+Y**2+Z**2)

    sample = data[int(len(z)/2),int(len(z)/2),:]
    sample.tolist()

    return list(sample)