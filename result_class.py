__author__ = 'fire'
import global_values
import global_utils
import os
import re
class ImgResult:
    def __init__(self,gname):
        self.game_name = gname
        self.input_dir = global_utils.get_input_directory(self.game_name)
        self.output_dir = global_utils.get_output_directory(self.game_name)
        self.input_file_dict = self.generate_file_lists(global_values.INPUT_DIR)
        self.output_file_dict = self.generate_file_lists(global_values.OUTPUT_DIR)
        self.html_file = global_utils.build_html_file(self.game_name)
        self.file_handle = open(self.html_file, 'w+')
        self.agg_stats_file = global_utils.get_agg_color_stats_file(self.game_name)
        self.reg_stats_file = global_utils.get_individual_stats_file(self.game_name)
        self.build_html_file()
        self.file_handle.close()

    def generate_file_lists(self, folder):
        tmp = {}
        if folder == global_values.OUTPUT_DIR:
            for root, dirnames, filenames in os.walk(self.output_dir):
                for filename in filenames:
                    tmp[filename] = os.path.join(self.output_dir,filename)
            return tmp
        elif folder == global_values.INPUT_DIR:
            for root, dirnames, filenames in os.walk(self.input_dir):
                for filename in filenames:
                    tmp[filename] = os.path.join(self.input_dir,filename)
            return tmp
    def write_tag(self,tag,t,tab_lvl):
        if t == global_values.START_TAG:
            start = global_values.TAB * tab_lvl
            start += '<%s>\n' % (tag)
            self.file_handle.write(start)
        elif t == global_values.END_TAG:
            end = global_values.TAB * tab_lvl
            end += '</%s>\n' % (tag)
            self.file_handle.write(end)
    def write_to_fh_simple(self,tag,attr,data,tab_lvl,need_end):
        start_tag = '<%s' % (tag)
        if attr != {}:
            start_tag += ' '
        end_tag = '</%s>\n' % (tag)
        final_msg = global_values.TAB * tab_lvl + start_tag
        for key, value in attr.iteritems():
            tmp = '%s=\"%s\" ' % (key,value)
            final_msg += tmp
        if tag != 'img':
            final_msg += '>'
        else:
            final_msg += '/>'
        if data is not None:
            final_msg += data
        if need_end:
            final_msg += end_tag
        else:
            final_msg += '\n'
        self.file_handle.write(final_msg)
    def get_stats(self,agg,tab_lvl,name):
        if agg:
            fh_tmp = open(self.agg_stats_file, 'r')
            for line in fh_tmp.read().split('\n'):
                if len(line) > 1:
                    data = line.split(':=:')
                    to_write = '%s' % data[1]
                    self.write_to_fh_simple('p',{},to_write,5, True)
            fh_tmp.close()
        else:
            fh_tmp = open(self.reg_stats_file, 'r')
            for line in fh_tmp.read().split('\n'):
                 if len(line) > 1:
                    line_test = '[%s]' % (name[:-4])
                    if line_test in line:
                        data = line.split(':=:')
                        self.write_to_fh_simple('p',{},data[1],5, True)

    def build_html_file(self):
        self.file_handle.write('<!DOCTYPE html>\n')
        self.write_tag('html',global_values.START_TAG,0) # <html>
        self.write_tag('head',global_values.START_TAG,1) # <head>
        self.write_to_fh_simple('title',{},self.game_name,2, True) # <title>test</title>
        self.write_to_fh_simple('meta',{'charset':'utf-8'},None,2, False)
        self.write_to_fh_simple('meta',{'name':'viewport', 'content':'width=device-width, initial-scale=1'},None,2, False)
        self.write_to_fh_simple('link',{'rel':'stylesheet', 'href':global_values.BOOTSTRAP_CSS},None,2, False)
        self.write_to_fh_simple('link',{'rel':'stylesheet', 'href':global_values.STYLE_CSS},None,2, False)
        self.write_to_fh_simple('script',{'src':global_values.JQUERY_JS},None,2, True)
        self.write_to_fh_simple('script',{'src':global_values.SCRIPT_JS},None,2, True)
        self.write_tag('head',global_values.END_TAG,1) # </head>
        self.write_tag('body',global_values.START_TAG,1) # <body>
        self.write_to_fh_simple('div',{'class':'container'},None,2, False)
        self.write_to_fh_simple('div',{'class':'jumbotron'},None,3, False)
        self.write_to_fh_simple('h1',{},self.game_name,4, True)
        self.write_tag('div',global_values.END_TAG,3)
        self.write_to_fh_simple('div',{'class':'row'},None,3, False)
        self.write_to_fh_simple('div',{'class':'col-sm-12'},None,4, False)
        self.write_to_fh_simple('h2',{},'Aggregate Data',5, True)
        self.write_tag('div',global_values.END_TAG,4)
        self.write_tag('div',global_values.END_TAG,3) # 3 is main tab level!
        self.write_to_fh_simple('div',{'class':'row'},None,3, False)
        self.write_to_fh_simple('div',{'class':'col-sm-4'},None,4, False)
        self.write_to_fh_simple('h3',{},'Image',5, True)
        self.write_to_fh_simple('p',{},'N/A',5, True)
        self.write_tag('div',global_values.END_TAG,4)
        self.write_to_fh_simple('div',{'class':'col-sm-4'},None,4, False)
        self.write_to_fh_simple('h3',{},'Top Colors',5, True)
        self.write_to_fh_simple('img',{'src':'output_aggregate.png', 'class': 'img-limited'},None,5, False)
        self.write_tag('div',global_values.END_TAG,4)
        self.write_to_fh_simple('div',{'class':'col-sm-4'},None,4, False)
        self.write_to_fh_simple('h3',{},'Stats',5, True)
        self.get_stats(True,5,None)
        self.write_tag('div',global_values.END_TAG,4)
        self.write_tag('div',global_values.END_TAG,3)
        for key in self.input_file_dict.keys():
            self.write_to_fh_simple('div',{'class':'row'},None,3, False)
            self.write_to_fh_simple('div',{'class':'col-sm-12'},None,4, False)
            self.write_to_fh_simple('h2',{},key,5, True)
            self.write_tag('div',global_values.END_TAG,4)
            self.write_tag('div',global_values.END_TAG,3)
            self.write_to_fh_simple('div',{'class':'row'},None,3, False)
            self.write_to_fh_simple('div',{'class':'col-sm-4'},None,4, False)
            self.write_to_fh_simple('h3',{},'Image',5, True)
            src_input = os.path.join('input', key)
            self.write_to_fh_simple('img',{'src':src_input, 'class': 'img-limited'},None,5, False)
            self.write_tag('div',global_values.END_TAG,4)
            self.write_to_fh_simple('div',{'class':'col-sm-4'},None,4, False)
            self.write_to_fh_simple('h3',{},'Top Colors',5, True)
            src_top_color = os.path.join('output',key)
            self.write_to_fh_simple('img',{'src':src_top_color, 'class': 'img-limited'},None,5, False)
            self.write_tag('div',global_values.END_TAG,4)
            self.write_to_fh_simple('div',{'class':'col-sm-4'},None,4, False)
            self.write_to_fh_simple('h3',{},'Stats',5, True)
            self.get_stats(False,5,key)
            self.write_tag('div',global_values.END_TAG,4)
            self.write_tag('div',global_values.END_TAG,3)
        self.write_tag('div',global_values.END_TAG,4)
        self.write_tag('div',global_values.END_TAG,3)
        self.write_tag('div',global_values.END_TAG,2)
        self.write_tag('body',global_values.END_TAG,1)
        self.write_tag('html',global_values.END_TAG,0)




