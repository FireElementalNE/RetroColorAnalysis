__author__ = 'fire'
from PIL import Image
import operator
import os
import globals.global_values as global_values
import globals.global_utils as global_utils
import color_utils
import sys
from scatterplots.scatter_plot import ScatterPlot
from dendrograms.distance_matrix import DMatrix
# TODO: use lab color distance from pure red and pure blue possibly?
# Maybe use hexagon distance (from 6 main colors, red blue yellow orandge purple green)

def test_white(pixel):
    '''
    tests if a pixel is too close to white
    :param pixel: RGB pixel
    :return: true iff the pixel is too close to white
    '''
    gray_scale = color_utils.to_grayscale(pixel)
    return gray_scale > global_values.WHITE_THRESHOLD


def test_black(pixel):
    '''
    tests if a pixel is too close to black
    :param pixel: RGB pixel
    :return: true iff the pixel is too close to black
    '''
    gray_scale = color_utils.to_grayscale(pixel)
    return gray_scale < global_values.BLACK_THRESHOLD


def avg(lst):
    '''
    returns the avg of a list
    :param list: the list
    :return: the average
    '''
    sum = 0
    for elm in lst:
        sum += elm
    return sum / (len(lst))


def avg_color_list(color_lst):
    '''
    returns the average color in a list of colors
    :param color_lst: the list of colors (a list of '-' separated values in a string)
    :return: the average color in the list
    '''
    sum_list = [0, 0, 0]
    for elm in color_lst:
        elem = elm[0].split('-')
        sum_list[0] += int(elem[0])
        sum_list[1] += int(elem[1])
        sum_list[2] += int(elem[2])
    sum_list[0] = sum_list[0] / len(color_lst)
    sum_list[1] = sum_list[1] / len(color_lst)
    sum_list[2] = sum_list[2] / len(color_lst)
    return sum_list


def actual_image_analysis(full_file_name):
    '''
    Analyze one image, creates a list of tuples that is sorted by pixel count
    so if a color appears more in the image it will be closer to the front
    of the list
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
                    hash_list[keyStr] = 1
                else:
                    hash_list[keyStr] += 1
    original.close()
    # sorts the list
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
    distance_metric3 = color_utils.avg_distance_colors(final_list, 'rgb')

    stat = [[os.path.basename(stat_file_name).split('.')[0],
             global_values.DISTANCE_METRIC_TAG_HSV, str(distance_metric1)],
            [os.path.basename(stat_file_name).split('.')[0],
             global_values.DISTANCE_METRIC_TAG_LAB, str(distance_metric2)],
            [os.path.basename(stat_file_name).split('.')[0],
             global_values.DISTANCE_METRIC_TAG_RGB, str(distance_metric3)]]
    for x in stat:
        global_utils.write_to_stat_fh(stat_fh,x)
    stat_fh.close()


def make_scatter_plot(all_color_list, dirs, is_agg):
    '''
    create a scatter plot
    :param all_color_list: a list of colors for the scatter plot
    :param dirs: the dirs array
    :return: nothing but makes the scatter plot
    '''
    rgb_val_dict = {}
    for color in all_color_list:
        tmp = color.split('-')
        r = int(tmp[0])
        g = int(tmp[1])
        b = int(tmp[2])
        if global_values.DISTANCE_TYPE == 'LAB':
            rgb_val_dict[color] = color_utils.rgb_to_lab(r, g, b)
        elif global_values.DISTANCE_TYPE == 'HSV':
            rgb_val_dict[color] = color_utils.rgb_to_hsv(r, g, b)
        elif global_values.DISTANCE_TYPE == 'RGB':
            rgb_val_dict[color] = [r, g, b]
        else:
            print 'Incorrect setting in globals.DISTANCE_TYPE: ', global_values.DISTANCE_TYPE
            sys.exit(0)
        splot = ScatterPlot(rgb_val_dict, dirs, is_agg)
        splot.make_scatter_plot()


def make_d_matrix(sorted_color_list, dirs, is_agg):
    '''
    Make dendrogram, using  LAB, HSV or RGB values for the
    distance matrix
    :param sorted_color_list: a list of colors for the dendrogram
    :param dirs: the dirs array
    :return: nothing but makes dendrogram file
    '''
    rgb_val_dict = {}
    for color in sorted_color_list:
        tmp = color.split('-')
        r = int(tmp[0])
        g = int(tmp[1])
        b = int(tmp[2])
        if global_values.DISTANCE_TYPE == 'LAB':
            rgb_val_dict[color] = color_utils.rgb_to_lab(r, g, b)
        elif global_values.DISTANCE_TYPE == 'HSV':
            rgb_val_dict[color] = color_utils.rgb_to_hsv(r, g, b)
        elif global_values.DISTANCE_TYPE == 'RGB':
            rgb_val_dict[color] = [r, g, b]
        else:
            print 'Incorrect setting in globals.DISTANCE_TYPE: ', global_values.DISTANCE_TYPE
            sys.exit(0)
    dmatrix = DMatrix(rgb_val_dict, dirs, is_agg)
    dmatrix.compute_table()
    dmatrix.cluster_samples()


def analyze_outputs(dirs):
    '''
    Analyze the output images from the input step, creates
    color swatches for the most common colors
    :param dirs: the dirs structure
    :return: nothing makes stats and image file
    '''
    output_dir = dirs[3]
    all_colors = []
    counter = 0
    for root, dirnames, filenames in os.walk(output_dir):
        for filename in filenames:
            if filename.endswith('png') and 'dendrogram' not in filename and 'scatter' not in filename:
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
    imOut.close()
    stat_file_name = dirs[6]
    new_final_list = []
    for el in final_list:
        z = '-'.join([str(x) for x in el])
        new_final_list.append(z)
    make_d_matrix(new_final_list, dirs, True)
    make_scatter_plot(new_final_list, dirs, True)
    calculate_stats(new_final_list, stat_file_name)

def analyze_individual(dirs):
    '''
    make a tmp stat and an image file for a given input
    also creates scatter plot
    :param dirs: the dirs structure
    :return: nothing but makes files
    '''
    full_file_name = dirs[0]
    output_filename = dirs[4]
    stat_file_name = dirs[5]
    sorted_x = actual_image_analysis(full_file_name) # do image analysis
    scatter_list = []
    for el in sorted_x[:global_values.MAX_SCATTER_POINTS]:
        scatter_list.append(el[0])
    make_scatter_plot(scatter_list, dirs, False)
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
    # save image
    imOut.save(output_filename)
    imOut.close()
    new_sorted_x = []
    for el in sorted_x[:global_values.number_of_colors]:
        new_sorted_x.append(el[0])
    calculate_stats(new_sorted_x, stat_file_name)
    d_gram_sorted_x = []
    actual_dgram_num = global_values.D_GRAM_NUMBER
    if global_values.D_GRAM_NUMBER >= len(sorted_x): # if we have less colors than are required
        actual_dgram_num = len(sorted_x)
    for el in sorted_x[:actual_dgram_num]:
        d_gram_sorted_x.append(el[0])
    make_d_matrix(d_gram_sorted_x, dirs, False)

if __name__ == "__main__":
    global_utils.print_run_main_error()





