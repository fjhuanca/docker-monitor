# Minimalist CPU percentage and Memory Usage logger and plotter for docker container.

## pre-run
### Virtual env set using Python 3.9:
```
virtualenv -p /usr/bin/python3.9 .venv
```

```
source .venv/bin/activate
```
### Install dependencies:
```
pip install -r requirements.txt
```
    
## Usage:
```
python logger.py -cid <container id> -t <Monitoring time in seconds>
```
Note: if not time is set or it is set to 0, program will run until it is interrupted.