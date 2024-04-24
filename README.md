# BrainBugBuster
Tool to analyse clinical samples from FFPE specimens. 

# Installing plotly and EMU

### Create an environment for python v3.7
```
conda create --name py37 python=3.7
``` 

```
conda activate py37
```

### Install plotly in your py37 environment
```
pip install plotly
```
### Install Emu
do this in the direction you would like to install EMU in (for instance your programs folder)

```
conda config --add channels defaults
```
```
conda config --add channels bioconda
```
```
conda config --add channels conda-forge
```
```
conda install emu
```

# Installing all needed scripts
Install all needed scripts (EMU_loop_script.py, BBB.py).
```
git clone https://github.com/daanbrackel/BrainBugBuster
```
# Running the full pipeline
- start of by running the EMU_loop_script.py script. you can do this as followed (assuming your in the BrainBugBuster directorie where all scripts are located):
  ```
  python EMU_loop_script.py "input_folder" "output_folder" "emu_database_dir"
  ```
  or enter 
  ```
  python EMU_loop_script.py --help
  ```
  for an explenation what each in/output is.

- Next run the BBB.py script to visualize all data. As input you should use the output folder of the previous script. The output folder **can not** be the same as the input folder, a different folder can be made by the user. Assuming your still in the BrainBugBuster directorie, use:

  ```
  python BBB.py "input_folder" "output_folder"
  ```
  or enter 
  ```
  python BBB.py --help
  ```
  for an explenation what each in/output is.
