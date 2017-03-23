import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import globals.global_values as global_values


class ScatterPlot:

    def __init__(self, cl, _dirs):
        '''
        init a scatter plot
        :param cl:  the list of colors
        :param _dirs: the dirs structure
        :param _type: the type of plot
        '''
        self.color_list = cl
        self.dirs = _dirs

    def make_file_name(self):
        '''
        create the correct filename for the scatter plot
        :return: the filename
        '''
        base_name = os.path.basename(self.dirs[0]).split('.')[0]
        d_name = '%s_%s_scatter.png' % (global_values.DISTANCE_TYPE, base_name)
        return  os.path.join(self.dirs[3], d_name)

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
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.savefig(self.make_file_name())


