function Task5()
[T, Y] = ode45(@f, [3 5], [6 3]);
plot(T,Y(:,1),'-');

function dy = f(x, y) 
% y1' = y2 => y2'=-y2/x+y1/x^2+1
dy = zeros(2, 1);
dy(1) = y(2);
%y2'=y1''
dy(2) = -y(2)/x+y(1)/x^2+1;

