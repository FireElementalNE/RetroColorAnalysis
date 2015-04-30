__author__ = 'fire'
import global_utils

number_of_colors = 10
D_GRAM_NUMBER = 40

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
BOOTSTRAP_SCRIPT_JS = '../../HTML_STATIC/Javascript/libs/bootstrap.min.js'
SCRIPT_JS = '../../HTML_STATIC/Javascript/script.js'


STATS_FILENAME = 'color.statistics'
STATS_FILENAME_AGG = 'color_aggregate.statistics'
DISTANCE_METRIC_TAG_HSV = "HSV Distance"
DISTANCE_METRIC_TAG_LAB = "LAB Distance"
STAT_ENDING_TMP = 'stattmp'

DENDROGRAM_LABEL_HTML = 'View Dendrogram (click here)'

FILE_STATS_RE = '^\[.*\] (.*)$'

TEST_FOLDER_NAME = 'test'
TEST_DIMENSIONS = [100,100]

BOOTSTRAP_TWIDTH = 12
BOOTSTRAP_COLW = BOOTSTRAP_TWIDTH / 3

BOOTSTRAP_TWIDTH_STR = 'col-sm-%d' % BOOTSTRAP_TWIDTH
BOOTSTRAP_COLW_STR = 'col-sm-%d' % BOOTSTRAP_COLW

P = 5
TRUNCATE_MODE = 'none'
PLOT_TITLE = 'Color Clustering'
ORIENTATION = 'left'
FIGURE_SIZE = (8, 10)
if __name__ == "__main__":
    global_utils.print_run_main_error()

