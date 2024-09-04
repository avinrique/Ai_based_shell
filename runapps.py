# import psutil

# def list_running_apps():
#     running_apps = []
#     for proc in psutil.process_iter(['pid', 'name']):
#         try:
#             # Fetch process details (name) and append to the list
#             proc_info = proc.info
#             app_name = proc_info['name']
#             running_apps.append(app_name)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return running_apps

# if __name__ == "__main__":
#     running_apps = list_running_apps()
#     print("Currently running applications:")
#     for app in running_apps:
#         print(app)



# import psutil

# def is_system_app(proc_path):
#     if proc_path is None:
#         return False
#     # Define system directories
#     system_dirs = ['/bin', '/usr/bin', '/sbin', '/usr/sbin']
#     # Check if the process path is in system directories
#     return any(proc_path.startswith(dir) for dir in system_dirs)

# def list_running_apps():
#     running_apps = {'system': [], 'user': []}
#     for proc in psutil.process_iter(['pid', 'name', 'exe']):
#         try:
#             # Fetch process details and check if it's a system app or user app
#             proc_info = proc.info
#             app_name = proc_info['name']
#             app_path = proc_info['exe']
#             if is_system_app(app_path):
#                 running_apps['system'].append(app_name)
#             else:
#                 running_apps['user'].append(app_name)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return running_apps

# if __name__ == "__main__":
#     running_apps = list_running_apps()
#     print("System applications:")
#     for app in running_apps['system']:
#         print(app , "----------\n")
    
#     print("\nUser applications:")
#     for app in running_apps['user']:
#         print(app)


# import psutil

# def is_system_app(proc_path):
#     # Define system directories
#     system_dirs = ['/bin', '/usr/bin', '/sbin', '/usr/sbin', '/lib', '/usr/lib', '/lib64', '/usr/lib64']
#     # Check if the process path is in system directories
#     return any(proc_path.startswith(dir) for dir in system_dirs)

# def list_running_apps():
#     running_apps = {'system': [], 'user': []}
#     for proc in psutil.process_iter(['pid', 'name', 'exe', 'username']):
#         try:
#             # Fetch process details and check if it's a system app or user app
#             proc_info = proc.info
#             app_name = proc_info['name']
#             app_path = proc_info['exe']
#             username = proc_info['username']
#             if is_system_app(app_path) or username == 'root':
#                 running_apps['system'].append(app_name)
#             else:
#                 running_apps['user'].append(app_name)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return running_apps

# if __name__ == "__main__":
#     running_apps = list_running_apps()
#     print("System applications:")
#     for app in running_apps['system']:
#     #   print(app)
#         pass
#     print("\nUser applications:")
#     for app in running_apps['user']:
#         print(app)





import psutil

def is_system_app(cmdline):
    # Define system directories
    system_dirs = ['/bin/', '/usr/bin/', '/sbin/', '/usr/sbin/', '/lib/', '/usr/lib/', '/lib64/', '/usr/lib64/']
    # Check if the process command line starts with system directories
    return cmdline and any(cmdline[0].startswith(dir) for dir in system_dirs)

def list_running_apps():
    running_apps = {'system': [], 'user': []}
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username']):
        try:
            # Fetch process details and check if it's a system app or user app
            proc_info = proc.info
            app_name = proc_info['name']
            cmdline = proc_info['cmdline']
            username = proc_info['username']
            if is_system_app(cmdline) or username == 'root':
                running_apps['system'].append(app_name)
            else:
                running_apps['user'].append(app_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return running_apps

if __name__ == "__main__":
    running_apps = list_running_apps()
    print("System applications:")
    for app in running_apps['system']:
        print(app)
    
    print("\nUser applications:")
    for app in running_apps['user']:
        print(app)
