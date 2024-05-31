"""
This script allows the user to download the PERSIT file from a desired venue and check if the given RIC is persisted
both for MARKET_PRICE , MARKET_BY_PRICE or MARKET_BY_ORDER 
"""
import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket

print("Please make sure PMAT is installed into your local machineat: C:\PMAT\"")

def main():
    hostname=input("provide server Ip: ")
    username=input("provide username: ")
    password=input("provide password: ")

    Lh_name=input("provide LH name :")
    venue_name=input("provide venue name :")
    config_path = "/data/Venues/"+ venue_name +"/config/"
    persist_file = "PERSIST_" + Lh_name +".DAT"
    download_Persist(hostname,username,password,config_path,persist_file)


# this function is to download the PMAT file to your local machine#

def download_Persist(hostname,username,password,config_path,persist_file):

    try:

        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username=username,password=password,port=22)

        sftp_client = ssh.open_sftp()
        print(f"file {persist_file}is downloading")
        sftp_client.get(config_path + persist_file, "C:\\PMAT\\" + persist_file)
        print(f"Download completed find file {persist_file} at {config_path}")
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
        print(f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


main()