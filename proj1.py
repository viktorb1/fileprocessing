import os, json, csv

def generate_data():
    with open('summary-results.csv', 'w') as csvfile:
        csvwrite = csv.writer(csvfile)
        
        fields = [  
                    'test_datetime', 
                    'io_bs', 
                    'io_rw', 
                    'io_rwmixread', 
                    'read_iops', 
                    'read_bw_bytes', 
                    'read_clat_ns_mean', 
                    'write_iops', 
                    'write_bw_bytes', 
                    'write_clat_ns_mean', 
                    'error', 
                    'logfile'
                ]

        csvwrite.writerow(fields)

        for filename in os.listdir("./sample-files"):
            if filename.endswith(".json"):
                f = open("./sample-files/" + filename)
                data = json.load(f)

                row = [
                        data['timestamp'],
                        data['jobs'][0]['job options']['bs'],
                        data['global options']['rw'],
                        data['global options']['rwmixread'] if 'rwmixread' in data['global options'] else None,
                        int(data['jobs'][0]['read']['iops']),
                        data['jobs'][0]['read']['bw_bytes'],
                        int(data['jobs'][0]['read']['clat_ns']['mean']),
                        int(data['jobs'][0]['write']['iops']),
                        data['jobs'][0]['write']['bw_bytes'],
                        int(data['jobs'][0]['write']['clat_ns']['mean']),
                        data['jobs'][0]['error'],
                        filename
                    ]

                csvwrite.writerow(row)
                f.close()

generate_data()