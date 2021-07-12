import dearpygui.dearpygui as dpg
import dearpygui.logger as dpg_logger

logger = dpg_logger.mvLogger()
logger.log("This is my logger. Just like an onion it has many levels.")


def log_things(sender, app_data, user_data):
    user_data.log("We can log to a trace level.")
    user_data.log_debug("We can log to a debug level.")
    user_data.log_info("We can log to an info level.")
    user_data.log_warning("We can log to a warning level.")
    user_data.log_error("We can log to a error level.")
    user_data.log_critical("We can log to a critical level.")


def set_level(sender, app_data, user_data):
    # changing the logger level will ignore any log messages below the set level
    logger = user_data[0]
    level_options = user_data[1]
    logger.log_level = (level_options[dpg.get_value(sender)])

    # we do this so we can see the set level effect
    log_things(sender, app_data, logger)


with dpg.window():
    dpg.add_button(label="Log to logger",
                   callback=log_things, user_data=logger)
    level_options = {"Trace": 0, "Debug": 1, "Info": 2,
                     "Warning": 3, "Error": 4, "Critical": 5}
    dpg.add_radio_button(list(level_options.keys()),
                         callback=set_level, user_data=[logger, level_options])

dpg.start_dearpygui()
