clear; close all; format long;

% -----------------------Revise--------------------------------
filename = ['Setup_CPU_data.csv']; % Set Read file name
pod_num = 14;             % Set Pod number
Time_inte = [1702021500, 1702026000];  % Set Total inteval tion
situation_Label = {'E2 Setup','Stop E2 Setup'}; % Set Use Case Lable
situation_Time = [1702022516, 1702024365];      % Set Use Case Lable
tick_num = 7; % set x-axis tick time
x_label = 'Time(min)';
y_label = 'Memory Utilization Mega Byte';
y_usecase_scale = [0 0.05];
Total_function = false;
% -------------------------------------------------------------

data = readtable(filename);
data_pod=cell(pod_num,2);
init = true;
hold on;
for i=1:pod_num
    data_pod{i,1} = table2array(data(i, 2));
    data_pod{i,2} = table2array(data(i:pod_num*3:end, [1 3]));
    plot(data_pod{i,2}(1:end, 1) - Time_inte(1), data_pod{i,2}(1:end, 2));
    if Total_function
        if init
            data_total = data_pod{i,2};
            init = false;
        else
            data_total(1:end, 2) = data_total(1:end, 2) + data_pod{i,2}(1:end, 2);
        end
    end
end
if Total_function
    plot(data_total(1:end, 1) - Time_inte(1), data_total(1:end, 2));
end

Time_dueation = Time_inte(2) - Time_inte(1);
situation_Time = situation_Time - Time_inte(1);
tick_Time = sort([linspace(0, Time_dueation, tick_num) situation_Time]);

for i = 1:length(situation_Time)
    plot([situation_Time(i) situation_Time(i)], y_usecase_scale, 'r--');
end

Tic_situation_Label=cell(1, length(tick_Time) - 1);
j = 1;
for i = 1 : length(tick_Time)
    if j <= length(situation_Time) && tick_Time(i) == situation_Time(j)
        Tic_situation_Label{i} = situation_Label{j};
        j = j + 1;
    else
        Tic_situation_Label{i} = tick_Time(i);
    end
end
if Total_function
    legend([[data_pod{:,1}] ['Total'] [situation_Label(1,:)]]);
else
    legend([[data_pod{:,1}] [situation_Label(1,:)]]);
end
xticks(tick_Time);
xticklabels(Tic_situation_Label);
xlabel(x_label);
ylabel(y_label);



