mkdir Exported
virtualenv --always-copy -p python3.8 virtual/
source virtual/bin/activate 
python3.8 -m pip install --no-cache-dir -r requirements.txt --ignore-installed
deactivate