function yd = ode_ex_fun(t, y, p)
yd = zeros (2,1);
vo = p(1);
k1 = p(2);
k2 = p(3);
yd(1) = vo - k1*y(1);
yd(2) = k1*y(1) - k2*y(2);