
import dearpygui.dearpygui as dpg


def callback(sender, app_data, user_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)


with dpg.file_dialog(directory_selector=False, show=False, callback=callback) as file_dialog_id:
    dpg.add_file_extension(".*", color=(255, 255, 255, 255))
    dpg.add_file_extension(".cpp", color=(255, 255, 0, 255))
    dpg.add_file_extension(".h", color=(255, 0, 255, 255))
    dpg.add_file_extension(".py", color=(0, 255, 0, 255))

    dpg.add_button(label="fancy file dialog")
    with dpg.child():
        dpg.add_selectable(label="bookmark 1")
        dpg.add_selectable(label="bookmark 2")
        dpg.add_selectable(label="bookmark 3")

with dpg.window(label="Tutorial", width=800, height=300):
    dpg.add_button(label="File Selector",
                   callback=lambda: dpg.show_item(file_dialog_id))

dpg.start_dearpygui()
