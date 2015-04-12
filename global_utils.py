__author__ = 'fire'
import os
import global_values
from random import randint
def get_input_directory(game_name):
	return os.path.join(global_values.MAPS_DIR, game_name, global_values.INPUT_DIR)

def get_output_directory(game_name):
	return os.path.join(global_values.MAPS_DIR, game_name, global_values.OUTPUT_DIR)

def get_base_dir(game_name):
    return os.path.join(global_values.MAPS_DIR, game_name)

def get_agg_color_stats_file(game_name):
    return os.path.join(global_values.MAPS_DIR, game_name, global_values.STATS_FILENAME_AGG)
def get_individual_stats_file(game_name):
        return os.path.join(global_values.MAPS_DIR, game_name, global_values.OUTPUT_DIR, global_values.STATS_FILENAME)


def write_to_stat_fh(stat_fh,stat):
    stat_fh.write('[%s]:=:%s: %s\n' % (stat[0],stat[1],stat[2]))

def build_html_file(game_name):
    game_name_html = '%s.html' % (game_name)
    return os.path.join(global_values.MAPS_DIR, game_name, game_name_html)


def check_folder(folder_name):
    if not os.path.exists(folder_name):
       os.makedirs(folder_name)

def random_color():
	r = randint(0,255)
	g = randint(0,255)
	b = randint(0,255)
	return [r,g,b]

def check_folders(game_name):
    input_folder = get_input_directory(game_name)
    output_folder = get_output_directory(game_name)
    check_folder(input_folder)
    check_folder(output_folder)

def check_input(target_name,arg_type):
    target_list = [dir_name for dir_name in os.listdir(global_values.MAPS_DIR) if os.path.isdir(os.path.join(global_values.MAPS_DIR, dir_name))]
    if arg_type == global_values.INPUT_MODE:
        return [target_name in target_list, target_list]
    elif arg_type == global_values.OUTPUT_MODE:
        if target_name in target_list:
            full_name_dir = os.path.join(global_values.MAPS_DIR,target_name,global_values.OUTPUT_DIR)
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
    return [dir_name for dir_name in os.listdir(global_values.MAPS_DIR) if os.path.isdir(os.path.join(global_values.MAPS_DIR, dir_name))]

def make_final_file_folder_name(game_name,filename):
	return os.path.join(global_values.MAPS_DIR,game_name,global_values.OUTPUT_DIR,filename.split('.')[0])

def print_run_main_error():
    print 'cannot directly use this file'

if __name__ == "__main__":
    print_run_main_error()