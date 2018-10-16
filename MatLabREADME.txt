This file contains instructions for how to use the enzyme kinetics model in the UNSW 2018 IGEM Team.

At the top of the Model.m file, vmax and km variables are declared for each enzyme. 
The values of these variables can be altered to suit a specific enzyme
Vmax2 and Km2 refer to the second enzyme in the reaction, and thus the sink.

The file is currently set up so that Vmax is the rate of production at enzyme 1, 
and the Michaelis-Menten equation in full controls the rate of consumption at enzyme 2.

This is set in the following lines in Model.m:

    applyBoundaryCondition(model, 'neumann', 'Edge', 2,'q',0.0, 'g', vmax);
    applyBoundaryCondition(model, 'neumann', 'Edge', 4,'q',0.0, 'g', myufunction);
    
myufunction refers to a non-linear boundary condition at the second enzyme, myufuncton is declared in the following line in Model.m:

    myufunction = @(region,state) -(vmax2*state.u)/(state.u+km2);
    
This is the michaelis-menten equation, calculated on the value of the solution U at the second enzyme
The solution U refers to the concentration of substrate. 

Notice that the code is wrapped in a loop:
    for i = 3.8:-0.1:0.2
The value of i is passed into a global variable 'c', which is then used to construct the geometry and mesh of the system.
The value c in the GEOMETRY PARAMETERS struct determines how far the enzymes are from the center.
    At a value of 0, the enzymes are on top of each other
    At a value of 1 the enzymes are 1 unit from the center (2 units apart)
    At a value of 3 the enzymes are 3 units from the center (6 units apart)
    
The effect of changing these values can be tested using the test_domain.m script.

To make the geometry area bigger and allow for a greater variety of distances to be tested, 
increase the value of a in the GEOMETRY PARAMETERS Struct in Model.m
Note that large values of a will slow the computation and may lead to errors as memory limits are reached

The value r in GEOMETRY PARAMETERS in Model.m changes the radius/size of the enzymes

The geometry is parametrically defined in domain2.m
