clear all; close all; clc

syms x1 x2 x3 x4 u y;

x = [x1;x2;x3;x4];

m = 1600;
alfa_n = 12;
T_m = 190;
beta = 0.4;
w_n = 420;
w_m = 2*pi;
C_r = 0.01;
ro = 1.3;
C_d = 0.32;
a_o = 2.4;
g = 9.8;
tita = 4;

f1 = (1/m)*(alfa_n*x2*T_m*(1-beta*(alfa_n*x1/w_n - 1)^2)-m*g*sind(tita)+m*g*C_r+(1/2)*ro*C_d*a_o*x1^2);

f2 = x3;

f3 = x4;

f4 = -3*w_m*x4-3*w_m^2*x3-w_m^3*x2+w_m^3*u;

f = [f1;f2;f3;f4];

%%
y = x1;

A = jacobian(f,x);

B = jacobian(f,u);

C = jacobian(y,x);

D = jacobian(y,u);


%equilibrio-------

x1e = 20;
x3e = 0;
x4e = 0;
ue = m*(g*sind(tita)-g*C_r-(1/(2*m))*ro*C_d*a_o*x1e^2)/(alfa_n*T_m*(1-beta*(((alfa_n*x1e)/w_n)-1)^2));
x2e = ue;
ye = x1e;

A = subs(A, str2sym({'x1','x2','x3','u','y'}),{x1e,x2e,x3e,ue,ye});
B = subs(B, str2sym({'x1','x2','x3','u','y'}),{x1e,x2e,x3e,ue,ye});
C = subs(C, str2sym({'x1','x2','x3','u','y'}),{x1e,x2e,x3e,ue,ye});
D = subs(D, str2sym({'x1','x2','x3','u','y'}),{x1e,x2e,x3e,ue,ye});

A_eq = double(A);
B_eq = double(B);
C_eq = double(C);
D_eq = double(D);


[Num,Den] = ss2tf(A_eq,B_eq,C_eq,D_eq);

P = zpk(ss(A_eq,B_eq,C_eq,D_eq));

%%

s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

Pap = zpk([-0.01735],[0.01735],1);
Pmp = zpk([],[-6.283 -6.283 -6.283 -0.01735],327.5);

figure();
bode(P, Pmp, Pap, optionss, {0.0001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%
close all;

wgc = 0.078; %a esta frecuencia la fase de la Pap es de -25°

wgc = 0.0851; %la frecuencia que quedó despues de hacer propio el controlador

wgc = 1; %pruebo este a ver si me da mejor es tiempo de establecimiento

wgc = 4.99; %tercer intento

C = db2mag(174)*zpk([],[0 -100 -100 -100 -100],1)*inv(Pmp);

L = minreal(P*C);

figure();
%optionss.PhaseMatchingValue=-180;
%optionss.PhaseMatchingFreq=20;
bode( L, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
rlocus(L);
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

T_s = 4*tand(18.2/2)/wgc;

Pade = zpk([4/T_s],[-4/T_s],-1);

L_pade = minreal(L*Pade);


figure();
%optionss.PhaseMatchingValue=-180;
%optionss.PhaseMatchingFreq=20;
bode( L_pade, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%
close all;

S = 1/(1+L_pade);

T = 1-S;

CS = C*S;

PS = P*S;

altura_step = 4;

step_options = stepDataOptions();
step_options.StepAmplitude = 4;

figure();
step(S,step_options);
legend

figure();
step(T,20,step_options);
legend

figure();
step(CS,step_options);
legend

figure();
step(PS,step_options);
legend


C_digit = c2d(C,T_s,'tustin');