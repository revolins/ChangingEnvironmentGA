import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import mlab
from mpl_toolkits.mplot3d import Axes3D
from fitness_function import *
import numpy as np

def main():
    base = "./ff_plots"
    landscape = schafferF7
    correlation = 0.99
    directory = "/" + landscape.__name__ + "_" + str(correlation) + ".png"
    ff = Fitness_Function(landscape, 2)
    ff.create_fitness2(correlation)
    #ff.set_flipped(True)
    #print fitness2([1,1])
    #plotFitnessFunction(ff.get_fitness1())
    plotFitnessFunction(ff, directory)

def plotFitnessFunction(ff, directory):
    plt.clf()
    function = ff.get_fitness2()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #interval = float(512+512)
    interval=10
    upper = 511
    lower = -512
    Y = range(lower, upper, interval)
    X = range(lower, upper, interval)
    X, Y = np.meshgrid(X, Y)
    Z = []
    for i in range(len(X)):
        Z.append([])
        for j in range(len(X[i])):
            Z[i].append(function(np.asarray([float(X[i][j]),float(Y[i][j])])))
    #print X, Y, Z
    #grid = mlab.griddate(X, Y, Z, X, Y)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)
    #surf = ax.plot_trisurf(X, Y, Z, cmap=cm.jet)
    #ax.plot_wireframe(X, Y, Z)
    plt.title("Correlation = " + str(ff.correlation()))
    plt.savefig(base + directory)

if __name__ == "__main__":
    main()

