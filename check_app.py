programming_language_packages = {
    # Programming Languages
    "node" : "nodejs",
    "nodejs": "nodejs",
    "java": "default-jdk",
    "python3": "python3",
    "python2": "python",
    "ruby": "ruby",
    "perl": "perl",
    "php": "php",
    "go": "golang-go",
    "rust": "rustc",
    "swift": "swift",
    "typescript": "typescript",
    "kotlin": "kotlin",
    "scala": "scala",
    "haskell": "haskell-platform",
    "r": "r-base",
    "lua": "lua5.3",
    "javascript": "nodejs",
    # Databases
    "mysql": "mysql-server",
    "postgresql": "postgresql",
    "mongodb": "mongodb",
    "sqlite": "sqlite3",
    "redis": "redis-server",
    # Additional tools
    "docker": "docker-ce",
    "docker-compose": "docker-compose",
    "vagrant": "vagrant",
    "git": "git",
    "svn": "subversion",
    "hg": "mercurial",
    "emacs": "emacs",
    "vim": "vim",
    "make": "make",
    "clang-format": "clang-format",
    "uncrustify": "uncrustify",
    "npm": "npm",
    "pip": "python3-pip",
    "gem": "rubygems",
    "gdb": "gdb",
    "valgrind": "valgrind",
    "curl": "curl",
    "wget": "wget",
    "doxygen": "doxygen",
}
ide_packages = {
    # JetBrains IDEs
    "pycharm": "pycharm-community",
    "intellij": "intellij-idea-community",
    "clion": "clion",
    "webstorm": "webstorm",
    "phpstorm": "phpstorm",
    "rider": "rider",
    "datagrip": "datagrip",
    "appcode": "appcode",
    "goland": "goland",
    "rubymine": "rubymine",
    "mps": "mps",
    # Other IDEs
    "vscode": "code",
    "eclipse": "eclipse",
    "atom": "atom",
    "sublime-text": "sublime-text",
    "netbeans": "netbeans",
    "gedit": "gedit",
    "brackets": "brackets",
    "geany": "geany",
    "arduino-ide": "arduino-ide",
    "bluej": "bluej",
    "kdevelop": "kdevelop",
    # More IDEs
    "visual-studio": "visual-studio-code",
    "codeblocks": "codeblocks",
    "emacs": "emacs",
    "vim": "vim",
    "jupyter-notebook": "jupyter-notebook",
    "qt-creator": "qt-creator",
    "xcode": "xcode",
    "android-studio": "android-studio",
    "netbeans": "netbeans",
    "oracle-sql-developer": "sqldeveloper",
    "intellij-idea-ultimate": "intellij-idea-ultimate",
    "android-studio": "android-studio",
    "visual-studio": "visual-studio",
    "netbeans": "netbeans",
    "eclipse-jdt": "eclipse-jdt",
    "eclipse-cdt": "eclipse-cdt",
    "phpstorm": "phpstorm",
    "android-studio": "android-studio",
    "netbeans": "netbeans",
    "eclipse-jdt": "eclipse-jdt",
    "eclipse-cdt": "eclipse-cdt",
    "phpstorm": "phpstorm",
}
browser_packages = {
    "chrome": "google-chrome-stable",
    "chromium": "chromium-browser",
    "edge": "microsoft-edge-dev",
    "firefox": "firefox",
    "opera": "opera-stable",
    "brave": "brave-browser",
    "vivaldi": "vivaldi-stable",
    "safari": "safari",
    "tor": "tor-browser",
    "epiphany": "epiphany-browser",
    "midori": "midori",
}
import subprocess
import shutil

def is_package_installed(package_name):
    # Check using apt
    try:
        result = subprocess.run(['apt', 'list', '--installed', package_name], capture_output=True, text=True, check=True)
        if package_name in result.stdout:
            return True
    except subprocess.CalledProcessError as e:
        pass

    # Check using dpkg
    try:
        result = subprocess.run(['dpkg-query', '-W', '-f=${Status}', package_name], capture_output=True, text=True)
        if "install ok installed" in result.stdout:
            return True
    except subprocess.CalledProcessError as e:
        pass

    # Check if the package executable is in the system's PATH
    return shutil.which(package_name) is not None

def get_package_version(package_name):
    # Try to get package version using dpkg-query
    try:
        result = subprocess.run(['dpkg-query', '-W', '-f=${Version}', package_name], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pass

    #try to get package version using apt-cache
    try:
        result = subprocess.run(['apt-cache', 'policy', package_name], capture_output=True, text=True, check=True)
        for line in result.stdout.split('\n'):
            if line.strip().startswith("Installed:"):
                return line.strip().split(":")[1].strip()
    except subprocess.CalledProcessError as e:
        pass

    return "Version information not available"

def check_installed(app_name):
    if app_name in browser_packages:
        package_name = browser_packages[app_name]
        app_type = "browser"
    elif app_name in ide_packages:
        package_name = ide_packages[app_name]
        app_type = "IDE"
    elif app_name in programming_language_packages:
        package_name = programming_language_packages[app_name]
        app_type =  "programminglang"
    else:
        print("Others app", app_name)
        if is_package_installed(app_name):
            print(f"{app_name.capitalize()} is installed.")
            print(f"Version: {get_package_version(app_name)}")
        else:
            print(f"{app_name.capitalize()} is not installed.")
        return

    if is_package_installed(package_name):
        print(f"{app_name.capitalize()} is installed.")
        print(f"Version: {get_package_version(package_name)}")
    else:
        print(f"{app_name.capitalize()} is not installed.")


def get_installed_packages():
    installed_packages = []
    try:
        # Run dpkg-query command to get the list of installed packages with their versions
        result = subprocess.run(['dpkg-query', '-W', '-f=${binary:Package} ${Version}\n'], capture_output=True, text=True, check=True)
        # Split the output into lines
        lines = result.stdout.splitlines()
        for line in lines:
            # Split each line into package name and version
            package_info = line.split()
            if len(package_info) == 2:
                package_name, package_version = package_info
                # Append package name and version to the list
                installed_packages.append((package_name, package_version))
    except subprocess.CalledProcessError as e:
        print("Error:", e)
    return installed_packages





while 1:
    app_to_check = input("Enter the name of the application to check: ").lower()
    if app_to_check ==  "1" :
        installed_packages = get_installed_packages()
        for package, version in installed_packages:
            print(package, version)

    else : 
        check_installed(app_to_check)
