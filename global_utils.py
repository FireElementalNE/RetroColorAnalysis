import math

__author__ = 'fire'
import os
import global_values
from random import randint

# dirs
# input directory
# output directory

def dirs_map(full_file_name, game_name):
    dirs = []
    dirs.append(full_file_name) #0
    dirs.append(game_name) # 1
    dirs.append(get_input_directory(game_name)) # 2
    dirs.append(get_output_directory(game_name)) # 3
    dirs.append(output_to_input(full_file_name,
                                get_output_directory(game_name), 'png')) # 4
    dirs.append(output_to_input(full_file_name,
                                get_output_directory(game_name), global_values.STAT_ENDING_TMP)) # 5
    dirs.append(get_agg_color_stats_file(game_name)) # 6
    dirs.append(os.path.join(get_base_dir(game_name), 'out_aggregate.png')) # 7
    dirs.append(get_base_dir(game_name))
    dirs.append(get_individual_stats_file(game_name))

    return dirs

def get_input_directory(game_name):
    '''
    get the input directory
    :param game_name: the game name
    :return: path to input dir
    '''
    return os.path.join(global_values.MAPS_DIR, game_name, global_values.INPUT_DIR)

def output_to_input(full_file_name, output_dir, ending):
    filename_base = os.path.basename(full_file_name).split('.')[0]
    filename_output = '%s_out.%s' % (filename_base, ending)
    return os.path.join(output_dir, filename_output)

def get_output_directory(game_name):
    '''
    get the output directory
    :param game_name: the game name
    :return: path to output dir
    '''
    return os.path.join(global_values.MAPS_DIR, game_name, global_values.OUTPUT_DIR)


def get_base_dir(game_name):
    '''
    get the base game directory
    :param game_name: the game name
    :return: path to base dir
    '''
    return os.path.join(global_values.MAPS_DIR, game_name)


def get_agg_color_stats_file(game_name):
    '''
    get path to aggregate stats file
    :param game_name: game name
    :return: path to aggregate stats file
    '''
    return os.path.join(global_values.MAPS_DIR, game_name, global_values.STATS_FILENAME_AGG)


def get_individual_stats_file(game_name):
    '''
    get path to individual stats file
    :param game_name: the game name
    :return: the individual stats file
    '''
    return os.path.join(global_values.MAPS_DIR, game_name, global_values.OUTPUT_DIR, global_values.STATS_FILENAME)


def make_final_file_folder_name(game_name, filename):
    '''
    get the final output folder name
    :param game_name: the game name
    :param filename: the filename
    :return: the correct dir
    '''
    return os.path.join(global_values.MAPS_DIR, game_name, global_values.OUTPUT_DIR, filename.split('.')[0])


def write_to_stat_fh(stat_fh, stat):
    '''
    write to a stats file
    :param stat_fh: the stats file file handle
    :param stat: the stat
    :return: nothing
    '''
    stat_fh.write('[%s]:=:%s: %s\n' % (stat[0], stat[1], stat[2]))


def build_html_file(game_name):
    '''
    get path to html file
    :param game_name: the game name
    :return: path to html file
    '''
    game_name_html = '%s.html' % (game_name)
    return os.path.join(global_values.MAPS_DIR, game_name, game_name_html)


def check_folder(folder_name):
    '''
    check if a folder exists if it doesnt create it
    :param folder_name: the path to the folder
    :return: nothing
    '''
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def random_color():
    '''
    get a random color
    :return: random RGB color
    '''
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return [r, g, b]


def check_folders(game_name):
    '''
    check all folder for existance
    :param game_name:  the game name
    :return: nothing
    '''
    input_folder = get_input_directory(game_name)
    output_folder = get_output_directory(game_name)
    check_folder(input_folder)
    check_folder(output_folder)


def check_input(target_name, arg_type):
    '''
    check the input see if passed game exists in file structure
    :param target_name: the passed val
    :param arg_type: output or input
    :return: tuple of truth value an games that match
    '''
    target_list = []
    for dir_name in os.listdir(global_values.MAPS_DIR):
        if os.path.isdir(os.path.join(global_values.MAPS_DIR, dir_name)):
            target_list.append(dir_name)
    if arg_type == global_values.INPUT_MODE:
        return [target_name in target_list, target_list]
    elif arg_type == global_values.OUTPUT_MODE:
        if target_name in target_list:
            full_name_dir = os.path.join(global_values.MAPS_DIR, target_name, global_values.OUTPUT_DIR)
            counter = 0
            for root, dirnames, filenames in os.walk(full_name_dir):
                for filename in filenames:
                    if filename.endswith('png'):
                        counter += 1
            return [counter > 0, target_list]
    elif arg_type == global_values.HTML_MODE:
        return [target_name in target_list, target_list]
    return [False, target_list]


def get_games_list():
    '''
    get full game list
    :return: the existing game folders
    '''
    return [dir_name for dir_name in os.listdir(global_values.MAPS_DIR) if os.path.isdir(os.path.join(global_values.MAPS_DIR, dir_name))]


def print_run_main_error():
    print 'cannot directly use this file'

def euclid(x1, y1, z1, x2, y2, z2):
    '''
    calculates the euclidean distance in a 3D space
    between two points
    '''
    x_prime = pow(x2 - x1, 2)
    y_prime = pow(y2 - y1, 2)
    z_prime = pow(z2 - z1, 2)
    return math.sqrt(x_prime + y_prime + z_prime)

if __name__ == "__main__":
    print_run_main_error()