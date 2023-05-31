# `monies.py`: Calculate who owes who what 

## Requirements
* `python` 3
* `pandas`, v1.4.4 recommended 

## Usage
You need a configuration YAML file and the data of who spent what as a CSV file. Then simply run
```
python <path/to/>monies.py <path/to/config>
```

Try running the example by executing
```
python monies.py example_config.yml
```
You should get the output
```
monies.py - INFO: loading example_config.yml
monies.py - INFO: reading example_data.csv
monies.py - INFO: calculating shares for person1, person2
monies.py - INFO: spent total: 24.00
monies.py - INFO: -- person1    --
monies.py - INFO:   share: 16.00
monies.py - INFO:   open:  10.00
monies.py - INFO: -- person2    --
monies.py - INFO:   share: 8.00
monies.py - INFO:   open:  -10.00
```