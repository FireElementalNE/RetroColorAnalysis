from scipy.cluster.hierarchy import dendrogram, linkage
import numpy
import matplotlib.pyplot as plt
from globals.global_utils import euclid, print_run_main_error
import globals.global_values as global_values
import os
class DMatrix:
    def __init__(self, cl, _dirs, _is_agg):
        '''
        initialize the dmatrix
        :param cl: the list of colors
        :param _dirs: the dirs structure
        :param _is_agg: flag for indicating whether output or input was run
        :return: nothing
        '''
        self.color_list = cl # will be a dictionary of {rgb : (hsv, lab, or rbg)}
        self.distance_matrix = []
        self.node_order = []
        self.dirs = _dirs
        self.is_agg = _is_agg

    def compute_table(self):
        '''
        Make a proper distance matrix from the color list
        :return: nothing
        '''
        for color_rgb, color_values in self.color_list.iteritems():
            tmp = []
            self.node_order.append(color_rgb)
            for color_rgb_test, color_values_test in self.color_list.iteritems():
                if color_rgb_test == color_rgb and color_values_test == color_values:
                    tmp.append(0.0)
                else:
                    distance = euclid(color_values[0], color_values[1], color_values[2],
                                      color_values_test[0], color_values_test[1], color_values_test[2])
                    tmp.append(distance)
            self.distance_matrix.append(tmp)

    def make_file_name(self):
        '''
        based on the is_agg member creates the correct filename for the
        Dentrogram
        :return: the filename
        '''
        if not self.is_agg:
            base_name = os.path.basename(self.dirs[0]).split('.')[0]
            d_name = '%s_dendrogram.png' % base_name
            return  os.path.join(self.dirs[3], d_name)
        else:
            return os.path.join(self.dirs[8], 'agg_dendrogram.png')

    def cluster_samples(self):
        '''
        http://stackoverflow.com/questions/11917779/how-to-plot-and-annotate-hierarchical-clustering-dendrograms-in-scipy-matplotlib
        Do the clustering
        :return: nothing
        '''
        title = os.path.basename(self.dirs[0]).split('.')[0]
        if title != '':
            title = title + ' - '
        if global_values.DISTANCE_TYPE == 'LAB':
            title = title + 'LAB'
        elif global_values.DISTANCE_TYPE == 'HSV':
            title = title + 'HSV'
        elif global_values.DISTANCE_TYPE == 'RGB':
            title = title + 'RGB'
        else:
            title = title + '???'
        numpy_matrix = numpy.array(self.distance_matrix)
        label_array = numpy.array(self.node_order)
        linked = linkage(numpy_matrix, method='single')
        plt.figure(figsize=global_values.FIGURE_SIZE)
        plt.title(title)
        dendrogram(linked, truncate_mode=global_values.TRUNCATE_MODE,
                   p=global_values.P, labels=label_array, orientation=global_values.ORIENTATION)
        plt.savefig(self.make_file_name())

if __name__ == "__main__":
    print_run_main_error()
