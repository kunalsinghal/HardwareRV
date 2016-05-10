Verifier
========


# Installation

Python modules that are needed are stored in requirements.txt
They can be installed using pip by running the following command:
```
pip install -r requirements.txt
```


# Runnning

First of all configure environment for running the verifier scripts
```
source configure
```
Then to generate vhdl files for the monitoring circuit, run the following command
```
python src/main.py <path to target directory>
```
target directory should contains the meta file for while circuits need to be created

eg.,
```
python src/main.py tests/malloc
```


