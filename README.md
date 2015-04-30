Retro Color Analysis
=====

By FireElementalNE

This program is made to analyze old game maps for color information.  
In reality you can analyze any set of images. 

```
usage: main.py [-h] [-i INPUT] [-o OUTPUT] [-a] [-t] [-H HTML]

Old game color analyzer

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input Folder (individual game)
  -o OUTPUT, --output OUTPUT
                        analyze outputs Folder (aggregate results)
  -a, --all             do it all
  -t, --threaded        thread the execution
  -H HTML, --Html HTML  build html file
```
The correct progression is using the -i argument on one  
run the -o argument on the next run and the -H argument  
on the final run.

Input
------
The input flag searches a file directory (within the *maps* directory) that  
matches the given input. When it is found each image within that directory  
is analyzed for color infomation. The a certain number of colors are selected  
(which is configurable in global_values.py

**NOTE:** The -t option and the -a option do nothing (works in progress)

The only external dependency is The Python Imaging Library found [Here](http://www.pythonware.com/products/pil/ "PIL").  

This README is under construction (Hold your criticism!)
