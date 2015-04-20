__author__ = 'fire'
import global_utils
import global_values
import sys
from result_class import ImgResult

def build_html(game_name):
    '''
    :param game_name: the game name
    :return: none (but html file is created)
    '''
    arg_check = global_utils.check_input(game_name, global_values.HTML_MODE)
    if arg_check[0]:
        ImgResult(game_name)
    else:
        sys.stdout.write('Bad args. Must be one of:\n')
        for game in arg_check[1]:
            sys.stdout.write('\t%s\n' % game)

if __name__ == "__main__":
    global_utils.print_run_main_error()