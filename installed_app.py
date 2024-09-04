import subprocess
import webbrowser

def check_apt(package_name):
    try:
        subprocess.run(['apt', 'show', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def check_snap(package_name):
    try:
        subprocess.run(['snap', 'info', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def install_with_apt(package_name):
    try:
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', package_name], check=True)
        print(f"{package_name} installed successfully using APT.")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name} using APT.")
        return False
def install_with_snap(package_name):
    try:
        subprocess.run(['sudo', 'snap', 'install', package_name], check=True)
        print(f"{package_name} installed successfully using Snap Store.")
        return True
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            try:
                subprocess.run(['sudo', 'snap', 'install', package_name, '--classic'], check=True)
                print(f"{package_name} installed successfully using Snap Store (classic confinement).")
                return True
            except subprocess.CalledProcessError:
                print(f"Failed to install {package_name} using Snap Store (classic confinement).")
                return False
        else:
            print(f"Failed to install {package_name} using Snap Store.")
            return False


def install_from_web(package_name):
    query = package_name + " linux download"
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(search_url)
    print(f"Please download {package_name} from the web and follow the installation instructions.")

def install_application(package_name):
    if check_apt(package_name):
        if install_with_apt(package_name):
            return

    elif check_snap(package_name):
        if install_with_snap(package_name):
            return
    install_from_web(package_name)

# Example usage
app_to_install = input("Enter the name of the application to install: ")
install_application(app_to_install)
