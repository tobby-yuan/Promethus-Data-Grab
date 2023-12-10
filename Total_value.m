close all;
format long;
ColumnLabel={'Standby','E2 Setup','KPIMON-GO xApp','TS Use Case'};
Column=0:3;
Power_total=[0.294370218, 0.340475067, 0.965178348, 5.000246429];
CPU_total=  [7.35359576, 7.154953011, 40.26959813, 155.6716825];
MEM_total=  [558.921875, 563.6447917, 1081.903995, 3154.356377];


% str=[repmat('',4,1) num2str(Power_total')];



figure(1)
plot(Column, Power_total,'.--');
legend('Power Consumption');
xlim([0 3]);
ylim([-0.5 6]);
ylabel('Total Power Consumption (Watt)');
xticks(Column);
xticklabels(ColumnLabel);
% text(Column,Power_total,cellstr(str))
grid on;


figure(2)
plot(Column, CPU_total,'.-', 'Color', 'red');
legend('CPU Utilization');
xlim([0 3]);
ylim([-5 200]);
ylabel('Total CPU Utilization (%)');
xticks(Column);
xticklabels(ColumnLabel);
grid on;

figure(3)
plot(Column, MEM_total,'.-', 'Color', '[0.9290 0.6940 0.1250]');
legend('Memory Utilization');
xlim([0 3]);
ylim([-100 3500]);
ylabel('Total Memory Utilization (Mega Byte)');
xticks(Column);
xticklabels(ColumnLabel);
grid on;
