# BrainBugBusters
This tool was specifically designed to analyse clinical samples from FFPE specimens, however it can be used to analyse any bacterial sample. The outcome of this tool will result in a stacked barplot showing the abundance of every species and/or genus in your sample. This tool was designed with Oxford Nanopore sequencing reads (MinION), and was not tested with any other sequencing data. The input should be a folder containing all barcodes in a fastq.gz format. 

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
Install all needed scripts (EMU_loop_script.py, GhostCode.py).
```
git clone https://github.com/daanbrackel/BrainBugBusters
```
# Running the full pipeline
- start of by running the EMU_loop_script.py script. you can do this as followed (assuming your in the BrainBugBusters directorie where all scripts are located):
  ```
  python EMU_loop_script.py "input_folder" "output_folder" "emu_database_dir"
  ```
  the input folder must be a folder containing all barcode files in a fastq.gz format
  
  or enter 
  ```
  python EMU_loop_script.py --help
  ```
  for an explenation what each in/output is.

- Next run the GhostCode.py script to visualize all data. As input you should use the output folder of the previous script. The output folder **can not** be the same as the input folder, a different folder can be made by the user. Assuming your still in the BrainBugBuster directorie, use:

  ```
  python GhostCode.py "input_folder" "output_folder"
  ```
  or enter 
  ```
  python BBB.py --help
  ```
  for an explenation what each in/output is.
