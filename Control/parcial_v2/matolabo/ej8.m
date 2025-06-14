clear all; clc 
close all; 

s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

%Para el T_s: frecuencia: 28.9 margen: 22.7

T_s = 0.0278;

Pade = zpk([4/T_s],[-4/T_s],-1);

%P = zpk([],[-80, 4i, -4i],80);

P = zpk(80/((s+80)*(s^2+4^2)));
Pmp = P;
Pap = zpk(0,0,1);

%{
Pap1 = zpk(0,0,0);
Pap2 = zpk(0,0,0);
Pap = Pap1*Pap2;

figure();
bode(Pap, Pap1, Pap2, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%}

figure();
bode(P, Pmp, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

C = db2mag(111)*zpk([-80,-1,-1],[0, -1000, -1000],1);

Lmp = minreal(C*Pmp);

L = minreal(P*C);

S = 1/(1+L);

T = 1-S;

PS = P*S;

CS = C*S;


figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(Lmp, L, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

L_digit = L*Pade;

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(L_digit, L, optionss, {0.1,100000});
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
step(T);
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