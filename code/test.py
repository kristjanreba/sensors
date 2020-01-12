'''
R -> radius of a circle arround the sensor.
Sensor can only gather data from that radius.
r -> max distance for 2 sensors to communicate

Goal:
1. minimize r and R
2. sensor network (graph) must be connected (Vietoris-Rips graph is a full graph)
3. sensor network must cover the whole sphere (Cech complex is homotopy equivalent to a sphere)
'''

import math
import random
import numpy as np
import gudhi

import rips
import cech as ch
from plotting import plot_points, plot_circles


def sample_spherical(npoints, ndim=3):
    '''
    function returns points randomly distributed on a sphere
    '''
    vec = np.random.randn(ndim, npoints)
    vec /= np.linalg.norm(vec, axis=0)
    vec = np.transpose(vec)
    vec = vec.tolist()
    return vec


def fibonacci_sphere(npoints=1):
    '''
    function returns points nearly optimally distributed on a sphere
    '''
    rnd = random.random() * npoints
    points = []
    offset = 2./npoints
    increment = math.pi * (3. - math.sqrt(5.))
    for i in range(npoints):
        y = ((i * offset) - 1) + (offset / 2)
        r = math.sqrt(1 - pow(y,2))
        phi = ((i + rnd) % npoints) * increment
        x = math.cos(phi) * r
        z = math.sin(phi) * r
        points.append([x,y,z])
    return points


def get_Euler_characteristic(K):
    '''
    K -> simplicial complex (dictionary of lists of simplices)
    returns Euler characteristic of K
    '''
    euler_c = 0
    for key, value in K.items():
        if key % 2 == 0: euler_c += len(value)
        else: euler_c -= len(value)
    return euler_c


def minimize(X):
    '''
    X -> list of points
    returns minimum R and r and obsolete points
    '''
    eps = 0.01
    R = 0.1
    r = 0.4 # keep at least 0.4 otherwise we get segmentation fault in gudhi library

    while True:
        print('R = {0:.4f} r = {1:.4f}'.format(R, r))
        rips_complex = gudhi.RipsComplex(points=X, max_edge_length=r)
        simplex_tree = rips_complex.create_simplex_tree(max_dimension=1)
        simplex_tree.persistence()
        betti_nums = simplex_tree.betti_numbers()
        #print('Betti numbers: ', betti_nums)
        
        if betti_nums[0] == 1:
            #generate Cech complex
            #check if  Cech complex is homotopy equivalent to a sphere
            #we can check Euler characteristic of Cech complex and compare it to 2
            cech_complex = ch.cech(X, R)
            if get_Euler_characteristic(cech_complex) == 2:
                # we have a valid sensor configuration
                # current R and r are good enough
                break
            else:
                # the sensor configuration does not cover the whole sphere (increase sensor range R)
                R += eps
        else:
            # not all sensors are connected (increase connecting radious r)
            r += eps
            R = r / 2
        
    obs = getObsoleteSensors(X, R, r)
    return R, r, obs


def getObsoleteSensors(X, R, r):
    '''
    returns all the obsolete sensors for given X, R and r
    '''
    Xc = [x[:] for x in X]
    cech_complex = ch.cech(Xc, R)
    obs = []
    i = 0
    while i < len(Xc):
        removed_point = Xc.pop(i)
        # generate cech complex without removed point
        cech_complex = ch.cech(Xc, R)
        if get_Euler_characteristic(cech_complex) == 2:
            obs.append(removed_point)
        else:
            Xc.insert(0, removed_point)
            i += 1
    return obs


def generate(npoints=50):
    '''
    generate a set of 50 points with
    parameters r and R as small as possible
    '''
    X = fibonacci_sphere(npoints)
    R, r, obs = minimize(X)
    return X, R, r, obs


if __name__ == '__main__':

    print('Experiment 1')
    X = [[0.0740328,-0.0669765,-0.995004],[-0.0424728,-0.0903481,-0.995004],[0.49942,-0.26344,-0.825336],[0.520044,0.219943,-0.825336],[0.158841,0.54184,-0.825336],[-0.318986,0.465907,-0.825336],[-0.562607,0.0478954,-0.825336],[-0.393151,-0.405282,-0.825336],[0.0649644,-0.560893,-0.825336],[0.475382,-0.304685,-0.825336],[0.866629,-0.207856,-0.453596],[0.844371,0.28511,-0.453596],[0.563236,0.690663,-0.453596],[0.109417,0.884465,-0.453596],[-0.377948,0.807097,-0.453596],[-0.749438,0.482279,-0.453596],[-0.891156,0.00959889,-0.453596],[-0.759652,-0.466025,-0.453596],[-0.395246,-0.798769,-0.453596],[0.0903402,-0.886617,-0.453596],[0.548228,-0.702635,-0.453596],[0.838034,-0.303231,-0.453596],[0.999467,0.0145951,0.0291995],[0.870013,0.492164,0.0291995],[0.527371,0.849133,0.0291995],[0.0555024,0.998031,0.0291995],[-0.429966,0.902373,0.0291995],[-0.810076,0.585597,0.0291995],[-0.991686,0.125327,0.0291995],[-0.930293,-0.365653,0.0291995],[-0.640942,-0.767034,0.0291995],[-0.194535,-0.980461,0.0291995],[0.299541,-0.953636,0.0291995],[0.720218,-0.693133,0.0291995],[0.964412,-0.262785,0.0291995],[0.833167,0.225751,0.504846],[0.57369,0.644988,0.504846],[0.127056,0.853807,0.504846],[-0.361029,0.784085,0.504846],[-0.731333,0.458566,0.504846],[-0.863051,-0.0165536,0.504846],[-0.713211,-0.486272,0.504846],[-0.330696,-0.797352,0.504846],[0.159703,-0.848307,0.504846],[0.598002,-0.622515,0.504846],[0.841211,-0.193636,0.504846],[0.448738,0.253724,0.856889],[0.0444146,0.513584,0.856889],[-0.398518,0.326994,0.856889],[-0.495025,-0.143847,0.856889],[-0.161214,-0.489644,0.856889],[0.312737,-0.409801,0.856889],[0.514831,0.0262759,0.856889],[0.030007,0.0287842,0.999135]]
    plot_points(X)
    R, r, obs = minimize(X)
    print('R = {0:.4f}\nr = {1:.4f}'.format(R, r))
    plot_circles(X, R)
    
    print('Experiment 2')
    X = sample_spherical(50, ndim=3)
    R, r, obs = minimize(X)
    print('R = {0:.4f}\nr = {1:.4f}'.format(R, r))
    plot_circles(X, R)

    print('Experiment 3')
    X, R, r, obs = generate(50)
    print('R = {0:.4f}\nr = {1:.4f}'.format(R, r))
    plot_circles(X, R)

    
    
