global GEOMETRY_PARAMETERS
vmax = 0.05;   % E1 in seconds^-1
km = 0.004;    % E1 in mM
vmax2 = 0.1;   % E2 in seconds^-1 
km2 = 0.03;    % E2 in mM
T = 0.2;
N = 25;
    
% Build the model at various values of d - gradually brings the enzymes
% closer together
distance = 1500;
for i = 3.8:-0.1:0.2
    
    GEOMETRY_PARAMETERS = struct('a', 4.0, 'c', i, 'r', 0.1);

    myufunction = @(region,state) -(vmax2*state.u)/(state.u+km2);
    
    % Create a model using the domain file to build the geometry
    model = createpde();
    geometryFromEdges(model, @domain2)
    applyBoundaryCondition(model, 'neumann', 'Edge', 2,'q',0.0, 'g', vmax);
    applyBoundaryCondition(model, 'neumann', 'Edge', 4,'q',0.0, 'g', myufunction);
    applyBoundaryCondition(model, 'neumann', 'Edge', [1, 3, 5], ...
    'q', 0.0, 'g', 0.0);
    specifyCoefficients(model, 'm', 0.0, 'd', 1.0, 'c', 100, 'a', 0.0, ...
    'f', 0.0);
    setInitialConditions(model, 0.0);

    mesh = generateMesh(model, 'MesherVersion', 'R2013a', 'Hmax', 0.1);
    times = linspace(0, T, N);
    results = solvepde(model, times);
    u = results.NodalSolution;

    figure(1);
    axis tight manual % this ensures that getframe() returns a consistent size
    %filename = 'diffusion.gif';
    pdeplot(model, 'XYData', u(:,end), 'ZData', u(:,end), 'Mesh', 'on');
    c = colorbar;
    c.Label.String = 'Concentration (mM)';
    xlabel x
    ylabel y
    zlabel u
    grid on
    str = sprintf('Concentration at time t = %0.2f (mM)', T);
    title(str)
    az = 0;
    el = 0;
    view(az, el);
    
    % Build a gif of the diffusion over the mesh, this can be removed if it
    % causes errors
%     if i == 2
%         gif(filename);
%     else
%         gif
%     end     

    figure(2)
    pdegplot(model, 'edgelabels', 'on')
    a = GEOMETRY_PARAMETERS.a;
    c = GEOMETRY_PARAMETERS.c;
    xq = linspace(-a, a, 25);
    [Xq, Yq] = meshgrid(xq);
    querypoints = [Xq(:), Yq(:)]';
    [gradx, grady] = evaluateGradient(results, querypoints, 1:N);
    hold on
    quiver(Xq(:), Yq(:), -c*gradx(:,N), -c*grady(:,N))
    xlabel x
    ylabel y
    axis equal
    axis off
    hold off
    
    
    % Get all nodes at the second enzyme
    Ne4 = findNodes(mesh,'region','Edge',4);
    
    % Calculating angstrom distance at each loop
    % They begin at 1500 angstroms apart, each loop brings them 50 closer
    if i ~= 2
        distance = distance - 50;
    end

    figure(3)
    plot(times, mean(u(Ne4,:)));
    grid on
    title 'Concentration at Sink as a Function of Time';
    xlabel 'Time, seconds'
    ylabel 'Concentration (mM)'
    hold on
    
    % Calculate the total concentration at the sink over the 0.2s time
    % period
    conc = trapz(mean(u(Ne4,:)));
    
    % Assuming law of mass action, then all substrate that reached the sink
    % is converted to product IAA
    
    figure(4)
    plot(distance, conc*1000, '*', 'Color', 'Blue');
    grid on
    title 'Amount of IAA Produced vs Distance';
    xlabel 'Distance Between Enzymes (Angstroms)'
    ylabel 'Amount of IAA Produced (micromoles)'
    hold on    
end
