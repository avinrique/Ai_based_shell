# import cv2
# import cvlib as cv
# from cvlib.object_detection import draw_bbox
# video = cv2.VideoCapture('/dev/video0')
# labels = []
# while True :
#     ret , frame = video.read()
#     bbox , label , conf = cv.detect_common_objects(frame)
#     output_image =  draw_bbox(frame, bbox , label, conf)

#     for item in label:
#         if item in labels :
#             pass
#         else :
#             labels.append(item)
    
#     cv2.imshow('Object Detection',output_image )
#     if cv2.waitKey(1) & 0xFF == ord("q") :
#         break
# print(labels)
import subprocess

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

installed_packages = get_installed_packages()

for package, version in installed_packages:
    print(package, version)


import subprocess

def get_package_version(package_name):
    try:
        # Run dpkg-query command to get the version of the package
        result = subprocess.run(['dpkg-query', '-W', '-f=${Version}', package_name], capture_output=True, text=True)
        # Check the output to see if the package is installed
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

def is_package_installed(package_name):
    try:
        # Run dpkg-query command to check if the package is installed
        result = subprocess.run(['dpkg-query', '-W', '-f=${Status}', package_name], capture_output=True, text=True)
        # Check the output to see if the package is installed
        if "install ok installed" in result.stdout:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return False

# Take input from the user
package_name = input("Enter the package name: ")

if is_package_installed(package_name):
    version = get_package_version(package_name)
    print(f"{package_name} is installed. Version: {version}")
else:
    print(f"{package_name} is not installed.")
