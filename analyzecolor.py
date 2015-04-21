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
    :param full_file_name: the filename
    :return: the list of most common colors
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


def calculate_stats(final_list, stat_file_name):
    '''
    Takes a list of the most common rgb values and runs various stat
    checks on them
    :param final_list: the list of rgb values
    :param stat_file_name: the file name
    :return: nothing but writes stat file
    '''
    stat_fh = open(stat_file_name, 'w+')
    distance_metric1 = color_utils.avg_distance_colors(final_list, 'hsv')
    distance_metric2 = color_utils.avg_distance_colors(final_list, 'lab')
    distance_metric3 = color_utils.avg_distance_colors(final_list, 'cct')
    distance_metric4 = color_utils.avg_distance_colors(final_list, 'cct_max')
    distance_metric5 = color_utils.avg_distance_colors(final_list, 'cct_min')
    stat = [[os.path.basename(stat_file_name).split('.')[0],
             global_values.DISTANCE_METRIC_TAG_HSV, str(distance_metric1)],
            [os.path.basename(stat_file_name).split('.')[0],
             global_values.DISTANCE_METRIC_TAG_LAB, str(distance_metric2)],
            [os.path.basename(stat_file_name).split('.')[0],
             global_values.DISTANCE_METRIC_TAG_CCT, str(distance_metric3)],
            [os.path.basename(stat_file_name).split('.')[0],
             global_values.DISTANCE_METRIC_TAG_CCT_MAX, str(distance_metric4)],
            [os.path.basename(stat_file_name).split('.')[0],
             global_values.DISTANCE_METRIC_TAG_CCT_MIN, str(distance_metric5)]]
    for x in stat:
        global_utils.write_to_stat_fh(stat_fh,x)
    stat_fh.close()



def analyze_outputs(dirs):
    '''
    Analyze the output images from the input step
    :param dirs: the dirs structure
    :return: nothing makes stats and image file
    '''
    output_dir = dirs[3]
    all_colors = []
    counter = 0
    for root, dirnames, filenames in os.walk(output_dir):
        for filename in filenames:
            if filename.endswith('png'):
                all_colors.append(actual_image_analysis(os.path.join(output_dir, filename)))
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
    imOut.save(dirs[7])
    stat_file_name = dirs[6]
    new_final_list = []
    for el in final_list:
        z = '-'.join([str(x) for x in el])
        new_final_list.append(z)
    calculate_stats(new_final_list, stat_file_name)

def analyze_individual(dirs):
    '''
    make a tmp stat and an image file for a given input
    :param dirs: the dirs structure
    :return: nothing but makes files
    '''
    full_file_name = dirs[0]
    output_filename = dirs[4]
    stat_file_name = dirs[5]
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
    imOut.save(output_filename)
    new_sorted_x = []
    for el in sorted_x[:global_values.number_of_colors]:
        new_sorted_x.append(el[0])
    calculate_stats(new_sorted_x, stat_file_name)






