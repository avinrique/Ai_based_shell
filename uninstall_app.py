import subprocess

def uninstall_with_apt(package_name):
    try:
        subprocess.run(['sudo', 'apt', 'remove', '--purge', package_name], check=True)
        print(f"{package_name} uninstalled successfully using APT.")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to uninstall {package_name} using APT.")
        return False

def uninstall_with_snap(package_name):
    try:
        subprocess.run(['sudo', 'snap', 'remove', package_name], check=True)
        print(f"{package_name} uninstalled successfully using Snap Store.")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to uninstall {package_name} using Snap Store.")
        return False

def uninstall_with_dpkg(package_name):
    try:
        subprocess.run(['sudo', 'dpkg', '--remove', package_name], check=True)
        print(f"{package_name} uninstalled successfully using dpkg.")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to uninstall {package_name} using dpkg.")
        return False

def uninstall_application(package_name):
    if uninstall_with_apt(package_name):
        return
    elif uninstall_with_snap(package_name):
        return
    elif uninstall_with_dpkg(package_name):
        return
    else:
        print(f"Uninstallation method not found for {package_name}. Please manually uninstall.")

# Example usage
app_to_uninstall = input("Enter the name of the application to uninstall: ")
uninstall_application(app_to_uninstall)
