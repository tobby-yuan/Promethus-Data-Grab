clear all;
close all;
format long;
ColumnLabel={'Standby','E2 Setup','KPIMON-GO xApp','TS Use Case'};
Column=0:3;
Power_percent=[0, 15.66219856, 227.8790747, 1598.625104];
CPU_percent=  [0, -2.70130091, 447.6177838, 2016.946424];
MEM_percent=  [0, 0.845004799, 93.56980714, 464.364452];
hold on;
grid on;
plot(Column, Power_percent,'.--', Column, CPU_percent,'.-', Column, MEM_percent,'.-');
legend('Power Consumption','CPU Utilization', 'Memory Utilization');
xlim([0 3]);
ylim([-100 2100]);
xticks(Column);
xticklabels(ColumnLabel);
ylabel('Percentage difference from standby(%)');






