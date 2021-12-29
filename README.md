# File Processing Tools

## proj1.py
This script assumes that `proj1.py` is located one level above the `sample-files` folder and it generates the `summary-results.csv` file in the same directory as `proj1.py`

Run the script as usual with:
```
python3 proj1.py
```

## proj2.py
This script is a generalized version of `proj1.py`. You can specify the following arguments:
- `--json_file`: name of input json file to parse data, this could be multiple file names
- `--output_filename`: name of output filename
- `--time_str_format`: convert timestamp in given string format before writing to .csv file
    ex: --time_str_format '%d/%m/%y %H:%M:%S' would be something like '21/11/06 16:30:12'
- `-h`, `--human-readable`: convert size bw_bytes in human readable format in power of 1024

Again, the script assumes that `proj2.py` is located one level above the `sample-files` folder and the `.json` file names provided are located directly inside the `sample-files` folder

Example command

```
proj2.py --json_file rw50-8k.json rw70-8k.json --output_filename save_here.csv --time_str_format '%d/%m/%y %H:%M:%S' -h
```

## find.py
This script finds all files and directories that match the provided pattern:
```
python3 find.py --root ./sample-files --name 'rw*'
```
