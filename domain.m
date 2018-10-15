function [x, y] = domain(bs, s)
global GEOMETRY_PARAMETERS
a = GEOMETRY_PARAMETERS.a;
c = GEOMETRY_PARAMETERS.c;
r = GEOMETRY_PARAMETERS.r;
d = GEOMETRY_PARAMETERS.d;
if nargin == 0
    x = 6;
    return
end
% a is area - x starts at -a, and finishes at a, same for y
% r is radius
% d is distance between enzymes - negative d reduces distance, positive
% distance increases distance, 0 is defaulted as 1 unit away
if nargin == 1
    d = [ -a    0     -c+r-d   0     c+r+d  0
          -c-r-d  pi*r  c-r+d    pi*r  a    pi*a
          1     1     1      1     1    1
          0     0     0      0     0    0 ];
    x = d(:,bs);
    return
end
x = zeros(size(s));
y = zeros(size(s));
if numel(bs) == 1  % scalar expansion required
    bs = bs * ones(size(s));
end
ii = find(bs == 1);
if ~isempty(ii)
    x(ii) = s(ii);
    y(ii) = 0;
end
ii = find(bs == 2);
if ~isempty(ii)
    theta = pi - s(ii)/r;
    x(ii) = -c + r * cos(theta) - d;
    y(ii) = r * sin(theta);
end
ii = find(bs == 3);
if ~isempty(ii)
    x(ii) = s(ii);
    y(ii) = 0;
end
ii = find(bs == 4);
if ~isempty(ii)
    theta = pi - s(ii)/r;
    x(ii) = c + r * cos(theta) + d;
    y(ii) = r * sin(theta);
end
ii = find(bs == 5);
if ~isempty(ii)
    x(ii) = s(ii);
    y(ii) = 0;
end
ii = find(bs == 6);
if ~isempty(ii)
    theta = s(ii)/a;
    x(ii) = a * cos(theta);
    y(ii) = a * sin(theta);
end
return
end

          