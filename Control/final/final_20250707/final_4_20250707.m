clear all;close all;clc

s=tf('s');

P = zpk([1],[10],-1);
G=ss(P);

%Primero chequeo que sea controlable en espacio de estados

Ctl = ctrb(G.a, G.b);
rango = rank(Ctl);

%Como el rango es igual a el orden de mi transferencia, es un sistema
%controlable en espacio de estados

K=acker(G.a,G.b,[-2]);

tA=G.a-G.b*K;
tC=G.c-G.d*K;

[P_nueva_num,P_nueva_den] = ss2tf(tA,G.b,tC,G.d);

P_nueva = zpk(roots(P_nueva_num),roots(P_nueva_den),1);

%Para chequear que la P_nueva sea estable, chequeo eig(P_nueva)

eig = eig(P_nueva);

%Se obtiene -2, que como se encuentra en el semiplano izquierdo, significa
%que el lazo es estable


