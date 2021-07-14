from knownpaths import FOLDERID
import dearpygui.dearpygui as dpg
import re
import pafy
from moviepy.editor import *
import os
from my_mvLogger import myMvLogger
# from knownpaths import folderid
import knownpaths as kp

# create viewport takes in config options too!

primary_window = dpg.generate_uuid()


class YTDL:
    def __init__(self):
        self.video = None
        self.available_streams = []
        self.available_video_streams = []
        self.available_audio_streams = []
        self.file_path = None
        self.file_path_text_widget = None
        self.video_quality_list = []
        self.audio_quality_list = []
        self.video_element_selected_index = None
        self.audio_element_selected_index = None

        self.video_title = ''
        self.audio_title = ''
        self.video_extension = None
        self.audio_extension = None

        self.video_url = None
        self.audio_url = None

        self.video_quality_listbox_id = dpg.generate_uuid()
        self.audio_quality_listbox_id = dpg.generate_uuid()

        self.url_input_text_id = dpg.generate_uuid()

        self.logger = None
        # self.logger = myMvLogger(0, dpg.get_item_height(
        # item=primary_window), 'Log information', width=dpg.get_item_width(item=primary_window), height=500)

    def select_audio_stream_quality(self, sender, user_data):
        audio_re = re.search('audio:(.*)@', user_data)
        self.audio_extension = audio_re.group(1)
        self.logger.log_info(f'Audio Extension: {self.audio_extension}')
        temp_available_audio_stream_str = [
            str(x) for x in self.available_audio_streams]
        self.audio_element_selected_index = temp_available_audio_stream_str.index(
            user_data)
        self.audio_url = self.available_audio_streams[self.audio_element_selected_index].url

    def select_video_stream_quality(self, sender, user_data):
        video_re = re.search('video:(.*)@', user_data)
        self.video_extension = video_re.group(1)
        self.logger.log_info(f'Video Extension: {self.video_extension}')
        temp_available_video_stream_str = [
            str(x) for x in self.available_video_streams]
        self.video_element_selected_index = temp_available_video_stream_str.index(
            user_data)
        self.video_url = self.available_video_streams[self.video_element_selected_index].url

    def get_video_info(self):
        url = str(dpg.get_value(self.url_input_text_id))
        print(url)
        self.video = pafy.new(url=url)
        # check if title has ':' or '|' or both;
        # if they do, then replace those characters with and '_'
        self.video_title = str(self.video.title)
        if ':' in str(self.video.title) or '|' in str(self.video.title) or ':' and '|' in str(self.video.title):
            # self.audio_title = str(self.video.title)
            self.video_title = self.video_title.replace(':', '_')
            self.audio_title = self.video_title.replace(':', '_')
            self.video_title = self.video_title.replace('|', '_')
            self.audio_title = self.video_title.replace('|', '_')
            print(self.video_title)
        # self.allstreams = self.video.allstreams
        self.available_video_streams = [
            (x) for x in self.video.allstreams if 'video' in str(x)]
        self.logger.log_info(str(self.available_video_streams))
        # self.logger.log(str(self.available_video_streams))
        # AUDIO
        self.available_audio_streams = [
            x for x in self.video.allstreams if 'audio' in str(x)]
        self.logger.log_info(str(self.available_audio_streams))
        # print(str(self.available_video_streams))
        dpg.configure_item(item=self.video_quality_list,
                           items=self.available_video_streams, callback=self.select_video_stream_quality, user_data='USER_DATA')
        dpg.configure_item(item=self.audio_quality_list,
                           items=self.available_audio_streams, callback=self.select_audio_stream_quality, user_data='USER_DATA')

    def merge_video_and_audio(self):
        ffmpeg_tools.ffmpeg_merge_video_audio(
            video=f'{str(self.file_path)}\{str(self.video_title)}-a.{str(self.video_extension)}', audio=f'{str(self.file_path)}\{str(self.video_title)}-v.{str(self.audio_extension)}', output=f'{str(self.file_path)}\{str(self.video_title)}.{str(self.video_extension)}', vcodec='copy', acodec='copy')

    def cleanup_files(self):
        os.remove(
            f'{self.file_path}\{self.video_title}-v.{self.video_extension}')
        os.remove(
            f'{self.file_path}\{self.video_title}-a.{self.audio_extension}')

    def output_folder(self, sender, app_data, user_data):
        self.file_path = app_data['file_path_name']
        dpg.configure_item(item=self.file_path_text_widget,
                           default_value=f'{self.file_path}')
        print(self.file_path)

    def download_files(self):
        self.logger.log_debug(f'Video_title: {self.video_title}')

        self.logger.log_info('Downloading Audio Please Wait....')
        self.logger.log_debug(
            f'VIDEO: {self.video_title}.{self.video_extension}')

        self.available_audio_streams[self.audio_element_selected_index].download(
            quiet=False, filepath=f'{self.file_path}\{self.video_title}-a.{self.audio_extension}')
        # print(self.audio_url)

        self.logger.log_info('Downloading Video Please Wait....')
        self.logger.log_debug(
            f'Audio: {self.video_title}.{self.audio_extension}')
        self.logger.log_debug(
            f'{self.video_url}')
        # print(self.video_url)
        self.available_video_streams[self.video_element_selected_index].download(
            quiet=False, filepath=f'{str(self.file_path)}\{str(self.video_title)}-v.{str(self.video_extension)}')

        self.logger.log_info('Merging Audio and Video; Please wait....')
        self.merge_video_and_audio()
        self.logger.log_info('Removing Temp Files....')
        self.cleanup_files()
        self.logger.log_info('Done')
        os.startfile(self.file_path)


