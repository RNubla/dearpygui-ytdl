import dearpygui.dearpygui as dpg
import dearpygui.logger as dpg_logger
import dearpygui.demo as dpgd
import pafy
import os
import re
from moviepy.editor import *
import ffmpeg


class MainApp:
    def __init__(self):
        viewport = dpg.create_viewport()
        dpg.set_viewport_title(title='YoutubeDL')
        dpg.setup_dearpygui(viewport=viewport)
        dpg.show_viewport(viewport=viewport, maximized=False)
        # dpg.
        dpgd.show_demo()

        self.video = None
        self.available_streams = []
        self.available_video_streams = []
        self.available_audio_streams = []
        # self.allstreams = None
        self.file_path_name = None
        self.logger = dpg_logger.mvLogger()
        self.logger.log('Test Log')
        self.video_quality_list = None
        self.audio_quality_list = None
        self.video_element_selected_index = None
        self.audio_element_selected_index = None
        self.file_path_text = None

        self.video_title = ''
        self.audio_title = ''
        self.video_extension = None
        self.video_extension_re = None
        self.audio_extension = None
        self.audio_extension_re = None

        self.video_quality_listbox_id = dpg.generate_uuid()
        self.audio_quality_listbox_id = dpg.generate_uuid()
        self.url_input_text_id = dpg.generate_uuid()
        self.file_dialog_id = dpg.add_file_dialog(
            directory_selector=True, show=False, callback=self.output_folder)

    def select_audio_stream_quality(self, sender, user_data):
        # print(user_data)
        self.audio_extension_re = re.search('audio:(.*)@', user_data)
        self.audio_extension = self.audio_extension_re.group(1)
        # print(self.audio_extension.group(1))
        self.logger.log_info(
            f'Audio Extension: {self.audio_extension}')
        temp_available_audio_stream_str = [
            str(x) for x in self.available_audio_streams]
        self.audio_element_selected_index = temp_available_audio_stream_str.index(
            user_data)

    def select_video_stream_quality(self, sender, user_data):
        # print(user_data)
        self.video_extension_re = re.search('video:(.*)@', user_data)
        self.video_extension = self.video_extension_re.group(1)
        self.logger.log_info(
            f'Video Extension: {self.video_extension}')
        temp_available_video_stream_str = [
            str(x) for x in self.available_video_streams]
        # print(temp_available_video_stream_str)
        self.video_element_selected_index = temp_available_video_stream_str.index(
            user_data)

    def get_video_info(self):
        url = str(dpg.get_value(self.url_input_text_id))
        self.video = pafy.new(url=url)
        # self.allstreams = self.video.allstreams
        self.available_video_streams = [
            (x) for x in self.video.allstreams if 'video' in str(x)]
        self.logger.log(str(self.available_video_streams))
        # AUDIO
        self.available_audio_streams = [
            x for x in self.video.allstreams if 'audio' in str(x)]
        self.logger.log_info(str(self.available_audio_streams))
        # print(str(self.available_video_streams))
        dpg.configure_item(item=self.video_quality_list,
                           items=self.available_video_streams, callback=self.select_video_stream_quality, user_data='USER_DATA')
        dpg.configure_item(item=self.audio_quality_list,
                           items=self.available_audio_streams, callback=self.select_audio_stream_quality, user_data='USER_DATA')

    def download(self):
        # print(dpg.get_value(self.url_input_text_id))
        # self.logger.log(str(self.allstreams[self.element_selected_index].download(quiet=False,
        #                                                                           filepath=self.file_path_name)))

        # self.logger.log_info(str(self.available_video_streams[self.element_selected_index].download(quiet=False,
        #                                                                                             filepath=self.file_path_name)))
        self.logger.log_info('Downloading Video Please Wait....')
        self.available_video_streams[self.video_element_selected_index].download(
            quiet=False, filepath=self.file_path_name)
        self.logger.log_info('Downloading Audio Please Wait....')
        self.available_audio_streams[self.audio_element_selected_index].download(
            quiet=False, filepath=self.file_path_name)
        self.logger.log_info('Merging Audio and Video; Please wait....')
        self.merge_video_and_audio()
        self.logger.log_info('Removing Temp Files....')
        self.cleanup_files()
        os.startfile(self.file_path_name)

    def merge_video_and_audio(self):
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
        clip = ffmpeg.input(
            f'{str(self.file_path_name)}\{str(self.video_title)}.{str(self.video_extension)}')
        audio = ffmpeg.input(
            f'{str(self.file_path_name)}\{str(self.video_title)}.{str(self.audio_extension)}')
        # ffmpeg.output(
        #     clip, audio, f'{str(self.file_path_name)}\Combined-{str(self.video_title)}.{str(self.video_extension)}', vcodec='copy')
        clip = VideoFileClip(
            f'{str(self.file_path_name)}\{str(self.video_title)}.{str(self.video_extension)}')
        audio = AudioFileClip(
            f'{str(self.file_path_name)}\{str(self.video_title)}.{str(self.audio_extension)}')
        video_clip = clip.set_audio(audio)
        # Save video to folder
        video_clip.write_videofile(
            f'{str(self.file_path_name)}\Combined-{str(self.video_title)}.{str(self.video_extension)}', codec='libvpx')

    def cleanup_files(self):
        os.remove(
            f'{self.file_path_name}\{self.video_title}.{self.video_extension}')
        os.remove(
            f'{self.file_path_name}\{self.video_title}.{self.audio_extension}')

    def output_folder(self, sender, app_data, user_data):
        self.file_path_name = app_data['file_path_name']
        dpg.configure_item(item=self.file_path_text,
                           default_value=f'{self.file_path_name}')
        print(self.file_path_name)

    def demoWindow(self):
        with dpg.window(label='Youtube-DL', width=400, height=300):
            with dpg.group(label="InputGroup"):
                dpg.add_text(default_value="Enter video url")
                dpg.add_input_text(label="URL Goes Here",
                                   id=self.url_input_text_id, callback=self.get_video_info)
                dpg.add_button(label='Select output folder',
                               callback=lambda: dpg.show_item(self.file_dialog_id))
                dpg.add_same_line()
                self.file_path_text = dpg.add_text(
                    default_value=f'{self.file_path_name}')

            dpg.add_spacing()
            dpg.add_separator()
            dpg.add_spacing()

            # dpg.add_button(label="Fetch Information",
            #                callback=self.get_video_info)
            with dpg.group(label="QualityGroup", width=100):
                self.video_quality_list = dpg.add_combo(label='Video Qualities',
                                                        items=self.available_video_streams, show=True, id=self.video_quality_listbox_id)
                self.audio_quality_list = dpg.add_combo(label='Audio Qualities',
                                                        items=self.available_audio_streams, show=True, id=self.audio_quality_listbox_id)
            dpg.add_same_line()
            with dpg.group(label="RadioGroup"):
                dpg.add_radio_button(label="Select One", items=[
                                     'Video Only', 'Audio Only'])
            dpg.add_spacing()
            dpg.add_separator()
            dpg.add_spacing()

            dpg.add_button(label="Download",
                           callback=self.download, user_data=self.logger)
        # dpg.set_primary_window(self.demoWindow, True)


if __name__ == '__main__':
    app = MainApp()
    app.demoWindow()
    while (dpg.is_dearpygui_running()):
        dpg.render_dearpygui_frame()
    dpg.cleanup_dearpygui()
