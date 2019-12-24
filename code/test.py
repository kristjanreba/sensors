'''
R -> radius of a circle arround the sensor.
Sensor can only gather data from that radius.
r -> max distance for 2 sensors to communicate

Goal:
1. minimize r and R
2. sensor network (graph) must be connected (Vietoris-Rips graph is a full graph)
3. sensor network must cover the whole sphere (Cech complex is homotopy equivalent to a sphere)


ToDo:
- implement function generate_Cech_complex(X)
- implement function get_Euler_characteristic(K)
- implement function minimize(X)
    - we need to search for near optimal R and r
    - right now we only search for optimal R and r where R = r
- implement function getObsoleteSensors(X, R, r)
- function generate should generate near optimal point distribution
- create nice visualization for generated points and spheres
'''


import numpy as np
import gudhi

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def plot_points(X):
    '''
    X -> list of 3d points
    '''
    X_np = np.array(X)
    print('X shape: ', X_np.shape)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X_np[:,0], X_np[:,1], X_np[:,2])
    plt.show()


def sample_spherical(npoints, ndim=3):
    '''
    function returns points randomly distributed on a sphere
    '''
    vec = np.random.randn(ndim, npoints)
    vec /= np.linalg.norm(vec, axis=0)
    vec = np.transpose(vec)
    return vec


def get_Euler_characteristic(K):
    '''
    K -> simplicial complex (list of simplices)
    returns Euler characteristic of K
    '''
    euler_c = 0
    return euler_c


def generate_Cech_complex(X):
    '''
    X -> list of points
    returns simplicial complex K
    '''
    K = []
    return K


def minimize(X):
    '''
    X -> list of points
    returns minimum R and r and obsolete points
    '''
    eps = 0.1
    R = 0.1
    r = 0.1

    while True:
        print('R =', R, 'r = ', r)
        rips_complex = gudhi.RipsComplex(points=X, max_edge_length=R)
        simplex_tree = rips_complex.create_simplex_tree(max_dimension=1)
        simplex_tree.persistence()
        betti_nums = simplex_tree.betti_numbers()
        print('Betti numbers: ', betti_nums)
        if betti_nums[0] == 1:
            break

            '''
            generate Cech complex
            check if  Cech complex is homotopy equivalent to a sphere
            we can check Euler characteristic of Cech complex and compare it to 2
            '''

            '''
            K = generate_Cech_complex(X)
            if get_Euler_characteristic(K) == 2:
                break
            '''
        else:
            R += eps
            r += eps
    
    obs = getObsoleteSensors(X, R, r)
    return R, r, obs


def getObsoleteSensors(X, R, r):
    '''
    returns all the obsolete sensors for given X, R and r
    '''
    obs = []

    return obs


def generate():
    '''
    generate a set of 50 points with
    parameters r and R as small as possible
    '''
    X = sample_spherical(50, ndim=3)
    R, r, obs = minimize(X)
    return X, R, r, obs


if __name__ == '__main__':
    X = [[0.0740328,-0.0669765,-0.995004],[-0.0424728,-0.0903481,-0.995004],[0.49942,-0.26344,-0.825336],[0.520044,0.219943,-0.825336],[0.158841,0.54184,-0.825336],[-0.318986,0.465907,-0.825336],[-0.562607,0.0478954,-0.825336],[-0.393151,-0.405282,-0.825336],[0.0649644,-0.560893,-0.825336],[0.475382,-0.304685,-0.825336],[0.866629,-0.207856,-0.453596],[0.844371,0.28511,-0.453596],[0.563236,0.690663,-0.453596],[0.109417,0.884465,-0.453596],[-0.377948,0.807097,-0.453596],[-0.749438,0.482279,-0.453596],[-0.891156,0.00959889,-0.453596],[-0.759652,-0.466025,-0.453596],[-0.395246,-0.798769,-0.453596],[0.0903402,-0.886617,-0.453596],[0.548228,-0.702635,-0.453596],[0.838034,-0.303231,-0.453596],[0.999467,0.0145951,0.0291995],[0.870013,0.492164,0.0291995],[0.527371,0.849133,0.0291995],[0.0555024,0.998031,0.0291995],[-0.429966,0.902373,0.0291995],[-0.810076,0.585597,0.0291995],[-0.991686,0.125327,0.0291995],[-0.930293,-0.365653,0.0291995],[-0.640942,-0.767034,0.0291995],[-0.194535,-0.980461,0.0291995],[0.299541,-0.953636,0.0291995],[0.720218,-0.693133,0.0291995],[0.964412,-0.262785,0.0291995],[0.833167,0.225751,0.504846],[0.57369,0.644988,0.504846],[0.127056,0.853807,0.504846],[-0.361029,0.784085,0.504846],[-0.731333,0.458566,0.504846],[-0.863051,-0.0165536,0.504846],[-0.713211,-0.486272,0.504846],[-0.330696,-0.797352,0.504846],[0.159703,-0.848307,0.504846],[0.598002,-0.622515,0.504846],[0.841211,-0.193636,0.504846],[0.448738,0.253724,0.856889],[0.0444146,0.513584,0.856889],[-0.398518,0.326994,0.856889],[-0.495025,-0.143847,0.856889],[-0.161214,-0.489644,0.856889],[0.312737,-0.409801,0.856889],[0.514831,0.0262759,0.856889],[0.030007,0.0287842,0.999135]]
    
    #plot_points(X)
    print(minimize(X))
    #print(generate())