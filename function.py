import requests
import csv

def save_to_csv(data, csv_filename, reset = False):
    write_type = 'a'
    if reset:
        write_type = 'w'
    with open(csv_filename, write_type, newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for i in range(len(data)):
            # print(data[i], type(data[i]))
            csv_writer.writerow(data[i])

def timetype_save_to_csv(Time, data, csv_filename, reset = False):
    write_type = 'a'
    if reset:
        write_type = 'w'
    with open(csv_filename, write_type, newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for i in range(len(data)):
            # print(data[i], type(data[i]))
            csv_writer.writerow([str(Time)] + data[i])

def get_url_content(url, params):
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Success get this URL")
            return(response.json())
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return 0

    except Exception as e:
        print(f"An error occurred: {e}")

def retrive_data(result, pod_n = 0, pod_name_label = 'pod'):
    if result['status'] == 'success':
        data = result['data']
        # print(data)
        returen_data = {}
        # print(f"Value at {timestamp}: {data['result'][j]}")
        returen_data.update({'Name': data['result'][pod_n]['metric'][pod_name_label]}) 
        returen_data.update({'Value': (data['result'][pod_n]['value'][1])})
        # print(returen_data)
        return returen_data
    else:
        print(f"Error: {result['error']}")

def sort_by_pod(sort_lable, sort_data, sort_num, name_lable = False, log_level = 3):
    output_data = []
    for i in range(sort_num):
        found_pod = False
        for j in range(len(sort_data)):
            if sort_lable[i] in sort_data[j][0]:
                if name_lable: 
                    sort_data[j][0] = name_lable[i]
                output_data.insert(i, sort_data[j])
                found_pod = True
                continue
        if not found_pod and log_level >= 3: 
            print(f'Waring: label {sort_lable[i]} not have corresponeded pod, Discard!')
    
    return output_data

