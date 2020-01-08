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
- test function get_Euler_characteristic(K)
- finish implementing function minimize(X)
- implement function getObsoleteSensors(X, R, r)
- create nice visualization for generated points and spheres
'''

import math
import random
import numpy as np
import gudhi

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import Circle, PathPatch
import matplotlib.pyplot as plt

from collections import Counter


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
    dims = [len(w) for w in K]
    dims = list(Counter(dims).values())
    for i in range(len(dims)):
        if i % 2 == 0: euler_c += dims[i]
        else: euler_c -= dims[i]
    return euler_c


def generate_Cech_complex(X, r):
    '''
    X -> list of points
    returns Cech simplicial complex K
    '''
    K = []
    return K


def minimize(X):
    '''
    X -> list of points
    returns minimum R and r and obsolete points
    '''
    eps = 0.01
    R = 0.4 # keep at least 0.4 otherwise we get segmentation fault in gudhi library
    r = 0.1

    while True:
        print('R =', R, 'r = ', r)
        rips_complex = gudhi.RipsComplex(points=X, max_edge_length=R)
        simplex_tree = rips_complex.create_simplex_tree(max_dimension=1)
        simplex_tree.persistence()
        betti_nums = simplex_tree.betti_numbers()
        print('Betti numbers: ', betti_nums)
        
        if betti_nums[0] == 1:
            #generate Cech complex
            #check if  Cech complex is homotopy equivalent to a sphere
            #we can check Euler characteristic of Cech complex and compare it to 2
            cech_complex = generate_Cech_complex(X, r)
            if get_Euler_characteristic(cech_complex) == 2:
                # we have a valid sensor configuration
                # current R and r are good enough
                break
            else:
                # the sensor configuration does not cover the whole sphere (increase sensor range r)
                r += eps
        else:
            # not all sensors are connected (increase connecting radious R)
            R += eps
        
    obs = getObsoleteSensors(X, R, r)
    return R, r, obs


def getObsoleteSensors(X, R, r):
    '''
    returns all the obsolete sensors for given X, R and r
    '''
    obs = []

    return obs


def generate(npoints=50):
    '''
    generate a set of 50 points with
    parameters r and R as small as possible
    '''
    X = fibonacci_sphere(npoints)
    R, r, obs = minimize(X)
    return X, R, r, obs


def fibonacci_sphere(npoints=1):
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


def plot_circles(X, r):
    X_np = np.array(X)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X_np[:,0], X_np[:,1], X_np[:,2], c='r')
    for point in X:
        x,y,z = point[0], point[1], point[2]
        p = Circle((0, 0), r, alpha=0.4)
        ax.add_patch(p)
        normal = [x,y,z]
        pathpatch_2d_to_3d(p, z=0, normal=normal)
        pathpatch_translate(p, point)
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    plt.show()


def rotation_matrix(v1,v2):
    """
    Calculates the rotation matrix that changes v1 into v2.
    """
    v1/=np.linalg.norm(v1)
    v2/=np.linalg.norm(v2)

    cos_angle=np.dot(v1,v2)
    d=np.cross(v1,v2)
    sin_angle=np.linalg.norm(d)

    if sin_angle == 0:
        M = np.identity(3) if cos_angle>0. else -np.identity(3)
    else:
        d/=sin_angle

        eye = np.eye(3)
        ddt = np.outer(d, d)
        skew = np.array([[    0,  d[2],  -d[1]],
                      [-d[2],     0,  d[0]],
                      [d[1], -d[0],    0]], dtype=np.float64)

        M = ddt + cos_angle * (eye - ddt) + sin_angle * skew

    return M


def pathpatch_2d_to_3d(pathpatch, z = 0, normal = 'z'):
    """
    Transforms a 2D Patch to a 3D patch using the given normal vector.

    The patch is projected into they XY plane, rotated about the origin
    and finally translated by z.
    """
    if type(normal) is str: #Translate strings to normal vectors
        index = "xyz".index(normal)
        normal = np.roll((1,0,0), index)

    path = pathpatch.get_path() #Get the path and the associated transform
    trans = pathpatch.get_patch_transform()

    path = trans.transform_path(path) #Apply the transform

    pathpatch.__class__ = art3d.PathPatch3D #Change the class
    pathpatch._code3d = path.codes #Copy the codes
    pathpatch._facecolor3d = pathpatch.get_facecolor #Get the face color    

    verts = path.vertices #Get the vertices in 2D

    M = rotation_matrix(normal,(0, 0, 1)) #Get the rotation matrix

    pathpatch._segment3d = np.array([np.dot(M, (x, y, 0)) + (0, 0, z) for x, y in verts])


def pathpatch_translate(pathpatch, delta):
    """
    Translates the 3D pathpatch by the amount delta.
    """
    pathpatch._segment3d += delta


if __name__ == '__main__':
    X = [[0.0740328,-0.0669765,-0.995004],[-0.0424728,-0.0903481,-0.995004],[0.49942,-0.26344,-0.825336],[0.520044,0.219943,-0.825336],[0.158841,0.54184,-0.825336],[-0.318986,0.465907,-0.825336],[-0.562607,0.0478954,-0.825336],[-0.393151,-0.405282,-0.825336],[0.0649644,-0.560893,-0.825336],[0.475382,-0.304685,-0.825336],[0.866629,-0.207856,-0.453596],[0.844371,0.28511,-0.453596],[0.563236,0.690663,-0.453596],[0.109417,0.884465,-0.453596],[-0.377948,0.807097,-0.453596],[-0.749438,0.482279,-0.453596],[-0.891156,0.00959889,-0.453596],[-0.759652,-0.466025,-0.453596],[-0.395246,-0.798769,-0.453596],[0.0903402,-0.886617,-0.453596],[0.548228,-0.702635,-0.453596],[0.838034,-0.303231,-0.453596],[0.999467,0.0145951,0.0291995],[0.870013,0.492164,0.0291995],[0.527371,0.849133,0.0291995],[0.0555024,0.998031,0.0291995],[-0.429966,0.902373,0.0291995],[-0.810076,0.585597,0.0291995],[-0.991686,0.125327,0.0291995],[-0.930293,-0.365653,0.0291995],[-0.640942,-0.767034,0.0291995],[-0.194535,-0.980461,0.0291995],[0.299541,-0.953636,0.0291995],[0.720218,-0.693133,0.0291995],[0.964412,-0.262785,0.0291995],[0.833167,0.225751,0.504846],[0.57369,0.644988,0.504846],[0.127056,0.853807,0.504846],[-0.361029,0.784085,0.504846],[-0.731333,0.458566,0.504846],[-0.863051,-0.0165536,0.504846],[-0.713211,-0.486272,0.504846],[-0.330696,-0.797352,0.504846],[0.159703,-0.848307,0.504846],[0.598002,-0.622515,0.504846],[0.841211,-0.193636,0.504846],[0.448738,0.253724,0.856889],[0.0444146,0.513584,0.856889],[-0.398518,0.326994,0.856889],[-0.495025,-0.143847,0.856889],[-0.161214,-0.489644,0.856889],[0.312737,-0.409801,0.856889],[0.514831,0.0262759,0.856889],[0.030007,0.0287842,0.999135]]
    #plot_points(X)
    
    #print(minimize(X))
    #print(generate())

    #X = fibonacci_sphere(npoints=50)
    #plot_points(X)

    #X = sample_spherical(50, ndim=3)
    #plot_points(X)

    X = fibonacci_sphere(npoints=50)
    plot_circles(X, 0.4)
    
    
