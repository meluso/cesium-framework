# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-10
@name: model_agent.py

-------------------------------------------------------------------------------
Description:
    
This file contains a model of an agent in a system. It contains the definition
of the class agent including its properties. Those properties include a
selection of an objective function, definition of a current estimate, and the
position of the agent in the system network. The location and neighbor options
are required while the others are optional. Additional objective functions may 
be added to the code following the format of the existing functions.
Parameters:
    
    loc = [0,1,...,n-2,n-1]
        An integer value from 0 to n-1 which specifies the location of the
        agent in the network of nodes. This and all other agents refer to the
        agent by this integer when referencing locations in the system.
    nbr = vect{[0,1,...,n-2,n-1]}
        A vector of integer values from 0 to n-1 which specifies the nodes in
        the network (by integer) which are neighbors of this agent.
    obj = (string)
        A string input which specifies the objective function the agent uses
        to evaluate the quality of a design. The input must be one of the
        following terms, specified with quotes:
            "ackley"          - uses the Ackley function as the objective,
                                which is also the default setting
            "griewank"        - uses the Griewank function as objective
            "langermann"      - uses the Langermann function as objective
            "levy"            - uses the Levy function as objective
            "rosenbrock"      - uses the Rosenbrock function as the objective
            "schwefel         - uses the Schwefel function as objective
            "sphere"          - uses the sphere function as the objective
            "styblinski-tang" - uses the Styblinski-Tang function as objective
    tmp = (0.01, 50000]
        A number which determines the initial temperature of the dual annealing
        algorithm. The domain options are set by the algorithm. If the max
        temperature isn't sufficient to cause the algorithm to move positions,
        try reducing the scale of the objective function such that the max
        value of the objective is no greater than the max temp value.
    crt = (0,3]
        The cooling rate of the algorithm, which sets how quickly the
        probability distribution of sampling further-off points contracts.
        The domain options are set by the algorithm.
    itr = [1,2,...,inf)
        The number of iterations that the annealing algorithm will run per
        execution. The default value is 1 to increase the difficulty of
        converging, but the value may be increased by integer values.
        
                               
-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2018-10-10  jmeluso    Initial version started.
2018-10-21  jmeluso    Initial version completed. Updates ongoing to tune the
                       model to perform in a way which produces meaningful
                       results.
2019-03-28  rojanov    Updated code for python3. 
2019-05-24  rojanov    Updated objective function for basin-hopping...removed 
                       brent scalar minimization function.
2019-06-19  jmeluso    Removed historical estimate code.
2019-07-08  jmeluso    Added div and itr parameters for monte carlo testing.
2019-10-24  jmeluso    Added the Griewank, Langermann, Levy, and Schwefel
                       functions as objectives.
2019-10-28  jmeluso    Replaced the stepsize parameter (limiting the max step
                       size) with the temperature parameter (setting the
                       cooling rate), setting the stepsize as constant to half
                       the total domain of the design space.
2019-10-30  jmeluso    Replace basin-hopping algorithm with dual annealing
                       from scipy with only the general simulated annealing
                       turned on to replicate the original simulated annealing
                       concept.
2019-11-04  jmeluso    Differentiated between simulated annealing cooling rate
                       (visit parameter) and initial temperature.
                       
