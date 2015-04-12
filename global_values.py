__author__ = 'fire'
import global_utils

number_of_colors = 10

MAPS_DIR = 'maps'
INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

TAB = '\t'

INPUT_MODE = 1
OUTPUT_MODE = 2
HTML_MODE = 3

START_TAG = 50
END_TAG = 51

THUMBS_FILENAME = 'Thumbs.db'

BOOTSTRAP_CSS = '../../HTML_STATIC/CSS/libs/bootstrap.min.css'
STYLE_CSS = '../../HTML_STATIC/CSS/style.css'
JQUERY_JS = '../../HTML_STATIC/Javascript/libs/jquery.min.js'
SCRIPT_JS = '../../HTML_STATIC/Javascript/libs/bootstrap.min.js'

STATS_FILENAME = 'color.statistics'
STATS_FILENAME_AGG = 'color_aggregate.statistics'
DISTANCE_METRIC_TAG = "HSV Distance"
STAT_ENDING_TMP = '.stattmp'

FILE_STATS_RE = '^\[.*\] (.*)$'

TEST_FOLDER_NAME = 'test'
TEST_DIMENSIONS = [100,100]

if __name__ == "__main__":
    global_utils.print_run_main_error()

