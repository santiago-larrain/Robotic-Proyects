function ode_ex_c

clear all
close all

p = [10, 0.5, 0.35]
y0 = [0, 0]
t1=cputime;
[t, y] = ode45(@ode_ex_funA, [0 20], y0, [], p)
cputime-t1
plot(t,y)
xlabel('t')
ylabel('y')

function yd = ode_ex_funA(t, y, p)
yd = zeros (2,1);
vo = p(1);
k1 = p(2);
k2 = p(3);
yd(1) = vo - k1*y(1);
yd(2) = k1*y(1) - k2*y(2);