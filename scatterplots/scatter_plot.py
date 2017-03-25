import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import globals.global_values as global_values


class ScatterPlot:

    def __init__(self, cl, _dirs, _is_agg):
        '''
        init a scatter plot
        :param cl:  the list of colors
        :param _dirs: the dirs structure
        :param _type: the type of plot
        '''
        self.color_list = cl
        self.dirs = _dirs
        self.is_agg = _is_agg

    def make_file_name(self):
        '''
        create the correct filename for the scatter plot
        :return: the filename
        '''
        if not self.is_agg:
            base_name = os.path.basename(self.dirs[0]).split('.')[0]
            d_name = '%s_scatter.png' % (base_name)
            return  os.path.join(self.dirs[3], d_name)
        else:
            return os.path.join(self.dirs[8], 'agg_scatter.png')

    def make_scatter_plot(self):
        '''
        make a scatter plot from the given figures
        :return: nothing
        '''
        # TODO: make correct labels
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        r = []
        g = []
        b = []
        for k, v in self.color_list.iteritems():
            ax.scatter(v[0], v[1], v[2], c='r', marker='.')
        if global_values.DISTANCE_TYPE == 'HSV':
            labels = global_values.HSV_SCATTER_LABELS
        elif global_values.DISTANCE_TYPE == 'LAB':
            labels = global_values.LAB_SCATTER_LABELS
        elif global_values.DISTANCE_TYPE == 'RGB':
            labels = global_values.RGB_SCATTER_LABELS
        else:
            labels = ['???', '???', '???']

        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.set_zlabel(labels[2])

        plt.savefig(self.make_file_name())
        plt.close()


