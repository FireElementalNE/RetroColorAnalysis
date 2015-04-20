from PIL import Image
import os
import argparse
import global_utils
import global_values

def run_main(num):
    '''
    :param num: The number of images to make
    :return: Nothing but creates the images
    '''
    global_utils.check_folders(global_values.TEST_FOLDER_NAME)
    for i in range(num):
        filename = '%d-test-out.png' % (i)
        imOut = Image.new("RGB", global_values.TEST_DIMENSIONS, "white")
        pixels = imOut.load()
        for x in range(imOut.size[0]):
            for y in range(imOut.size[1]):
                tmp = global_utils.random_color()
                pixels[x, y] = (tmp[0], tmp[1], tmp[2])
        imOut.save(os.path.join(global_utils.get_input_directory(global_values.TEST_FOLDER_NAME), filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Test data')
    parser.add_argument('-n', '--number', help='number of test files to create', required=False, type=int, default=5)
    args = parser.parse_args()
    run_main(args.number)

