from scipy.cluster.hierarchy import dendrogram, linkage
import numpy
import matplotlib.pyplot as plt
from globals.global_utils import euclid
import globals.global_values as global_values
import os
class DMatrix:
    def __init__(self, cl, _dirs, _is_agg):
        self.color_list = cl # will be a dictionary of {rgb : lab}
        self.distance_matrix = []
        self.node_order = []
        self.dirs = _dirs
        self.is_agg = _is_agg

    def compute_table(self):
        for color_rgb, color_lab in self.color_list.iteritems():
            tmp = []
            self.node_order.append(color_rgb)
            for color_rgb_test, color_lab_test in self.color_list.iteritems():
                if color_rgb_test == color_rgb and color_lab_test == color_lab:
                    tmp.append(0.0)
                else:
                    distance = euclid(color_lab[0], color_lab[1], color_lab[2],
                                      color_lab_test[0], color_lab_test[1], color_lab_test[2])
                    tmp.append(distance)
            self.distance_matrix.append(tmp)

    def make_file_name(self):
        if not self.is_agg:
            base_name = os.path.basename(self.dirs[0]).split('.')[0]
            d_name = '%s_dendrogram.png' % base_name
            return  os.path.join(self.dirs[3], d_name)
        else:
            return os.path.join(self.dirs[8], 'agg_dendrogram.png')

    def cluster_samples(self):
        '''
        http://stackoverflow.com/questions/11917779/how-to-plot-and-annotate-hierarchical-clustering-dendrograms-in-scipy-matplotlib
        '''
        numpy_matrix = numpy.array(self.distance_matrix)
        label_array = numpy.array(self.node_order)
        linked = linkage(numpy_matrix, method='single')
        plt.figure(figsize=global_values.FIGURE_SIZE)
        plt.title(os.path.basename(self.dirs[0]).split('.')[0])
        dendrogram(linked, truncate_mode=global_values.TRUNCATE_MODE,
                   p=global_values.P, labels=label_array, orientation=global_values.ORIENTATION)
        plt.savefig(self.make_file_name())


