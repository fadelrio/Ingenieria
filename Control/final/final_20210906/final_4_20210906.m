s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
optionss.Grid='on';

ceros = [1 2];
polos = [7 8];

P = zpk(ceros,polos,1);
Pmp = zpk([-1 -2],[-7 -8],1);


Pap1 = zpk([1],[-1],-1);
Pap2 = zpk([2],[-2],-1);
Pap3 = zpk([-8],[8],1);
Pap4 = zpk([-7],[7],1);
Pap = Pap1*Pap2*Pap3*Pap4;

figure();
bode(Pap, Pap1, Pap2, Pap3, Pap4, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend



figure();
bode(P, Pmp, Pap, Pmp*Pap, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%
close all;

%La wgc tiene que ser menor a .216 o mayor a 45.4, para que la parte Pap me
%aporte menos de 30 de dafase

C = db2mag(0)*zpk([],[],1);

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
%%

%Toca realimentación en espacio de estados

Num = poly(ceros);

Den = poly(polos);

[A,B,C,D] = tf2ss(Num,Den);

pol_car = charpoly(A);

K = acker(A,B, [-1 -1]);



[num_monio, den_monio] = ss2tf(A-B*K,B,C,D);

P_monio = zpk(roots(num_monio),roots(den_monio),1);

figure();
rlocus(P_monio);

figure();
bode(P_monio*0.008, optionss, {.1,1000});

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