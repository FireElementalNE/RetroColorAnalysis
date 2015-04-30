__author__ = 'fire'
import global_utils

number_of_colors = 10 # the number of colors to pick for the swatch
D_GRAM_NUMBER = 40 # the number of colors to pick for the dendrogram

MAPS_DIR = 'maps' # maps directory
INPUT_DIR = 'input' # input directory
OUTPUT_DIR = 'output' # output directory

TAB = '\t' # not REALLY neccesarry

INPUT_MODE = 1 # run in input mode
OUTPUT_MODE = 2 # run in output mode
HTML_MODE = 3 # run in html mode

START_TAG = 50 # flags for tags in html
END_TAG = 51 # flags for tags in html

THUMBS_FILENAME = 'Thumbs.db' # annoying stuff

BOOTSTRAP_CSS = '../../HTML_STATIC/CSS/libs/bootstrap.min.css' # for html imports
STYLE_CSS = '../../HTML_STATIC/CSS/style.css' # for html imports
JQUERY_JS = '../../HTML_STATIC/Javascript/libs/jquery.min.js' # for html imports
BOOTSTRAP_SCRIPT_JS = '../../HTML_STATIC/Javascript/libs/bootstrap.min.js' # for html imports
SCRIPT_JS = '../../HTML_STATIC/Javascript/script.js' # for html imports


STATS_FILENAME = 'color.statistics' # the combined color statistics file (not aggregated)
STATS_FILENAME_AGG = 'color_aggregate.statistics' # the aggregated stats file
DISTANCE_METRIC_TAG_HSV = "HSV Distance" # labels
DISTANCE_METRIC_TAG_LAB = "LAB Distance" # labels
STAT_ENDING_TMP = 'stattmp' # tmp file ending

DENDROGRAM_LABEL_HTML = 'View Dendrogram (click here)' # labels

FILE_STATS_RE = '^\[.*\] (.*)$' # re used for parsing color.statistics

TEST_FOLDER_NAME = 'test' # the test folder
TEST_DIMENSIONS = [100,100] # dimensions of test daya

BOOTSTRAP_TWIDTH = 12 # bootstrap class
BOOTSTRAP_COLW = BOOTSTRAP_TWIDTH / 3 # bootstrap class

BOOTSTRAP_TWIDTH_STR = 'col-sm-%d' % BOOTSTRAP_TWIDTH # bootstrap class
BOOTSTRAP_COLW_STR = 'col-sm-%d' % BOOTSTRAP_COLW # bootstrap class

P = 5
TRUNCATE_MODE = 'none' # Dendreogram settings
PLOT_TITLE = 'Color Clustering' # Dendreogram settings
ORIENTATION = 'left' # Dendreogram settings
FIGURE_SIZE = (8, 10) # Dendreogram settings

if __name__ == "__main__":
    global_utils.print_run_main_error()

