__author__ = 'fire'
from PIL import Image
import operator
import os
import global_values
import global_utils
import color_utils


def test_white(pixel):
    '''
    cant be too close to white
    :param pixel: RGB pixel
    :return: boolean if its too close
    '''
    if avg(pixel) > 220:
        return True
    return False


def test_black(pixel):
    '''
    cant be too close to black
    :param pixel: RGB pixel
    :return: boolean if its too close
    '''
    if avg(pixel) < 35:
        return True
    return False


def avg(list):
    '''
    returns the avg of a list
    :param list: the list
    :return: the average
    '''
    sum = 0
    for elm in list:
        sum += elm
    return sum / (len(list))


def avg_color_list(list):
    '''
    returs the averages in a list
    :param list:
    :return:
    '''
    sum_list = [0, 0, 0]
    for elm in list:
        elem = elm[0].split('-')
        sum_list[0] += int(elem[0])
        sum_list[1] += int(elem[1])
        sum_list[2] += int(elem[2])
    sum_list[0] = sum_list[0] / len(list)
    sum_list[1] = sum_list[1] / len(list)
    sum_list[2] = sum_list[2] / len(list)
    return sum_list


def actual_image_analysis(full_file_name):
    '''
    Does the actual pixel analysis
    :param full_file_name:  the full file path of the image
    :return: list of the top colors
    '''
    original = Image.open(full_file_name).convert('RGB')
    hash_list = {}
    for x in range(original.size[0]):
        for y in range(original.size[1]):
            r, g, b = original.getpixel((x, y))
            pixel = [r, g, b]
            if test_white(pixel) or test_black(pixel):
                continue
            else:
                keyStr = '%d-%d-%d' % (r, g, b)
                if keyStr not in hash_list.keys():
                    hash_list[keyStr] = 0
                else:
                    hash_list[keyStr] += 1

    sorted_x = sorted(hash_list.items(), key=operator.itemgetter(1))
    sorted_x = sorted_x[::-1]
    return sorted_x


def analyze_outputs(foldername,game_name):
    '''
    Anaylzes the swatch outputs of the individual images to make
    aggregate statistics
    :param foldername: the foldername
    :param game_name: the gamename
    :return: nothing but creates new stats
    '''
    all_colors = []
    counter = 0
    for root, dirnames, filenames in os.walk(foldername):
        for filename in filenames:
            if filename.endswith('png'):
                all_colors.append(actual_image_analysis(os.path.join(foldername, filename)))
                counter += 1
    final_list = []
    for index in range(global_values.number_of_colors):
        current_index_color_list = []
        for current_color in all_colors:
            current_index_color_list.append(current_color[index])
        final_list.append(avg_color_list(current_index_color_list))
    imOut = Image.new("RGB", # create aggregate 'swatch'
                      [global_values.number_of_colors * global_values.number_of_colors,
                       global_values.number_of_colors],
                      "white")
    pixels = imOut.load()
    count = 0
    for x in range(imOut.size[0]): # does teh same analysis as individual just on swatches
        current = None
        if count < global_values.number_of_colors:
            current = final_list[0]
        else:
            current = final_list[count / global_values.number_of_colors]
        for y in range(imOut.size[1]):
            pixels[x, y] = (int(current[0]), int(current[1]), int(current[2]))
        count += 1
    imOut.save(foldername + '_aggregate.png')
    stat_file_name = os.path.join(global_utils.get_base_dir(game_name), global_values.STATS_FILENAME_AGG)
    stat_fh = open(stat_file_name, 'w+')
    new_final_list = []
    for el in final_list:
        z = '-'.join([str(x) for x in el])
        new_final_list.append(z)
    # write stats
    distance_metric1 = color_utils.avg_distance_colors(new_final_list, 'hsv')
    distance_metric2 = color_utils.avg_distance_colors(new_final_list, 'lab')
    distance_metric3 = color_utils.avg_distance_colors(new_final_list, 'cct')
    stat = [[os.path.basename(stat_file_name).split('.')[0], global_values.DISTANCE_METRIC_TAG_HSV, str(distance_metric1)],
            [os.path.basename(stat_file_name).split('.')[0], global_values.DISTANCE_METRIC_TAG_HSV, str(distance_metric2)],
            [os.path.basename(stat_file_name).split('.')[0], global_values.DISTANCE_METRIC_TAG_CCT, str(distance_metric3)]]
    global_utils.write_to_stat_fh(stat_fh, stat[0])
    global_utils.write_to_stat_fh(stat_fh, stat[1])
    global_utils.write_to_stat_fh(stat_fh, stat[2])
    stat_fh.close()


def analyze_individual(full_file_name, foldername, output_dir):
    '''
    :param full_file_name: the full relative path of the image
    :param foldername: the folder for the output
    :param output_dir: the output directory
    :return: none but creates stats and image
    '''
    stat_file_name = '%s_%s' % \
                     (os.path.basename(full_file_name).split('.')[0], global_values.STAT_ENDING_TMP) # create the stat file name
    stat_fh = open(os.path.join(output_dir, stat_file_name), 'w+') # stat file handle
    sorted_x = actual_image_analysis(full_file_name) # do image analysis
    imOut = Image.new("RGB",
                      [global_values.number_of_colors * global_values.number_of_colors,
                       global_values.number_of_colors],
                      "white") # create 'swatch' image
    pixels = imOut.load()
    count = 0
    for x in range(imOut.size[0]): # based on top colors fill up swatch
        current = None
        if count < global_values.number_of_colors:
            current = sorted_x[0]
        else:
            current = sorted_x[count / global_values.number_of_colors]
        for y in range(imOut.size[1]):
            current_split = current[0].split('-')
            pixels[x, y] = (int(current_split[0]), int(current_split[1]), int(current_split[2]))
        count += 1
    imOut.save(foldername + '.png')
    new_sorted_x = []
    for el in sorted_x[:global_values.number_of_colors]:
        new_sorted_x.append(el[0])
    # This is to write stats
    distance_metric1 = color_utils.avg_distance_colors(new_sorted_x, 'hsv')
    distance_metric2 = color_utils.avg_distance_colors(new_sorted_x, 'lab')
    distance_metric3 = color_utils.avg_distance_colors(new_sorted_x, 'cct')
    stat = [[os.path.basename(full_file_name).split('.')[0], global_values.DISTANCE_METRIC_TAG_HSV, str(distance_metric1)],
            [os.path.basename(full_file_name).split('.')[0], global_values.DISTANCE_METRIC_TAG_LAB, str(distance_metric2)],
            [os.path.basename(full_file_name).split('.')[0], global_values.DISTANCE_METRIC_TAG_CCT, str(distance_metric3)]]
    global_utils.write_to_stat_fh(stat_fh, stat[0])
    global_utils.write_to_stat_fh(stat_fh, stat[1])
    global_utils.write_to_stat_fh(stat_fh, stat[2])
    stat_fh.close()





