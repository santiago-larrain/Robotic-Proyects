% Generamos la lista de muestras (1 ciclo)
n = 256;
i = 1;
listaY = zeros(1, 256);
listaX = zeros(1, 256);
while i < n + 1
    x = i - 1;
    listaY(i) = int16(128*sin((2*pi/256)*x) + 128);
    listaX(i) = x;
    i = i + 1;  
end

% Probamos con n ciclos
i = 0;
n = 5;
listaFinalY = [];
listaFinalX = [];
while i < n
    auxY = listaFinalY;
    auxX = listaFinalX;
    listaFinalY = [auxY, listaY];
    listaFinalX = [auxX, listaX + i*256];
    i = i + 1;
end

plot(listaFinalX, listaFinalY);
writematrix(listaY, "ValoresGenerador.txt");
type ValoresGenerador.txt