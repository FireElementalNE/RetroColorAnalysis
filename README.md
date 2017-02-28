Retro Color Analysis
=====

By FireElementalNE

This program is made to analyze old game maps for color information.  
In reality you can analyze any set of images.   
[retro_analysis.py](https://github.com/FireElementalNE/RetroColorAnalysis/blob/master/retro_analysis.py) is the main program, you can split the input, output and HTML  
generation steps via the command line arguments.

```
usage: retro_analysis.py [-h] [-i INPUT] [-o OUTPUT] [-a] [-t] [-H HTML]

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
**NOTE:** The -t option and the -a option do nothing (works in progress)

The -i flag must be run before the -o flag which must be run  
before the -H flag.  
EXAMPLE:  
```
python main.py -i test
python main.py -o test
python main.py -H test
```

[main.py](https://github.com/FireElementalNE/RetroColorAnalysis/blob/master/main.py) is a wrapper that runs all three of these tests. Used for convince and simplicity.  
```
usage: main.py [-h] -g GAME

Wrapper function

optional arguments:
  -h, --help            show this help message and exit
  -g GAME, --game GAME  Game name
```

Input
------
The input flag searches a file directory (within the *maps* directory) that  
matches the given input. Each PNG Image within this directory  
is analyzed for color information. The 10 most common colors are selected  
(which is configurable in [global_values.py](https://github.com/FireElementalNE/RetroColorAnalysis/blob/master/globals/global_values.py) along with many other variables) and  
made into a color swatch.

Two statistics are also calculated:    

1. The average distance between the top colors in [HSV](http://en.wikipedia.org/wiki/HSL_and_HSV) space  
2. The average distance between the top colors in [LAB](http://en.wikipedia.org/wiki/Lab_color_space) space

A [Dendrogram](http://en.wikipedia.org/wiki/Dendrogram) of the top 40 colors (which is also configured in [global_values.py](https://github.com/FireElementalNE/RetroColorAnalysis/blob/master/globals/global_values.py))  
is also made. The distance matrix that is used to create the Dendrogram can be created using the values  
of the colors in RGB, HSV or LAB space (this is configurable in [global_values.py](https://github.com/FireElementalNE/RetroColorAnalysis/blob/master/globals/global_values.py)).


Output
------
Outputs from the input phase are taken as inputs to the output phase creating  
an aggregate result for each game folder.  

HTML
-------
The HTML builder takes all of the input and output data and makes a nice pretty  
bootstrap based web page on the fly. It holds all of the information discussed  
above.



External Dependencies
-----

* Python Imaging Library found [Here](http://www.pythonware.com/products/pil/ "PIL").
* SciPy found [here](http://www.scipy.org/).
* Numpy found [here](http://www.numpy.org/).
* Matplotlib found [here](http://matplotlib.org/).

Notes
----
[make_test_images.py](https://github.com/FireElementalNE/RetroColorAnalysis/blob/master/make_test_images.py) is used to create test images to upload to Github.  
```
usage: make_test_images.py [-h] [-n NUMBER]

Create Test data

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        number of test files to create
```

Program written in Python 2.7.6
