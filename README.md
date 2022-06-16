# saveblue

This script helps you systematically detect large files in your working directory in a depth-first style.

Download
```
wget https://raw.githubusercontent.com/liulihe954/saveblue/main/saveblue.py
```
Usage
```
python3 saveblue.py --root SomeDir \
               --top \
               --suffix \
               --output \
               --delete
```
Mandatory:  
`--root` specifies the (parent) folder need to be scanned.

Optional:  
`--top` set the total number of file to return. default 20, means largest 20 files.  
`--suffix` specifies the suffix of file to check. default is empty which mean checking all files.  
`--output` specifies the name of the output file list. Will be auto generated.  
`--delete` if T, the found large files will be deleted. default False.   
