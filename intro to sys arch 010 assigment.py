## importing the datatime to gather the time and date from the local device##
import datetime
## importing socket libary to locate my ip address##
import socket
## using the netmiko libary to connect to the remote device through ssh##
from netmiko import ConnectHandler
## using the SCP libary to import SCPclient, this allows me to back up the local file
from scp import SCPClient
## using the OS libary to interact with my operating system
import os
## using the urllib.request libary to handle the url data inputed from the user
import urllib.request

##I begin with displaying my menue, by defining the menu function

def display_menu():
    print("\n+++++++++++++++      menu      +++++++++++++++")
    print ("+             (1) date and time             ++")
    print("+            (2) local IP address           ++")
    print("+   (3) show remote home directory listing  ++")
    print("+     (4)back up a file from remote device  ++")
    print("+               (5)save web page            ++")
    print("+            (Q) exit the program           ++")
    print("++++++++++++++++++++++++++++++++++++++++++++++")

## the users options##

## Option 1. display the time and date request 
def display_local_timedate():
    print(f"Local-device date and time: {datetime.datetime.now()}")

## Option 2. display the ip address of the local device 
def get_local_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Local-device IP Address: {ip_address}")
    except Exception as e:
        print (f"ERROR: {e}")

## (3&4) CONNECTION TO REMOTE DEVICE.
def Remote_device_connection():
    return ConnectHandler(
        device_type = "linux",  
        host = "127.0.0.1",
        username = "darlo",
        password = "lubuntu1", 
        port = 2222,
        secret = "lubuntu1"
    )

## Option 3. List directory contents on the remote VM.##
def list_directory(connection, dir_path="/home/darlo"):
    command = f"ls -l {dir_path}"
    output = connection.send_command(command)
    print(f"Contents of {dir_path}:\n{output}")

## Option 4. backup a file from the remote VM to the local device##
def backup_file(connection, remote_file, backup_dir):
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

##installing the file name from remote device 
        filename = os.path.basename(remote_file)
        local_file = os.path.join(backup_dir, filename)

##using SCP backup to save file to local device 
        with SCPClient(connection.remote_conn.transport) as scp:
            scp.get(remote_file, local_file)

        print(f"File backup complete: {local_file}")
        
    except Exception as e:
        print(f"Failed to back up the file: {e}")
        
## option 5. Saving a webpage to the local system
def save_webpage():
    print(f"File will be saved in {os.getcwd()}")
    url = input("Enter the Url of the webpage to save: ").strip()
    try: 
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status == 200:
                content = response.read().decode('utf-8')
                with open("webpage_backup.html",'w', encoding='utf-8') as file:
                    file.write(content)
                print("webpage saved to webpage_backup.html")
            else:
                print(f"Failed to fetch the webpage: HTTP status {response.status}")
    except Exception as e:
            print(f"An error occurred while fetching the webpage: {e}")

## User input operation functions. this reads the users input to display the options
def main():
    connection = None 
    
    try:    
        while True:
            display_menu()
            choice = input("Please ENTER your choice: ").strip()

            if choice == "1":
                display_local_timedate()

            elif choice == "2":
                get_local_ip()

            elif choice == "3":
                if not connection:
                    connection = Remote_device_connection()
                list_directory(connection)
            

            elif choice == "4":
                if not connection:
                    connection = Remote_device_connection()
                remote_file = input("Enter the File path to back up: ").strip()
                backup_dir = input("Enter local backup location: ").strip()
                if not os.path.exists(backup_dir):
                    print(f"Backup directory '{backup_dir} does not exist. Creating it...")
                    os.makedirs(backup_dir)
                backup_file(connection, remote_file, backup_dir)

            elif choice == "5":
                save_webpage()
            
            elif choice.lower() == "q":
                print ("You have exited the program!")
                break 
        else:
            print ("Error! invalid choice. try again")  
    finally:
        if connection: 
            connection.disconnect()
                        
if __name__ == "__main__":
    main()

     

    


