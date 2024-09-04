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
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(model.name)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
chat.send_message("""You are an intelligent assistant named 'Vain,' designed to automate operating system tasks on my behalf. Your primary role is to understand my instructions and execute them efficiently, using your capabilities to break down complex tasks, generate actionable commands, and perform operations directly on the OS. You are aware that your purpose is to help me by interpreting natural language prompts, converting them into executable commands, and ensuring that all tasks are completed as per my requirements. You should always strive to perform tasks accurately, efficiently, and with the utmost reliability.""")


while True:
    cmd_input = input("Enter the command: ")
    task_prompt = f"""
    You are an intelligent assistant that can understand natural language prompts. 
    Your job is to break down the given prompt into smaller, actionable tasks that can be performed on a {System_OS} system. 
    Identify sentences or phrases that describe specific actions or commands. 
    Please exclude any irrelevant information or context that doesn't lead to actionable tasks. 
    Return the tasks in a clear and concise list format.
    The input prompt is: "{cmd_input}"
    """

    tasks_response = model.generate_content(task_prompt, safety_settings={'HARASSMENT': 'block_none', 'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
    print(tasks_response.text , "\n\n-----------------------------------------------------------------------------------------------------------------------\n\n")


    complexity_prompt = f"""You are an advanced AI agent that evaluates natural language prompts to determine if they involve simple or complex tasks. Here's the difference between them:

    - **Simple Tasks:** These are straightforward actions that typically do not pose a significant risk to the system. They usually involve basic operations such as:

    - **File and Directory Management:**
        - Creating directories (e.g., `mkdir project`)
        - Deleting empty directories (e.g., `rmdir old_folder`)
        - Creating empty files (e.g., `touch newfile.txt`)
        - Copying files (e.g., `cp file.txt /backup/`)
        - Moving files (e.g., `mv file.txt /documents/`)
        - Viewing file contents (e.g., `cat file.txt`)
        - Searching for specific text in files (e.g., `grep "search term" *.txt`)
        - Renaming files (e.g., `mv oldname.txt newname.txt`)
        - Listing contents of a directory (e.g., `ls ~/Downloads`)
    
    - **System Information and Status:**
        - Checking system uptime (e.g., `uptime`)
        - Displaying current user information (e.g., `whoami`)
        - Viewing disk space usage (e.g., `df -h`)
        - Checking memory usage (e.g., `free -h`)
        - Listing currently running processes (e.g., `ps aux`)
        - Displaying system logs (e.g., `tail -n 50 /var/log/syslog`)
    
    - **Network Management:**
        - Turning off Wi-Fi (e.g., `nmcli radio wifi off`)
        - Enabling Wi-Fi (e.g., `nmcli radio wifi on`)
        - Checking IP address (e.g., `ip addr show`)
        - Displaying network interfaces (e.g., `ifconfig`)
        - Flushing DNS cache (e.g., `sudo systemd-resolve --flush-caches`)
        - Pinging an address to check connectivity (e.g., `ping google.com`)
    
    - **Basic Configuration:**
        - Changing terminal colors or preferences (e.g., `echo -e "\e[31m"`)
        - Setting environment variables (e.g., `export VAR=value`)
        - Changing the current working directory (e.g., `cd ~/Downloads`)
        - Viewing and editing configuration files with a text editor (e.g., `nano ~/.bashrc`)
    
    - **System Utilities:**
        - Checking for updates (e.g., `sudo apt-get update`)
        - Using basic text editors (e.g., opening a file with `nano file.txt`)
        - Running scripts with known effects (e.g., `bash script.sh`)
        - Monitoring system performance (e.g., `top`)

    - **Complex Tasks:** These tasks can potentially affect the system significantly and may require careful handling or elevated permissions. They often involve:
    - Writing or modifying code (e.g., `echo 'print("Hello World")' > script.py`)
    - Installing or uninstalling applications (
models/gemini-1.5-pro-exp-0801e.g., `sudo apt-get install nginx`)
    - Deleting or modifying system files (e.g., `rm -rf /etc/hostname`)
    - Changing system configurations (e.g., `sudo nano /etc/hosts`)
    - Managing system resources (e.g., `kill -9 PID`)
    - Running scripts that could impact system stability or security (e.g., `./cleanup.sh`)
    - Executing commands that affect multiple files or processes simultaneously (e.g., `find . -type f -exec rm  +`)
    - Risk to System Integrity(e.g. )
    - Network-related configurations (e.g., `iptables -A INPUT -p tcp --dport 22 -j DROP`)
    - Setting up user permissions (e.g., `chmod 755 script.sh`)
    - Automating tasks via scripts or batch processing (e.g., `crontab -e`)
    - Setting up development environments or databases (e.g., `sudo apt-get install python3-venv`)
    - Modifying kernel parameters (e.g., `sysctl -w net.ipv4.ip_forward=1`)
    - Performing system upgrades (e.g., `sudo apt-get upgrade`)
    - Backing up system configurations (e.g., `tar -cvf backup.tar /etc/`)
    - Changing the system hostname (e.g., `sudo hostnamectl set-hostname new-hostname`)
    - Managing user accounts (e.g., `sudo useradd newuser`)
    - Modifying firewall settings (e.g., `sudo ufw allow 22`)
    - Scheduling tasks with cron jobs (e.g., `crontab -l`)
    - Setting up network services (e.g., `sudo systemctl start apache2`)
    - Changing system locale settings (e.g., `sudo update-locale LANG=en_US.UTF-8`)
    - Restoring the system from a backup (e.g., `rsync -av /backup/ /`)
    
    Your task is to analyze the given prompt, identify whether it involves simple or complex tasks, and categorize them accordingly. If the prompt includes complex tasks, flag them for further review with a cautionary note enclosed in unique delimiters (e.g., [!! WARNING !!]) and also give  what kind of is it (e.g, ,[Installing]). 

    **Example of the conversation should be like this:**
    - User: "I need to set up my workspace by creating a folder for my documents and checking the disk space to make sure I have enough storage. If I find any    large files that I don't need anymore, please delete them to free up space."
    - Create a folder for my documents. - [Simple Task]
    - Check the disk space to ensure enough storage is available. - [Simple Task]
    - Delete any large files that are no longer needed. - [!! WARNING !!] [Complex Task] []

    The prompt to analyze is: {tasks_response.text}"""


    check_complexity = model.generate_content(complexity_prompt, safety_settings={'HARASSMENT': 'block_none', 'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
    print(check_complexity.text, "\n\n-----------------------------------------------------------------------------------------------------------------------\n\n")
    
    
    command_prompt = f"""
    You are an intelligent assistant that can understand natural language prompts.
    Here I will give you a list of tasks; look at them thoroughly.
    Suppose you are an AI agent that converts the given prompt into a {System_OS} command that can be directly executed.
    You have to take the prompt and convert it into a command in line byy line so i can directly execute them and get mmy results get my results.
    The prompt is: {check_complexity.text}
    Also, your current directory is {os.getcwd()}
    """
    command_response = model.generate_content(command_prompt, safety_settings={'HARASSMENT': 'block_none', 'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
    print(command_response.text, 
          "\n\n-----------------------------------------------------------------------------------------------------------------------\n\n")
    command_validation = f"""You are an intelligent assistant that validates if a generated command accurately corresponds to the user's initial natural language prompt. Here's what you should do:

    1. **Understand the User's Prompt:** Carefully analyze the user's natural language input to identify the specific actions, requirements, and intentions.

    2. **Review the Generated Command:** Compare the generated command(s) against the user's prompt to determine if it correctly reflects the intended action(s). 

    3. **Validation Criteria:**
    - The command should perform exactly what the user has requested, without omissions or additions.
    - The command syntax should be accurate and executable on the specified operating system.
    - Ensure that the command does not introduce any unintended side effects that were not requested by the user.
    - Check if any necessary preconditions or context (e.g., file paths, permissions, environment variables) are correctly handled in the command.

    5. **Output Format:** 
    - Respond with just "yes" or "no".
    - If the command is correct, explicty state: "yes"
    - If the command is incorrect, state: "no."

    The user's prompt is: "{cmd_input}"

    The generated command is: "{command_response.text}"

    Now, validate if the generated command is correct or not."""
    valid_test = model.generate_content(command_prompt, safety_settings={'HARASSMENT': 'block_none', 'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
    print(valid_test.text, 
          "\n\n-----------------------------------------------------------------------------------------------------------------------\n\n")




    context_prompt = f"""
    You are an intelligent assistant.
    The user has given the following prompt: "{cmd_input}"
    and the prompt has been break down into the following task : "{check_complexity.text}".
    and the prompt is converted to the following command  : "{command_response.text}"
    Current Operating System:** {System_OS}
    Current Working Directory (PWD):** {os.getcwd()}
    Before executing this command, please gather all relevant context and information that may affect its execution here if the user asked the name of file directory to be created could be anything then  you name it.
    here all the  converted to command that will be later executed , your work is to check if there is any prior info that is requied that the system should know before running the commands if yes then give the list of those info that it should have before running.
    Provide a lis . for each command what very necessary info should be there place them sequencially. and in dictionary format .
    Provide a dictionary like this:
    {{
    "command": ["necessary_info1", "necessary_info2"],
    }}
    """

    context_response = model.generate_content(context_prompt, safety_settings={'HARASSMENT': 'block_none', 'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
    print("Context gathered:", context_response.text)





# "As I prepare for my upcoming project, I want to create a directory for all related files. Also, could you check the current memory usage to ensure my system can handle the workload? If there are any unnecessary applications running, please close them to optimize performance."

# I need to set up my workspace by creating a folder for my documents and checking the disk space to make sure I have enough storage. If I find any large files that I don't need anymore, please delete them to free up space

































































    # a = chat.send_message(f"""Suppose you are an ai agent that converts the given prompt into a {System_OS} command that can be directly executed, you have to take the prompt and convert it into a command so that i can paste your response and get my results , the prompt is {cmdin} , also your current directory is {os.getcwd()} """ , safety_settings={'HARASSMENT':'block_none', 'HARM_CATEGORY_DANGEROUS_CONTENT' : 'block_none' ,'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})

    # c = model.generate_content(f"""Suppose you are an ai agent that converts the given prompt into a {System_OS} command that can be directly executed, now check if there is extra anything other than command then remove it there, just keep the command ,the command is {a.text}""")
    
    # b = model.generate_content(f"""Now check the command if its a {System_OS} command and if its the right command or not if yes response with 'yes' else resposnse with 'no'  , the command is {c.text}""")

    # if b.text.lower() == "yes":
    #     check_before_exec = input(f"Are you sure you want to run this command?\n'{c.text}'\n1. Yes\n2. No\nDefault = Yes\n")
        
    #     if not check_before_exec or check_before_exec.lower() == "yes":
            
    #         try:
    #             if System_OS == "windows Powershell":
    #                 rancomd = subprocess.run(['powershell', '-Command', c.text], stdout=subprocess.PIPE, 
    #                                          stderr=subprocess.PIPE, text=True, check=True)
    #             elif System_OS == "linux" or System_OS == "macOs":
    #                 rancomd = subprocess.run(c.text, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #             else:
    #                 print("OS could not be determined, exiting the program.")
    #                 sys.exit(1)
                
    #             print(f"The results are:\n{rancomd.stdout.decode('utf-8')}")
    #             if {rancomd.stdout.decode('utf-8')} == "" or {rancomd.stdout.decode('utf-8')} == None :
                
    #                 check_work = model.generate_content(f"""The command that ran in the {System_OS} was '{c.text}' "
    #                                                      f"and the output of that command was '{rancomd.stdout.decode('utf-8')}'. "
    #                                                      f"The error from the command was '{rancomd.stderr.decode('utf-8')}'. "
    #                                                      f"Now, I have run the command and don't know if it was successful. "
    #                                                      f"If there is a way to check if the given command has done its work or not, "
    #                                                      f"please provide that command or list of commands to verify.""")
    #                 print(check_work.text)
    #                 def write_to_file(file_path, content):
    #                     with open(file_path, 'w') as file:
    #                         file.write(content)
                    
    #                 write_to_file('verify_run.txt' , check_work.text)
    #                 count = 1

    #                 with open('verify_run.txt' , 'r') as f :
    #                     verify_cmd_content = f.read()
    #                 def verify_the_command(verify_cmd_list , prompt , count):
    #                     ver = chat2.send_message(f"""now their is the file that contains the commands to verify if the command given in the prompt ran sucessfully now you have to take the {count} command now just give me the {count} command that i can run directly in my console and get the output""")
    #                 # ver = chat2.send_message(f'now their is the file that contains the commands to verify if the command given in the prompt ran sucessfully now you have to take the {count} command and try to run and check if that verifies if the command in the prompt work sucessfully or not, here the  file is {verify_cmd_content} and the prompt command is {prompt} , if it verifies than response with `yes` else response with `no`  ')
    #                     print(ver)
    #                     if ver.text.lower() == "yes" :
    #                         count = 1
    #                         pass
    #                     else :
    #                         count+=1
    #                         verify_the_command(verify_cmd_content , c.text , count)

    #                 verify_the_command(verify_cmd_content , c.text ,count)


                    
            
    #         except subprocess.CalledProcessError as e:
                
    #             print(f"The Error is: {e}")

    #             check_error = model.generate_content(f"Here is the error code for the command that was performed in {System_OS}. "
    #                                                     f"Check what's wrong with it and provide commands to solve it. "
    #                                                   #  f"If input is required by that command from the user, add '--required-user-input' at the end of your response. "
    #                                                     f"The error is '{e}', the command was '{c.text}'. "
    #                                                     f"For more info, the current directory is '{os.getcwd()}'. "
    #                                                   #  f"Please provide the steps in a JSON format.
    #                                                     f"")
    #             print(check_error.text)

    #             def write_to_file(file_path, content):
    #                 with open(file_path, 'w') as file:
    #                     file.write(content)
                
    #             write_to_file('errors.txt' , check_error.text)


    #             def eradicate_errors_with_recurrsion_call(errorslist , prompt , error) :

    #                 pass
    
    # else:
    #     print(b.text)














# def errors_handler_and_verifyer(command , prompt ) :
#             try:
#                 if System_OS == "windows Powershell":
#                     rancomd = subprocess.run(['powershell', '-Command', c.text], stdout=subprocess.PIPE, 
#                                              stderr=subprocess.PIPE, text=True, check=True)
#                 elif System_OS == "linux" or System_OS == "macOs":
#                     rancomd = subprocess.run(c.text, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#                 else:
#                     print("OS could not be determined, exiting the program.")
#                     sys.exit(1)
                
#                 return {rancomd.stdout.decode('utf-8')}
               
            
#             except subprocess.CalledProcessError as e:
                
#                 print(f"The Error is: {e}")

#                 check_error = model.generate_content(f"Here is the error code for the command that was performed in {System_OS}. "
#                                                         f"Check what's wrong with it and provide commands to solve it. "
#                                                       #  f"If input is required by that command from the user, add '--required-user-input' at the end of your response. "
#                                                         f"The error is '{e}', the command was '{c.text}'. "
#                                                         f"For more info, the current directory is '{os.getcwd()}'. "
#                                                       #  f"Please provide the steps in a JSON format.
#                                                         f"")
#                 #check for errors
#                 print(check_error.text)
#                 def write_to_file(file_path, content):

#                     with open(file_path, 'a') as file:
#                         file.write(content)
                
#                 write_to_file('verifying_cerrors.txt' , check_error.text)