folder_id = getattr(FOLDERID, 'Downloads')
# print(kp.get_path(folderid=folder_id))
vp = dpg.create_viewport(title='Youtube-DL', width=750, height=750)
yt = YTDL()
file_dialog = dpg.add_file_dialog(directory_selector=True, default_path=(kp.get_path(folderid=folder_id)),
                                  show=False, callback=yt.output_folder, width=300, height=400, label='Select an output directory')


with dpg.window(label="Example Window", width=750, no_title_bar=True, height=200, id=primary_window, no_move=True, no_resize=True):
    dpg.set_primary_window(primary_window, False)

    with dpg.group(label="InputGroup", width=300):
        dpg.add_text(default_value='Download Youtube Videos')
        dpg.add_input_text(label='Enter URL Here',
                           id=yt.url_input_text_id, callback=yt.get_video_info)
        dpg.add_button(label='Select output folder',
                       callback=lambda: dpg.show_item(file_dialog))
        dpg.add_same_line()
        yt.file_path_text_widget = dpg.add_text(
            default_value=f'{yt.file_path}')
    dpg.add_spacing()
    dpg.add_separator()
    dpg.add_spacing()

    with dpg.group(label='QualityGroup', width=300):

        yt.video_quality_list = dpg.add_combo(
            label='Video Qualities', items=yt.available_video_streams, show=True, id=yt.video_quality_listbox_id)
        yt.audio_quality_list = dpg.add_combo(
            label='Audio Qualities', items=yt.available_audio_streams, show=True, id=yt.audio_quality_listbox_id)

    dpg.add_spacing()
    dpg.add_separator()
    dpg.add_spacing()
    yt.logger = myMvLogger(0, dpg.get_item_height(item=primary_window),
                           'Log information', width=dpg.get_item_width(item=primary_window), height=500, no_move=True, no_resize=False)

    dpg.add_button(label="Download", callback=yt.download_files,
                   user_data=yt.logger)

    # with dpg.window(label='TestWindow', width=300) as nested_window:
    #     with dpg.tab_bar(label='tb1'):
    #         with dpg.tab(label='t1'):
    #             dpg.add_text('Gloood')
    #             dpg.add_child(label='Test Child')
    #             dpg_logger.mvLogger()
    #         # dpg_logger.mvLogger()
    # logger = dpg_logger.mvLogger().log('Te')

    # dpg.set_item_pos(item=logger, pos=[
    #                  0, dpg.get_item_height(item=primary_window)])
    # dpg.get_item_pos()
    # with dpg_logger.mvLogger():


dpg.setup_dearpygui(viewport=vp)
dpg.show_viewport(vp)
dpg.start_dearpygui()
# https://www.youtube.com/watch?v=5mm_gdnOxpU
