import subprocess
import os
import sys
import re
import platform
import google.generativeai as genai

def check_os():
    system = platform.system()
    if system == "Windows":
        return "windows Powershell"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macOs"
    else:
        print("Unknown operating system")

System_OS = check_os()

genai.configure(api_key="AIzaSyAlSRMwkkHtlsNkZJHrdjXRvD4zJdOsLKI")

# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)




def errors_handler_and_verifyer(command , prompt ) :
            try:
                if System_OS == "windows Powershell":
                    rancomd = subprocess.run(['powershell', '-Command', c.text], stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE, text=True, check=True)
                elif System_OS == "linux" or System_OS == "macOs":
                    rancomd = subprocess.run(c.text, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    print("OS could not be determined, exiting the program.")
                    sys.exit(1)
                
                return {rancomd.stdout.decode('utf-8')}
               
            
            except subprocess.CalledProcessError as e:
                
                print(f"The Error is: {e}")

                check_error = model.generate_content(f"Here is the error code for the command that was performed in {System_OS}. "
                                                        f"Check what's wrong with it and provide commands to solve it. "
                                                      #  f"If input is required by that command from the user, add '--required-user-input' at the end of your response. "
                                                        f"The error is '{e}', the command was '{c.text}'. "
                                                        f"For more info, the current directory is '{os.getcwd()}'. "
                                                      #  f"Please provide the steps in a JSON format.
                                                        f"")
                #check for errors
                print(check_error.text)
                def write_to_file(file_path, content):

                    with open(file_path, 'a') as file:
                        file.write(content)
                
                write_to_file('verifying_cerrors.txt' , check_error.text)





model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
chat2 = model.start_chat(history=[])

chat.send_message(""" Hey i am aAbhinav Gupta and my skills are 
                    Programming and Development:

                    Python
                    JavaScript (including Node.js and web development)
                    PowerShell and Bash scripting
                    Familiarity with ES6 modules
                    Artificial Intelligence and Automation:

                    Experience with large language models (LLMs)
                    Development of automation systems (e.g., 'autogen')
                    Knowledge of generative AI applications
                    Robotics and Hardware:

                    Building robotic arms
                    Working with microcontrollers (e.g., ESP8266, Raspberry Pi)
                    Experience with RF communication
                    Computer Vision:

                    Using OpenCV with Arducam TOF camera
                    Database Management:

                    Understanding of databases, ER diagrams, normalization, and SQL operations
                    Web Development:

                    Building and managing e-commerce websites
                    Implementing features like language toggles and cart functionality
                    Cybersecurity:

                    Knowledge of ethical hacking and vulnerability assessment
                    Collaboration and Project Management:

                    Experience in developing projects focused on real-time collaboration and task management                   """)

while True:
    cmdin = input("Enter the prompt ")
    a = chat.send_message(f"""Suppose you are an ai agent that converts the given prompt into a {System_OS} command that can be directly executed, you have to take the prompt and convert it into a command so that i can paste your response and get my results , the prompt is {cmdin} , also your current directory is {os.getcwd()}. and you also have my details like myb name and things """ , safety_settings={'HARASSMENT':'block_none', 'HARM_CATEGORY_DANGEROUS_CONTENT' : 'block_none' ,'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})

    c = model.generate_content(f"""Suppose you are an ai agent that converts the given prompt into a {System_OS} command that can be directly executed, now check if there is extra anything other than command then remove it there, just keep the command ,the command is {a.text}""")
    
    b = model.generate_content(f"""Now check the command if its a {System_OS} command and if its the right command or not if yes response with 'yes' else resposnse with 'no'  , the command is {c.text}""")

    if b.text.lower() == "yes":
        check_before_exec = input(f"Are you sure you want to run this command?\n'{c.text}'\n1. Yes\n2. No\nDefault = Yes\n")
        
                         # if not check_before_exec or check_before_exec.lower() == "yes":
        if "yes" == "yes":
            
            try:
                if System_OS == "windows Powershell":
                    rancomd = subprocess.run(['powershell', '-Command', c.text], stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE, text=True, check=True)
                elif System_OS == "linux" or System_OS == "macOs":
                    rancomd = subprocess.run(c.text, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    print("OS could not be determined, exiting the program.")
                    sys.exit(1)
                print(f"The results are:\n{rancomd.stdout.decode('utf-8')}")
                if {rancomd.stdout.decode('utf-8')} == "" or {rancomd.stdout.decode('utf-8')} == None :
                
                    check_work = model.generate_content(f"""The command that ran in the {System_OS} was '{c.text}' "
                                                         f"and the output of that command was '{rancomd.stdout.decode('utf-8')}'. "
                                                         f"The error from the command was '{rancomd.stderr.decode('utf-8')}'. "
                                                         f"Now, I have run the command and don't know if it was successful. "
                                                         f"If there is a way to check if the given command has done its work or not, "
                                                         f"please provide that command or list of commands to verify.""")
                    print(check_work.text)
                    def write_to_file(file_path, content):
                        with open(file_path, 'w') as file:
                            file.write(content)
                    
                    write_to_file('verify_run.txt' , check_work.text)
                    count = 1

                    with open('verify_run.txt' , 'r') as f :
                        verify_cmd_content = f.read()
                    def verify_the_command(verify_cmd_list , prompt , count):
                        ver = chat2.send_message(f"""now their is the file that contains the commands to verify if the command given in the prompt ran sucessfully now you have to take the {count} command now just give me the {count} command that i can run directly in my console and get the output""")
                    # ver = chat2.send_message(f'now their is the file that contains the commands to verify if the command given in the prompt ran sucessfully now you have to take the {count} command and try to run and check if that verifies if the command in the prompt work sucessfully or not, here the  file is {verify_cmd_content} and the prompt command is {prompt} , if it verifies than response with `yes` else response with `no`  ')
                        print(ver)
                        if ver.text.lower() == "yes" :
                            count = 1
                            pass
                        else :
                            count+=1
                            verify_the_command(verify_cmd_content , c.text , count)

                    verify_the_command(verify_cmd_content , c.text ,count)


                    
            
            except subprocess.CalledProcessError as e:
                
                print(f"The Error is: {e}")

                check_error = model.generate_content(f"Here is the error code for the command that was performed in {System_OS}. "
                                                        f"Check what's wrong with it and provide commands to solve it. "
                                                      #  f"If input is required by that command from the user, add '--required-user-input' at the end of your response. "
                                                        f"The error is '{e}', the command was '{c.text}'. "
                                                        f"For more info, the current directory is '{os.getcwd()}'. "
                                                      #  f"Please provide the steps in a JSON format.
                                                        f"")
                print(check_error.text)

                def write_to_file(file_path, content):
                    with open(file_path, 'w') as file:
                        file.write(content)
                
                write_to_file('errors.txt' , check_error.text)


                def eradicate_errors_with_recurrsion_call(errorslist , prompt , error) :


                    pass
    
    else:
        print(b.text)
