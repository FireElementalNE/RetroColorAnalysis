Retro Color Analysis
=====

By FireElementalNE

This program is made to analyze old game maps for color information.  

To use all that is needed are simple command line arguments:

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

NOTE: While it says the arguments are optional it is required that at least  
one is chosen.

**NOTE:** Threaded execution and all (-a option) do not currently work

The only external dependency is Python Imaging Library found [Here](http://www.pythonware.com/products/pil/ "PIL").  

This README is under construction (Hold your criticism!)