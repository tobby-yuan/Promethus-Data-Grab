clear; close all; format long;

% -----------------------Revise--------------------------------
filename = 'Standby_Memory_data.csv'; % Set Read file name
pod_num = 14;             % Set Pod number
Time_inte = [1701433265, 1701433265 + 3600];  % Set Total inteval tion
situation_Label = {'E2 Setup','Deploy KPIMON-GO xApp','Deploy TS Use Case'}; % Set Use Case Lable
situation_Time = linspace(1701433265+500, (1701433265 + 3600 - 300), 3);     % Set Use Case Lable
tick_num = 10; % set x-axis tick time
x_label = 'Time(s)';
y_label = 'Memory Utilization Mega Byte';
% -------------------------------------------------------------

data = readtable(filename);
data_pod=cell(pod_num,2);
hold on;
for i=1:pod_num
    data_pod{i,1} = table2array(data(i, 2));
    data_pod{i,2} = table2array(data(i:pod_num:end, [1 3]));
    plot(data_pod{i,2}(1:end, 1) - Time_inte(1), data_pod{i,2}(1:end, 2));
end
% ------------------------

filename = 'KPI_Memory_data.csv'; % Set Read file name
old_pod_num = pod_num;
pod_num = old_pod_num + 1;

data = readtable(filename);
hold on;
for i=old_pod_num + 1:pod_num
    data_pod{i,1} = table2array(data(i, 2));
    data_pod{i,2} = table2array(data(i:pod_num:end, [1 3]));
    plot(data_pod{i,2}(1:end, 1) - Time_inte(1), data_pod{i,2}(1:end, 2));
end
% ------------------------
% filename = 'TS_Memory_data.csv'; % Set Read file name
% old_pod_num = pod_num;
% pod_num = old_pod_num + 4;
% 
% data = readtable(filename);
% hold on;
% for i=old_pod_num + 1:pod_num
%     data_pod{i,1} = table2array(data(i, 2));
%     data_pod{i,2} = table2array(data(i:pod_num:end, [1 3]));
%     plot(data_pod{i,2}(1:end, 1) - Time_inte(1), data_pod{i,2}(1:end, 2));
% end
% ------------------------

Time_dueation = Time_inte(2) - Time_inte(1);
situation_Time = situation_Time - Time_inte(1);
tick_Time = sort([linspace(0, Time_dueation, tick_num) situation_Time]);

for i = 1:3
    plot([situation_Time(i) situation_Time(i)], [0 130], 'r--');
end

Tic_situation_Label=cell(1, length(tick_Time) - 1);
j = 1;
for i = 1 : length(tick_Time)
    if j < 4 && tick_Time(i) == situation_Time(j)
        Tic_situation_Label{i} = situation_Label{j};
        j = j + 1;
    else
        Tic_situation_Label{i} = tick_Time(i);
    end
end

legend([[data_pod{:,1}] [situation_Label(1,:)]]);
xticks(tick_Time);
xticklabels(Tic_situation_Label);
xlabel(x_label);
ylabel(y_label);