-------------------------------------------------------------------------------
"""

# Import python packages
import numpy as np
from numpy import exp, sin, cos, pi, sqrt, dot
import scipy.optimize as opt


class Agent(object):
    '''Defines a class agent which designs an artifact in a system.'''


    def __init__(self, loc, nbr, obj="ackley", tmp=10, crt=2.62, itr=1):

        '''Initializes an agent with all of its properties.'''

        ##### Network Properties #####
        
        self.location = loc  # Define the agent index in the system
        self.neighbors = nbr  # Define a vector of the agent's neighbors

        ##### Objective Properties #####

        self.fn = obj  # Specify the evaluating objective function
        
        
        # Create the agent's objective
        self.objective = Objective(self.fn,self.neighbors)

        # Set decision variable boundaries
        if self.fn == "ackley":
            self.obj_bounds = Bounds(-32.768,32.768)
        elif self.fn == "griewank":
            self.obj_bounds = Bounds(-600.00,600.00)
        elif self.fn == "langermann":
            self.obj_bounds = Bounds(0.00,10.00)
        elif self.fn == "levy":
            self.obj_bounds = Bounds(-10.00,10.00)
        elif self.fn == "rosenbrock":
            self.obj_bounds = Bounds(-5.00,10.00)
        elif self.fn == "schwefel":
            self.obj_bounds = Bounds(-500.00,500.00)
        elif self.fn == "sphere":
            self.obj_bounds = Bounds(-5.12,5.12)
        elif self.fn == "styblinski-tang":
            self.obj_bounds = Bounds(-5.00,5.00)
        else:
            print("Input for 'obj' is not valid.")
        
        ##### Optimization Properties #####

        self.tmp = tmp  # Initial temperature for the annealing algorithm
        self.cooling = crt  # Cooling rate for the annealing algorithm
        self.iterations = itr  # Number of iterations for the optimization
        
        ##### Estimate Properties #####
        
        self.curr_est = Obj_Eval()  # Initialize the agent's current estimate


    def __repr__(self):
        '''Returns a representation of the agent'''
        return self.__class__.__name__
        
        
    def initialize_estimates(self):
        '''Generates a random value for the initial current estimate.'''
        
        # Initialize the agent's current estimate by randomly generating an
        # a value on the domain of the objective function inputs
        # (-bound,+bound)
        self.curr_est.x = ((self.obj_bounds.xmax - self.obj_bounds.xmin)* \
                           np.random.random_sample() + self.obj_bounds.xmin)
        
        
    def initialize_evaluations(self,sys_vect):
        '''Generates an initial estiamte which the agent feeds back to the
        system. Then, the system feeds the system vector back to the agents
        to populate the objective evaluations.'''
        
        # Get own value for initial evaluation
        xi = self.curr_est.x
        
        # Initialize a vector of neighbors' values
        xj = [sys_vect[j] for j in self.neighbors]
        
        # Calculate the current estimate's objective evaluation
        self.curr_est.fx = self.objective(xi, xj)


    def get_estimate(self):
        '''Returns the appropriate estimate according to the type of estimate
        the agent is designated to return.'''
        
        # Return an estimate ("current") 
        return self.curr_est  # Return current value to system
    
    def generate_estimate(self,sys_vect):
        '''Uses a system vector input and the current agent estimate to
        generate one estimate value for the agent. The agent then compiles the
        generated decision variable value and objective evaluation. Finally,
        the agent uses its estimate type to determine which value (the current
        or future) of the estimate to return.''' ### Should always return current
        
        xi = self.curr_est.x
        
        # Initialize a vector of neighbors' values
        xj = [sys_vect[j].x for j in self.neighbors]

        # Create a new estimate by optimizing with inputs and own values
        estimate = self.optimize(xi,xj)

        # Save results
        self.curr_est.x = estimate.x
        self.curr_est.fx = estimate.fx
        
        # Return the estimate
        return self.get_estimate()


    def optimize(self,xi,xj):
        '''Optimizes the agent's design using the objective function and inputs
        from neighbor agents. The function takes in the agent's own value (xi)
        and the neighbors vector (xj). Uses the basinhopping algorithm to
        optimize the objective function.'''
        
        # Define arguments for optimization
        bound_lower = np.array([self.obj_bounds.xmin])
        bound_upper = np.array([self.obj_bounds.xmax])
        
        # Define local search option dictionary
        loc_search = {"method": "L-BFGS-B"}

        # Call the basin hopping minimization method
        output = opt.dual_annealing(func = self.objective,
                         bounds = list(zip(bound_lower,bound_upper)),
                         x0 = [xi],
                         args = tuple([xj]),
                         maxiter = self.iterations,
                         local_search_options = loc_search,
                         initial_temp = self.tmp,
                         # restart_temp_ratio = default,
                         visit = self.cooling,
                         # accept = default,
                         # maxfun = default,
                         # seed = default,
                         no_local_search = True,
                         # callback = default,
                         )
        
        # Save the desired outputs in float format
        if isinstance(output.fun,np.ndarray):
            result = Obj_Eval(output.x[0],output.fun[0])
        else:
            result = Obj_Eval(output.x[0],output.fun)
        
        # Return the result
        return result


class Objective:
    '''Based on the agent's own input (xi), a selected function (fn), and
    the inputs of the other agents (a vector, xj, of length k), this callable
    class calculates the specified objective function evaluation and returns
    the solution. '''
    
    def __init__(self,fn,neighbors):
        '''Initializes the objective function with the specified input function
        given by (fn) and calculates its degree (k) from its neighbors.'''
        
        self.fn = fn  # The selected objective function
        self.k = len(neighbors)  # The agent's degree
        

    def __call__(self,xi,xj):
        '''Executes the specified objective function with the inputs (xi) for
        the current agent and (xj) for the adjacent agents.'''        

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
            root_term = -a*exp(-b*sqrt((xi**2 + dot(xj,xj))/(self.k + 1)))
            cos_term = -exp((cos(c*xi) + cos_sum)/(self.k + 1))

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
            
        else: #self.fn == "styblinski-tang"
            
            # Build the sums for function evaluation
            xi_term = xi**4 - 16*xi**2 + 5*xi
            xj_term = 0
            for j in xj:
                xj_term = xj_term + j**4 - 16*j**2 + 5*j
                
            # Return the outcome
            result = 0.5*(xi_term + xj_term) + 39.166166*(self.k + 1)

        # Return the outcome
        return result


class Obj_Eval(object):
    '''Defines a class Obj_Eval for function evaluation which has two values,
    an input x and an output f(x) which represent one of several types of
    objective evaluations.'''
    
    def __init__(self,x=[],fx=[]):
        '''Initializes an instance of a function evaluation with all of its
        properties.'''
        
        self.x = x  # Initialize the input value of the function
        self.fx = fx  # Initialize the output value of the function


    def __repr__(self):
        '''Returns a representation of the function evaluation.'''
        return self.__class__.__name__
    
    
    def get_eval(self):
        '''Gets the values stored in the function eval class.'''
        
        return [self.x,self.fx]  # Return the objective evaluation pair

        
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