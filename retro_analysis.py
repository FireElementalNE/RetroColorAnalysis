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

def analyze_image(game_name, arg_type, threaded):
    '''
    :param game_name: the name of the game folder to be analyzed
    :param arg_type: doing input or output analysis
    :param threaded: use threaded values
    :return: boolean value corresponding to success
    '''
    arg_check = global_utils.check_input(game_name, arg_type)
    if (threaded):
        print 'Threaded Does not currently work.'
    if arg_check[0]:
        global_utils.check_folders(game_name)
        threads = []
        if arg_type == global_values.INPUT_MODE:
            print 'Input mode on %s' % game_name
            directory_search = global_utils.get_input_directory(game_name)
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
            return True
        elif arg_type == global_values.OUTPUT_MODE:
            print 'Output mode on %s' % game_name
            directory_search = global_utils.get_output_directory(game_name)
            analyze_outputs(global_utils.dirs_map('', game_name))
            return True
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
    parser.add_argument('-o', '--output', help='analyze outputs Folder (aggregate results)', required=False)
    parser.add_argument('-a', '--all', action='store_true', help='do it all', required=False)
    parser.add_argument('-t', '--threaded', action='store_true', help='thread the execution', required=False)
    parser.add_argument('-H', '--Html', help='build html file', required=False)
    args = parser.parse_args()
    if args.output and not args.input and not args.all:
        analyze_image(args.output, global_values.OUTPUT_MODE, args.threaded)
    elif args.input and not args.output and not args.all:
        analyze_image(args.input, global_values.INPUT_MODE, args.threaded)
    elif args.all and not args.output and not args.input:
        full_game_list = global_utils.get_games_list()
        print 'Not done yet, you will be unhappy if you use this.'
        #for game in full_game_list:
        #    analyze_image(game, global_values.INPUT_MODE, args.threaded)
        #    analyze_image(game, global_values.OUTPUT_MODE, args.threaded)
    elif args.Html and not args.output and not args.input and not args.all:
        if args.threaded:
            print 'Threaded does nothing here.'
        html_builder.build_html(args.Html)
    else:
        print 'Cant use all'
        parser.print_help()

   