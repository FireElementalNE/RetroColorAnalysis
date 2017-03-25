__author__ = 'fire'
import os
import argparse
import multiprocessing
from color_tests.analyzecolor import analyze_individual
from color_tests.analyzecolor import analyze_outputs
import globals.global_values as global_values
import globals.global_utils as global_utils
import sys
import html_builder.html_builder as html_builder
import time

# TODO: Pidgen hole how close colors are (are there alot of complimentary colors? similar (analagous) colors? cool, warm? satuarion?)

def analyze_image(game_name, threaded):
    '''
    :param game_name: the name of the game folder to be analyzed
    :param arg_type: doing input or output analysis
    :param threaded: use threaded values
    :return: none
    '''
    arg_check = global_utils.check_input(game_name)
    if threaded:
        print 'Threaded Does not currently work.'
    if arg_check[0]:
        global_utils.check_folders(game_name)
        threads = []
        print 'Analzying individual images %s' % game_name
        directory_search = global_utils.get_input_directory(game_name)
        global_utils.sanitize_filenames(directory_search)
        for root, dirnames, filenames in os.walk(directory_search):
            for filename in filenames:
                if not filename.endswith('db') and not filename.endswith(global_values.STAT_ENDING_TMP):
                    full_file_name = os.path.join(directory_search, filename)
                    print 'Working on file %s.' % (filename)
                    #if (threaded):
                        #p = multiprocessing.Process(target=analyze_individual,
                        #                            args=(full_file_name, final_file_folder_name, output_dir), )
                        #threads.append(p)
                    #else:
                    analyze_individual(global_utils.dirs_map(full_file_name, game_name))
        output_dir = global_utils.get_output_directory(game_name)
        final_statistic_fh = open(os.path.join(output_dir, global_values.STATS_FILENAME), 'w+')
        for root, dirnames, filenames in os.walk(output_dir):
            for filename in filenames:
                if filename.endswith(global_values.STAT_ENDING_TMP):
                    fh_tmp = open(os.path.join(output_dir, filename), 'r')
                    line = fh_tmp.read()
                    final_statistic_fh.write(line)
                    fh_tmp.close()
                    os.remove(os.path.join(output_dir, filename))
        final_statistic_fh.close()
        print 'Creating output structure %s' % game_name
        directory_search = global_utils.get_output_directory(game_name)
        analyze_outputs(global_utils.dirs_map('', game_name))
        html_builder.build_html(game_name)
        #if threaded:
            #[x.start() for x in threads]
            #[x.join() for x in threads]

    else:
        sys.stdout.write('Bad args. Must be one of:\n')
        for game in arg_check[1]:
            sys.stdout.write('\t%s\n' % game)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Old game color analyzer')
    parser.add_argument('-i', '--input', help='Input Folder (individual game)', required=False)
    parser.add_argument('-t', '--threaded', action='store_true', help='thread the execution', required=False)
    args = parser.parse_args()
    analyze_image(args.input, args.threaded)
    html_builder.build_html(args.input)

   