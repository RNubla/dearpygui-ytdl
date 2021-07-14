import dearpygui.dearpygui as dpg

vp = dpg.create_viewport()
dpg.enable_docking(dock_space=True)

# Trying to dock these windows into the viewport / primary window just puts the window on top & not into the viewport window.
for i in range(4):
    with dpg.window(label=f"Window {i}", width=300, height=300, pos=[i*10+100, i*10+20]):
        dpg.add_text("Another window")

with dpg.window(label="Main Layout", no_background=True, no_bring_to_front_on_focus=True) as main_window:
    dpg.add_text("Primary Window")

dpg.setup_dearpygui(viewport=vp)
dpg.show_viewport(vp)

# Potential bug if you set the primary window the no_background is no longer observed
#dpg.set_primary_window(main_window, True)
dpg.start_dearpygui()
