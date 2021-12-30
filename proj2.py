import os, json, csv
import argparse
from datetime import datetime
from datetime import timezone

def add_args():
    parser = argparse.ArgumentParser(description='Convert json to csv file', add_help=False)
    parser.add_argument('--json_file', nargs='+')
    parser.add_argument('--output_filename', nargs=1)
    parser.add_argument('--time_str_format')
    parser.add_argument('-h', '--human-readable', action='store_true')
    parser.add_argument("--help", action="help")
    return parser.parse_args()

def generate_data(args):
    save = "summary-results.csv" if args.output_filename is None else args.output_filename
    with open(save, 'w') as csvfile:
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

        for filename in args.json_file:
            if os.path.isfile("./sample-files/" + filename):
                f = open("./sample-files/" + filename)
                data = json.load(f)

                row = [
                        data['timestamp'] if args.time_str_format is None else datetime.fromtimestamp(data['timestamp'], tz=timezone.utc).strftime(args.time_str_format),
                        data['jobs'][0]['job options']['bs'],
                        data['global options']['rw'],
                        data['global options']['rwmixread'] if 'rwmixread' in data['global options'] else None,
                        int(data['jobs'][0]['read']['iops']),
                        round(data['jobs'][0]['read']['bw_bytes'] / 1024, 1) if args.human_readable else data['jobs'][0]['read']['bw_bytes'],
                        int(data['jobs'][0]['read']['clat_ns']['mean']),
                        int(data['jobs'][0]['write']['iops']),
                        data['jobs'][0]['write']['bw_bytes'],
                        round(data['jobs'][0]['write']['clat_ns']['mean'] / 1024, 1) if args.human_readable else int(data['jobs'][0]['write']['clat_ns']['mean']),
                        data['jobs'][0]['error'],
                        filename
                    ]

                csvwrite.writerow(row)
                f.close()

if __name__ =="__main__":
    args = add_args()
    generate_data(args)