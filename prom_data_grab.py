import function as func



    
# -------------------------------- main ----------------------------------------
# Defind query and start time
prometheus_url = "http://192.168.8.47:32000"
query = "sum(irate(kepler_container_joules_total{container_namespace=~'.*ricplt.*|.*ricxapp.*',pod_name!~'.*kong.*'}[1m])) by (pod_name, container_namespace, instance)"
# query = "sum(rate(container_cpu_usage_seconds_total{name!~'.*POD.*',id=~'.*/docker.*', namespace=~'.*ricplt.*|.*ricxapp.*', pod!~'.*kong.*'}[40s])*100) by (pod, namespace, instance)"
# query = "sum(container_memory_working_set_bytes{name!~'.*POD.*',id=~'.*/docker.*', namespace=~'.*ricplt.*|.*ricxapp.*', pod!~'.*kong.*'}) by (pod, namespace, instance) /1024/1024"
time_inteval = [1702021500, 1702026000]
time_step = 3

# Add column
csv_filename='Setup_Power_data.csv'
# csv_filename='Setup_Memory_data.csv'
# csv_filename='KPI_Memory_data.csv'
# csv_filename='TS_Memory_data.csv'
column = {'Name': 'pod', 'Value': 'value'}
func.timetype_save_to_csv(Time='time', data=[list(column.values())], csv_filename=csv_filename, reset=True)

# sort 
name_lable = ['influxDB', 'DBaas Server', 'Jaeger Adaptor', 'Routing Manager', 'xApp Manager', 'Subscription Manager', 'E2 Manager', 'E2 Termination', 'A1 Mediator', 'Alarm Manager', 'Alert Manager', 'Prometheus Server', 'VESPA Manager', 'O1 Mediator', 'KPIMONGO xApp', 'AD xApp',    'QP xApp',    'TS xApp',     'RC xApp'   ]
sort_lable = ['influx',   'dbaas',        'jaeger',         'rtmgr',           'appmgr',       'submgr',               'e2mgr',      'e2term',         'a1mediator',  'alarmmanager',  'alertmanager',  'prometheus-server', 'vespamgr',      'o1mediator',  'kpimon-go',     'ricxapp-ad', 'ricxapp-qp', 'trafficxapp', 'ricxapp-rc']

# name_lable = ['KPIMONGO xApp', ]
# sort_lable = ['kpimon-go']

# name_lable = ['AD xApp',    'QP xApp',    'TS xApp',     'RC xApp'   ]
# sort_lable = ['ricxapp-ad', 'ricxapp-qp', 'trafficxapp', 'ricxapp-rc']

# Store data
pod_name_label = 'pod_name'
# pod_name_label = 'pod'
pod_num = 14
# pod_num = 1
# pod_num = 4

#----------------------------------Above need to be Revise depended by your situation------------------------------
timestamp = time_inteval[0]
while(timestamp <= time_inteval[1] or (timestamp != time_inteval[1] and (timestamp - time_step) < time_inteval[1])):
    if timestamp > time_inteval[1]:
        timestamp = time_inteval[1]
    # print(timestamp)
    # get the time data
    url = f"{prometheus_url}/api/v1/query"
    params = {'query': query, 'time': timestamp}
    result = func.get_url_content(url=url, params=params)
    save_data = []
    for j in range(len(result['data']['result'])):
        data = func.retrive_data(result=result, pod_n=j, pod_name_label = pod_name_label)
        save_data.append(list(data.values()))
    
    # print("Before sort", save_data, len(save_data))
    save_data = func.sort_by_pod(sort_lable=sort_lable, name_lable=name_lable, sort_data=save_data, sort_num = pod_num)
    # print("After sort", save_data, len(save_data))

    func.timetype_save_to_csv(Time=timestamp, data=save_data, csv_filename=csv_filename) 
    timestamp = timestamp + time_step

    