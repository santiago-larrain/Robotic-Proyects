clear all
close all

p = [10, 0.5, 0.35]
y0 = [0, 0]
tic
[t, y] = ode45(@ode_ex_fun, [0:(20-0)/(100-1):20], y0, [], p)
toc
plot(t,y)
xlabel('t')
ylabel('y')
