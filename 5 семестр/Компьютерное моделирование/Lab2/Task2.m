function Task2()
[T, Y] = ode45(@f, [0 1], [1 1]);
plot(T,Y(:,1),'-',T,Y(:,2),'.');

function dy = f(x, y) % y(1) -> y, y(2) -> z
dy = zeros(2, 1);
dy(1) = (y(2)-y(1))*x;
dy(2) = (y(2)+y(1))*x;