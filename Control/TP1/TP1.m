syms s;


%Ejercicio 1.1,dos grados de libertad

A = [0,1;
    -1,1];
B = [0;
    1];
C = [1,0];
D = [0];

sys = ss(A,B,C,D);

