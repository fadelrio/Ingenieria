clear all; close all; clc

syms x1 x2 x3 u y;

x = [x1;x2;x3];

Q_max = 5;
R = 40;
tau = 1;

f1 = Q_max*R^(x3-1)-sqrt(x1-x2);

f2 = sqrt(x1-x2)-sqrt(x2);

f3 = (-x3+u)/tau;

f = [f1;f2;f3];

%%
y = x1;

A = jacobian(f,x);

B = jacobian(f,u);

C = jacobian(y,x);

D = jacobian(y,u);


%equilibrio-------

x1e = 2;
x2e = 1;
x3e = 0.56;
ue = 0.56;
ye = 2;

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

%it is stable!!!!



