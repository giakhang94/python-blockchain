**Activate the virtual environment**

```
source blockchain-env/bin/activate
for windows: blockchain-env/Scripts/activate
```

**Install all packages**

```
pip3 install -r requirements.txt
```

**Run the test**
Make sure to active the virtual environment

```
python3 -m pytest backend/test
```

**Run the application and API**
Make sure to activate the virtual environment

```
python3 -m backend.app
```

**Run a peer instance**
Make sure to activate the virtual environment

```
$env:PEER="True"; python -m backend.app (for windows)
export PEER="True" && python -m backend.app (for MacOS)

```
