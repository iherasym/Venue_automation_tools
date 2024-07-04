"""
This script allows the user to create and download the DumpCache file for a desired venue and to get from it the most
active RIC for every CID and Domain.
"""
import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket
import time
import datetime
import pandas as pd
import csv
import re

def main():
    hostname = input("provide server Ip: ")
    password = input("provide password: ")
    LH_name = input("provide LH names separated by space: ").split()
    venue_name = input("provide venue name: ")
    config_path = "/data/Venues/" + venue_name + "/config/"
    local_path = input("provide a location where you want to save FIDFilter and DumpCache files to your local machine: ")
    today=datetime.datetime.now().strftime("%Y%m%d")
    dumpcache_file = LH_name + "_" + today + ".csv"
    download_fidfilter(hostname, password, config_path, local_path)
    for LH in LH_name:
        download_dumpcache(hostname,password,config_path,local_path,dumpcache_file)
    CID_dumpcache = find_CID_dumpcache(dumpcache_file)
    CID_FIDFilter = find_CID_FIDFilter()
    compare_CID(CID_dumpcache, CID_FIDFilter)

# this function is to download the DumpCache and FidFilter files to your local machine#
def download_fidfilter(hostname,password,config_path,local_path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username=root,password=password,port=22)
        print("I am connected to download FIDFilter file")
        sftp_client = ssh.open_sftp()
        print("FIDFilter.txt is downloading")
        sftp_client.get(config_path + "FIDFilter.txt", local_path + "\\FIDFilter.txt")
        print("FIDFilter.txt - downloading completed")
        sftp_client.close()
        ssh.close
        return None

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
def download_dumpcache(hostname,password,config_path,local_path,dumpcache_file):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username=root,password=password,port=22)
        print("I am connected to download DumpCache file")

        stdin, stdout, stderr = ssh.exec_command(f"cd /data/che/bin ; pwd ; ./Commander -n linehandler -c 'dumpcache {LH_name}'")
        time.sleep(10)
        outp = stdout.readlines()

        sftp_client = ssh.open_sftp()
        print("DumpCache file is downloading")
        sftp_client.get(config_path + dumpcache_file, local_path + "\\" + dumpcache_file)
#       sftp_client.get(config_path + dumpcache_file, "C:\\Temp\\" + dumpcache_file)
        print("Dumpcache file - download completed")
        sftp_client.close()
        ssh.close
        return None

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

def find_CID_dumpcache(dumpcache_file):
    data = pd.read_csv(dumpcache_file).dropna()
    CID_dumpcache = list(set(map(int,data["CONTEXT_ID"].tolist())))
    CID_dumpcache = [format(c, 'd') for c in CID_dumpcache]
    return CID_dumpcache
def find_CID_FIDFilter():
    fo=open(file, "r")
    fo1=open(file_CID, "w")
    content=fo.readlines()
    fo.close()
    for l in content:
        if "LIST NUMBER:" in l:
            fo1.write(l)
    fo1.close()
    fo1=open(file_CID, "r")
    CID_FIDFilter=[]
    patt=r"\d\d\d\d"
    for p in fo1:
        CID_FIDFilter.extend(re.findall(patt, p))
    fo1.close()
    return CID_FIDFilter

def compare_CID(CID_dumpcache, CID_FIDFilter):
    CID_missing = []
    for c in CID_FIDFilter:
        if c not in CID_dumpcache:
            CID_missing.append(c)
    if len(CID_missing) != 0:
        print(f"Missing CIDs in dumpcache are: {CID_missing}")
    else:
        print(f"All CID from FIDFilter are present in dumpcache")
    return None

def sample_RIC_per_CID(dumpcache_file, CID):
    for D in CID:
        data = pd.read_csv(dumpcache_file)
        CURR_SEQ_NUM = data["CURR_SEQ_NUM"].tolist()
        CURR_SEQ_NUM.sort()
        highest = CURR_SEQ_NUM[-1]
        return (highest)

main()
