clear all; clc 
close all; 

s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

P = zpk([1000 1000],[1 1],1);
Pmp = zpk([-1000 -1000],[-1 -1],1);
%Pap = zpk(0,0,0);

Pap1 = zpk([1000 1000],[-1000 -1000],1);
Pap2 = zpk([-1 -1],[1 1],1);
Pap = Pap1*Pap2;

figure();
bode(Pap, Pap1, Pap2, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend


figure();
bode(P, Pmp, Pap, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%{
int 1:voy a tratar de cancelar un polo estable y un cero estable, a ver que pasa
int 1 *5 min despues*: mucha pinta de querer estable, para el margen de fase
puedo meter el cruce de los 0dB entre 6 y 172 rad/s, voy a los 172 a ver
que pasa (-15.4dB). Cumple el margen de fase, a ver que pasa con las rta al
escalón. ME OLVIDÉ EL CONTROL INTEGRAL, SOY RE GIL.
int 2: cancelo la dinamica de la planta, toca rajarse un tiro.
int 2 *5 min despues*: ajusto la ganancia, cambiaron las frecuencias, ahora
está entre 8 y 122 rad/s. Uso 122 rad/s (41.7dB). Nuevamente, cumple con el
margen de fase, ahora a ver que pasa con las rta al escalón. Me sigue dando
error constante al escalón, me habré mandado una cagada? Estaba viendo un
itervalo de tiempo muy corto, sigo siendo re gil. Tarda 5.77s en llegar a 1
clavado, y tiene un sobrepico del 6%. Cumple con el enunciado, calculo que
ya está.
%}
C = db2mag(41.7)*inv(Pmp)*zpk([],[0],1);

Lmp = minreal(C*Pmp);

L = minreal(P*C);

S = 1/(1+L);

T = 1-S;

PS = P*S;

CS = C*S;

%%
figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(Lmp, L, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
rlocus(L);
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

figure();
step(S);
legend

figure();
step(T,10);
legend

figure();
T_PS = T + PS;
step(T_PS); % Salida con referencia de escalón + perturbacion de entrada de escalón
legend

figure();
T_CS = S + CS;
step(T_CS); %Acción de control con referencia de escalon + pertubacion de entrada escalón
legend

figure();
step(PS);
legend

figure();
step(CS);
legend