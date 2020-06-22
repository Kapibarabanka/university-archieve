function Task4()
[T, Y] = ode45(@f, [0 0.3], [0.5 1]);
plot(T,Y(:,1),'-',T,Y(:,2),'.');

function dy = f(x, y) % y(1) -> y, y(2) -> z
dy = zeros(2, 1);
dy(1) = exp(-x^2-y(2)^2)+2*x;
dy(2) = 2*y(1)^2+y(2);

