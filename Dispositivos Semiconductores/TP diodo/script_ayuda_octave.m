close all; clear all; clc;

%% Constantes
k = 1.3806e-23; % [J/K] Constante del Boltzmann
q = 1.60223e-19; % [C] Carga del electron
T = 300; % [K] Temperatura de trabajo
vth = k*T/q; % [V] Tensión termica

%% Lectura del archivo
archivo = 'datos_diodo.txt';

% Leo el archivo. Salteo la primera fila ya que esa tiene los nombres de las columnas
data = dlmread(archivo, '\t', 1, 0); % Nombre del archivo, delimitador

% Asigno datos
VD = data(:, 1); % Aca elegir la columna que represente los datos de tension
VD_directa = VD(VD>0);
ID = data(:, 2); % Aca elegir la columna que represente los datos de corriente
logID = log(abs(ID)); % Tomo el logaritmo natural del valor absoluto de la corriente

%% Graficos de los datos
% Grafico los datos en escala lineal
% Multiplico por 1e3 la corriente para pasarla a mA
figure();
plot(VD, 1e3*ID, '.b');
grid minor
ylabel('Corriente [mA]');
xlabel('Tension [V]');

% Grafico los datos en escala semilog
% Debo tomar el valor abosulto de ID ya que el logaritmo no admite valores negativos
figure();
semilogy(VD, abs(ID), '.b')
grid minor
ylabel('Corriente [A]');
xlabel('Tension [V]');
ylim([1e-15 1]); % Esto me permite controlar los limites del eje y


%% Ajuste de la curva de diodo en directa

% Hay que elegir los puntos en directa a ajustar con una recta.
% Seleccionar vMin y vMax para elegir un rango de puntos a ajsutar por una recta.
% Este debe ser el rango de tensiones donde la recta del diodo en escala semilog se parece a una recta
vMin = 0.2; % Valor minimo del rango (en volts)
vMax = 0.6; % Valor maximo del rango (en volts)

% Me quedo con los puntos entre vMin y vMax
indicesAjuste = (VD > vMin) & (VD < vMax);

% Tomo los datos en el intervalo elegido
VD_ajuste = VD(indicesAjuste);
ID_ajuste = ID(indicesAjuste);
logID_ajuste = logID(indicesAjuste);

% Ajusto una recta a esos puntos
coefAjuste = polyfit(VD_ajuste, logID_ajuste, 1); % Ajusto una recta y obtengo los coeficientes

% Calculo la corriente del diodo usando los parametros ajustados y el modelo exponencial
logIS = coefAjuste(2);
IS = exp(logIS); % Corriente de saturación en inversa
n = 1/(coefAjuste(1)*vth);% Coeficiente de idealidad
ID_ajustada = IS*exp(VD_directa/(n*vth));

disp(['Ajuste de IS = ' num2str(IS) ' A'])
disp(['Ajuste de n = ' num2str(n)])

figure()
semilogy(VD, abs(ID), '.b'), hold on
plot(VD_ajuste, abs(ID_ajuste), '.r')
plot(VD_directa, ID_ajustada, '--g', 'LineWidth', 2)
grid minor
ylim([10e-13 10])
ylabel('Corriente [A]');
xlabel('Tension [V]');
legend('Datos de simulacón', 'Datos elegidos para el ajuste', ['Curva ajustada. IS = ' num2str(IS) ' A || n = ' num2str(n)],"location", "northwest")






