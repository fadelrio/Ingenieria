clear all; clc 
close all; 

T_s = 20e-3;

tau = 40e-3;

fase_digit = 5;

wgc = (4/T_s)*tand(5/2);

fase_pap2 = 2*atand(wgc/(2/tau));

fase_pap1 = 30 - fase_digit - fase_pap2;

p = wgc*tand(fase_pap1/2);


s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

P = zpk([50],[-50 p],-1);
Pmp = zpk([],[-p],1);
Pap1 = zpk([-p],[p],1);
Pap2 = zpk([50],[-50],-1);
Pap = Pap1*Pap2;

%{
Pap1 = zpk(0,0,0);
Pap2 = zpk(0,0,0);
Pap = Pap1*Pap2;
%}
figure();
bode(Pap, Pap1, Pap2, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend



figure();
bode(P, Pmp, Pap, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

C = db2mag(18.8)*inv(Pmp)*zpk([],[0],1);

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

figure();
rlocus(L);
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(S, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%margen de estabilidad: 0.7516;

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(T, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(PS, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(CS, optionss, {0.1,100000});
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