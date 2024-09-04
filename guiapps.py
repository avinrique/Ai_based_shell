import subprocess

def get_running_gui_apps():
    process = subprocess.Popen(['wmctrl', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    windows = stdout.decode().split('\n')

    gui_apps = []
    for window in windows:
        if window:
            win_id = window.split()[0]
            process = subprocess.Popen(['xprop', '-id', win_id, '_NET_WM_WINDOW_TYPE', 'WM_CLASS'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = process.communicate()
            output = stdout.decode()

            if '_NET_WM_WINDOW_TYPE_NORMAL' in output:  # check if the window is a normal window
                app_name = output.split()[-1].strip('"')
                gui_apps.append(app_name)

    return gui_apps

print("Running GUI Applications:")
print(get_running_gui_apps())
