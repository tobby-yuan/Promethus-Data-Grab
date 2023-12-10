import function as func
from datetime import datetime

# -------------------------------- main ----------------------------------------
# Defind query and start time
prometheus_url = "http://192.168.8.47:32000"
url = f"{prometheus_url}/api/v1/query"

Metrics = ['Power', 'CPU', 'Memory']
Metrics_query = []
Metrics_query.append("avg_over_time(sum(irate(kepler_container_joules_total{{container_namespace=~'.*ricplt.*|.*ricxapp.*',pod_name!~'.*kong.*'}}[1m])) by (pod_name, container_namespace, instance) [{}m:])")
Metrics_query.append("avg_over_time(sum(rate(container_cpu_usage_seconds_total{{name!~'.*POD.*',id=~'.*/docker.*', namespace=~'.*ricplt.*|.*ricxapp.*', pod!~'.*kong.*'}}[5m])*100) by (pod, namespace, instance) [{}m:])")
Metrics_query.append("avg_over_time(sum(container_memory_working_set_bytes{{name!~'.*POD.*',id=~'.*/docker.*', namespace=~'.*ricplt.*|.*ricxapp.*', pod!~'.*kong.*'}}) by (pod, namespace, instance) [{}m:])/1024/1024")


# Add Title and Time
csv_filename='Near-RT RIC Platform BM -- Setup.csv'
Use_case_lable = ["Mean of Standby Status", "Mean of E2 Setup", "Mean of Stop E2 Setup"]
# Use_case_lable = ["Mean of Standby Status", "Mean of E2 Setup", "Mean of KPIMON-GO xApp", "Mean of TS Use Case"]
# Use_case_End_time = [1701433265, 1701433265, 1701433265, 1701433265]
Use_case_End_time = [1702022516, 1702024365, 1702026000]
Use_case_time_duration = [30, 30, 27]
Blank_table = ["","","",""]
Blank_table_data = ["","",""]

# print( Metrics_query[0].format(Use_case_time_duration[0]))


# sort 
name_lable = ['influxDB', 'DBaas Server', 'Jaeger Adaptor', 'Routing Manager', 'xApp Manager', 'Subscription Manager', 'E2 Manager', 'E2 Termination', 'A1 Mediator', 'Alarm Manager', 'Alert Manager', 'Prometheus Server', 'VESPA Manager', 'O1 Mediator', 'KPIMONGO xApp', 'AD xApp',    'QP xApp',    'TS xApp',     'RC xApp'   ]
sort_lable = ['influx',   'dbaas',        'jaeger',         'rtmgr',           'appmgr',       'submgr',               'e2mgr',      'e2term',         'a1mediator',  'alarmmanager',  'alertmanager',  'prometheus-server', 'vespamgr',      'o1mediator',  'kpimon-go',     'ricxapp-ad', 'ricxapp-qp', 'trafficxapp', 'ricxapp-rc']

# Store data
pod_name_label = ['pod_name','pod', 'pod']
# pod_num = [14, 14 + 1, 14 + 5]
pod_num = [14, 14, 14]

#----------------------------------Above need to be Revise depended by your situation------------------------------
# Add Title and Time
Title_data = [[],[]]
for i in range(len(Use_case_lable)):
    Title_data[0].append(Use_case_lable[i])
    Title_data[0].extend(Blank_table)
    Title_data[1].append(f"Collect Time {datetime.fromtimestamp(Use_case_End_time[i]-Use_case_time_duration[i]*60)} ~ {datetime.fromtimestamp(Use_case_End_time[i])}, Duration: {Use_case_time_duration[i]} Minute")
    Title_data[1].extend(Blank_table)
# print(Title_data[1])
func.save_to_csv(data=Title_data, csv_filename=csv_filename, reset=True)

# Start grabbing data


for Merics_count in range(len(Metrics)):
    save_data_csv = []
    pod_blank = 25
    for Use_Case_count in range(len(Use_case_lable)):
        # Get the time data
        print(f"Start to grab mean of {Metrics[Merics_count]} metric in {Use_case_lable[Use_Case_count]}") 
        print(f"\t--> Collect Time {datetime.fromtimestamp(Use_case_End_time[Use_Case_count]-Use_case_time_duration[Use_Case_count]*60)} ~ {datetime.fromtimestamp(Use_case_End_time[Use_Case_count])}, Duration: {Use_case_time_duration[Use_Case_count]} Minute")        
        params = {'query': Metrics_query[Merics_count].format(Use_case_time_duration[Use_Case_count]), 'time': Use_case_End_time[Use_Case_count]}
        # print(params)
        result = func.get_url_content(url=url, params=params) 
        # print(result['data']['result'])

        save_data = []
        # Retrive_data
        for j in range(len(result['data']['result'])):
            data = func.retrive_data(result=result, pod_n=j, pod_name_label = pod_name_label[Merics_count])
            save_data.append(list(data.values()))
        # print(save_data)

        # Sort_data
        save_data = func.sort_by_pod(sort_lable=sort_lable, name_lable = name_lable, sort_data=save_data, sort_num = pod_num[Use_Case_count])
        save_data_csv.append(save_data)
    # print(len(save_data_csv[0]))
    if len(save_data_csv[0]) != 0:      
        #store Data into CSV
        total = []
        Metric_column = []
        for i in range(len(Use_case_lable)):
            Metric_column.extend([Metrics[Merics_count]] + Blank_table)
            total.extend(['Total', 0] + Blank_table_data)
        func.save_to_csv(data=[Metric_column], csv_filename=csv_filename)
        for i in range(pod_num[Merics_count]):
            data = []
            for j in range(len(Use_case_lable)):
                data.extend(save_data_csv[j][i] + Blank_table_data)
                total[1+2*j+3*j] = total[1+2*j+3*j] + float(save_data_csv[j][i][1])
            # print(data)
            func.save_to_csv(data=[data], csv_filename=csv_filename)
        func.save_to_csv(data=[total], csv_filename=csv_filename)
        pod_blank = pod_blank - pod_num[Merics_count]
    else:
        print(f"Waring: No Data")

    for i in range(pod_blank):
        func.save_to_csv(data=[[""]], csv_filename=csv_filename)




# while(timestamp <= time_inteval[1] or (timestamp != time_inteval[1] and (timestamp - time_step) < time_inteval[1])):
#     if timestamp > time_inteval[1]:
#         timestamp = time_inteval[1]
#     # print(timestamp)
#     # get the time data
#     url = f"{prometheus_url}/api/v1/query"
#     params = {'query': query, 'time': timestamp}
#     result = func.get_url_content(url=url, params=params)
#     save_data = []
#     for j in range(len(result['data']['result'])):
#         data = func.retrive_data(result=result, pod_n=j, pod_namee_label = pod_namee_label)
#         save_data.append(list(data.values()))
    
#     # print("Before sort", save_data, len(save_data))
#     save_data = func.sort_by_pod(sort_lable=sort_lable, name_lable=name_lable, sort_data=save_data, sort_num = pod_num)
#     # print("After sort", save_data, len(save_data))

#     func.save_to_csv(Time=timestamp, data=save_data, csv_filename=csv_filename) 
#     timestamp = timestamp + time_step

    