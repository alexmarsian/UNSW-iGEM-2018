global GEOMETRY_PARAMETERS
GEOMETRY_PARAMETERS = struct('a', 4.0, 'c', 3.0, 'r', 0.1);
figure(1)
pdegplot(@domain, 'EdgeLabels', 'on', 'SubdomainLabels', 'on')
axis equal
axis off

figure(2)
[p, e, t] = initmesh(@domain, 'MesherVersion', 'R2013a', 'Hmax', 0.1);
pdeplot(p, e, t)
axis equal
