# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:13:50 2020

@author: John Meluso
"""

# Import python packages
import numpy as np
from numpy import exp, sin, cos, pi, sqrt, dot
import scipy.optimize as opt
import datetime as dt


class Objective(object):

    def __init__(self,fn):

        self.fn = fn


    def __call__(self,x,minmax):
        '''Executes the specified objective function with the inputs (xi) for
        the current agent and (xj) for the adjacent agents.'''

        k = len(x)-1
        xi = x[0]
        xj = x[1:]

        # Select the correct function to evaluate
        if self.fn == "ackley":

            # Set values of constants for ackley function
            a = 20
            b = 0.2
            c = 2*pi

            # Build the sums for function evaluation
            cos_sum = 0
            for j in xj:
                cos_sum = cos_sum + cos(c*j)

            # Evaluate the ackley function
            root_term = -a*exp(-b*sqrt((xi**2 + dot(xj,xj))/(k + 1)))
            cos_term = -exp((cos(c*xi) + cos_sum)/(k + 1))

            # Return the function evaluation
            result = root_term + cos_term + a + exp(1)

        elif self.fn == "griewank":

            # Build vector of all elements
            vect = xj
            vect.insert(0,xi)

            # Build the sum term
            sum_term = 1
            for v in vect:
                sum_term = sum_term + v**2/4000

            # Build the product term
            prod_term = 1
            for r in range(0,len(vect)):
                prod_term = prod_term*cos(vect[r]/sqrt(r+1))

            # Return the function evaluation
            result = sum_term - prod_term

        elif self.fn == "langermann":

            # Set values of constants for the langermann function
            a = [3, 5, 2, 1, 7]  # Location of the 5 minima
            c = [-1,-2,-5,-2,-3]  # Amplitudes of the 5 minima

            # Build vector of all elements
            vect = xj
            vect.insert(0,xi)

            # Initialize the sum of all elements
            result = 0  # For the full product of c, exp, and cos

            # Iterate through the len(c) minima
            for i in range(0,len(c)):

                sqr_sum = 0  # For the sum within the exponent

                # Iterate through the n dimensions of matrix A
                for j in range(0,len(vect)):

                    # Add element to square sum term
                    sqr_sum = sqr_sum + (vect[j]-a[i])**2

                # Combine into total sum
                result = result + c[i] \
                    * exp((-1/pi)*sqr_sum) * cos(pi*sqr_sum)

        elif self.fn == "levy":

            # Build vector of all elements
            vect = xj
            vect.insert(0,xi)

            # Initialize w(i) and the sum over all dimensions as result
            w = [(1 + (x-1)/4) for x in vect]
            result = (sin(pi*w[0]))**2 + \
                (w[-1]-1)**2*(1+(sin(2*pi*w[-1]))**2)

            # Iteratively add sum elements to initial and final sum terms
            for i in range(0,len(vect)-1):
                result = result + \
                    (w[i]-1)**2 * (1 + 10*(sin(pi*w[i]+1))**2)

        elif self.fn == "rosenbrock":

            # Build vector of all elements
            vect = xj
            vect.insert(0,xi)

            # Call scipy function for rosenbrock
            result = opt.rosen(vect)

        elif self.fn == "schwefel":

            # Build vector of all elements
            vect = xj
            vect.insert(0,xi)

            # Initialize minimum
            result = 418.9829*len(vect)

            # Iteratively add elements to minimum elements
            for x in vect:
                result = result + x*sin(sqrt(abs(x)))

            # Scale function down
            result = result/1000

        elif self.fn == "sphere":

            # Evaluate the sphere function
            result = xi**2 + dot(xj,xj)

        else: #fn == "styblinski-tang"

            # Build the sums for function evaluation
            xi_term = xi**4 - 16*xi**2 + 5*xi
            xj_term = 0
            for j in xj:
                xj_term = xj_term + j**4 - 16*j**2 + 5*j

            # Return the outcome
            result = 0.5*(xi_term + xj_term) + 39.16599*(k + 1)

        # Return the outcome
        return minmax*result


class Bounds(object):
    '''Defines a set of bounds, upper and lower, within which to evaluate an
    objective function.'''

    def __init__(self,xmin,xmax):
        '''Initializes the bounds class with min and max values.'''
        self.xmax = np.array(xmax)
        self.xmin = np.array(xmin)

    def __call__(self, **kwargs):
        '''Checks to see if a value falls within the specified bounds or not
        and returns either True or False accordingly.'''
        x = kwargs["x_new"]
        tmax = bool(np.all(x <= self.xmax))
        tmin = bool(np.all(x >= self.xmin))
        return tmin and tmax


def optimize(fn,x,x_lower,x_upper,minmax):
    '''Optimizes the agent's design using the objective function and inputs
    from neighbor agents. The function takes in the agent's own value (xi)
    and the neighbors vector (xj). Uses the basinhopping algorithm to
    optimize the objective function.'''

    # Call the optimization function
    output = opt.minimize(fun = fn,
                          x0 = x,
                          args = minmax,
                          bounds = list(zip(x_lower,x_upper))
                          )

    # Save the desired outputs in float format
    if isinstance(output.fun,np.ndarray):
        result = output.fun[0]
    else:
        result = output.fun

    # Return the result
    return result


if __name__ == '__main__':

    # Create array of number of variables
    nodes = np.array([2,3,4])
    num_nodes = len(nodes)
    ind_nodes = 0
    ind_min = 1
    ind_max = 2

    # Create functions
    functions = []
    new_fun = {'fn': "ackley",'bounds': Bounds(-32.768,32.768)}
    functions.append(new_fun)
    new_fun = {'fn': "griewank",'bounds': Bounds(-600.00,600.00)}
    functions.append(new_fun)
    new_fun = {'fn': "langermann",'bounds': Bounds(0.00,10.00)}
    functions.append(new_fun)
    new_fun = {'fn': "levy",'bounds': Bounds(-10.00,10.00)}
    functions.append(new_fun)
    new_fun = {'fn': "rosenbrock",'bounds': Bounds(-5.00,10.00)}
    functions.append(new_fun)
    new_fun = {'fn': "schwefel",'bounds': Bounds(-500.00,500.00)}
    functions.append(new_fun)
    new_fun = {'fn': "sphere",'bounds': Bounds(-5.12,5.12)}
    functions.append(new_fun)
    new_fun = {'fn': "styblinski-tang",'bounds': Bounds(-5.00,5.00)}
    functions.append(new_fun)

    # Start timer
    t_start = dt.datetime.now()

    # Iterate through each function to get the max and min
    for f in functions:
        f['extrema'] = np.empty((3,num_nodes))
        f['extrema'][ind_nodes,:] = nodes
        objective = Objective(f['fn'])
        bmin = f['bounds'].xmin
        bmax = f['bounds'].xmax
        for ii in np.arange(len(nodes)):
            n = nodes[ii]
            rand_start = (bmax-bmin)*np.random.random(n)-bmin
            lower = bmin*np.ones((n,1))
            upper = bmax*np.ones((n,1))
            f['extrema'][ind_min,ii] = optimize(
                objective,rand_start,lower,upper,1)
            f['extrema'][ind_max,ii] = -optimize(
                objective,rand_start,lower,upper,-1)
            print("(" + str(f['fn']) + "," + str(nodes[ii]) + ") - " + \
                  "min: " + str(f['extrema'][ind_min,ii]) + ", " + \
                  "max: " + str(f['extrema'][ind_max,ii]))

            # Stop timer
            t_stop = dt.datetime.now()
            print((t_stop - t_start))











