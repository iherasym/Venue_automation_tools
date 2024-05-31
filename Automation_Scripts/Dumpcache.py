"""
This script allows the user to create and download the DumpCache file for a desired venue and to get from it the most
active RIC for every CID and Domain.
"""
import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket
import time
import datetime
"""
def main():
    hostname = input("provide server Ip: ")
    username = input("provide username: ")
    password = input("provide password: ")
    LH_name = input("provide LH name: ")
    venue_name = input("provide venue name: ")
    config_path = "/data/Venues/" + venue_name + "/config/"
    local_path = input("provide a location where you want to save dumpcache file on your local machine: ")
    today=datetime.datetime.now().strftime("%Y%m%d")
    dumpcache_file = LH_name + "_" + today + ".csv"
    download_dumpcache_fidfilter(hostname,username,password,config_path)
"""

# /data/Venues/SWISS/config/
#
# SNF01F_20240530.csv

hostname = "10.167.157.3"
username = "root"
password = "Reuters1"
LH_name = "SMF01F"
venue_name = "SWISS"
config_path = "/data/Venues/SWISS/config/"
local_path = input("provide a location where you want to save dumpcache file on your local machine: ")
today = datetime.datetime.now().strftime("%Y%m%d")
dumpcache_file = LH_name + "_" + today + ".csv"

# this function is to download the DumpCache and FidFilter files to your local machine#

def download_dumpcache_fidfilter(hostname,username,password,config_path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username=username,password=password,port=22)
        print("I am connected")

        stdin, stdout, stderr = ssh.exec_command(f"cd /data/che/bin ; pwd ; ./Commander -n linehandler -c 'dumpcache {LH_name}'")
        time.sleep(10)
        outp = stdout.readlines()

        sftp_client = ssh.open_sftp()
        print("Files are downloading")
        sftp_client.get(config_path + "FIDFilter.txt", local_path + "\FIDFilter.txt")
#       sftp_client.get(config_path + "FIDFilter.txt", "C:\\Temp\\" + "FIDFilter.txt")
        print("FIDFilter.txt - download completed")
        sftp_client.get(config_path + dumpcache_file, local_path + "\\" + dumpcache_file)
#       sftp_client.get(config_path + dumpcache_file, "C:\\Temp\\" + dumpcache_file)
        print("Dumpcache file - download completed")
        sftp_client.close()
        ssh.close

    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except TimeoutError:
        print("Host file not found make sure the server ip and local path provided are correct")
        quit()
    except FileNotFoundError:
        print("Host file not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(
            f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()

download_dumpcache_fidfilter(hostname,username,password,config_path)

#main()
