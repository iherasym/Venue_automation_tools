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
import re
import os

def main():
    hostname = input("provide server Ip: ")
    password = input("provide password: ")
    LH_name = input("provide LH names separated by space: ").split()
    local_path = input("provide a location where you want to save FIDFilter and DumpCache files to your local machine: ")
    today=datetime.datetime.now().strftime("%Y%m%d")
    fo4 = open(local_path + "Sample_RICs.txt", "w")
    fo4.write(f"Sample RICs for:\n\n")
    fo4.close()
    for LH in LH_name:
        dumpcache_file = download_dumpcache(hostname, password, LH, local_path, today)
        CID = find_CID_dumpcache(local_path, dumpcache_file)
        sample_RIC_per_CID(local_path, dumpcache_file, CID, LH)


# this function is to download the DumpCache and FidFilter files to your local machine#
# this function is to download the DumpCache and FidFilter files to your local machine#
def download_dumpcache(hostname, password, LH, local_path, today):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=password, port=22)
        print("I am connected to download DumpCache file")

        stdin, stdout, stderr = ssh.exec_command(f"cd /data/che/bin ; pwd ; ./Commander -n linehandler -c 'dumpcache {LH}'")
        time.sleep(10)
        outp = stdout.readlines()
        dumpcache_file = LH + "_" + today + ".csv"
        print(dumpcache_file)
        stdin, stdout, stderr = ssh.exec_command(f"find / -name " + dumpcache_file)
        time.sleep(2)
        config_ph = stdout.read()
        print(config_ph)
        config_ph = config_ph.decode(encoding="utf-8")
        config_ph = ''.join(c for c in config_ph if c.isprintable())
        print(config_ph)

        sftp_client = ssh.open_sftp()
        print("DumpCache file is downloading")
        sftp_client.get(config_ph, local_path + dumpcache_file)

        print("Dumpcache file - download completed")
        sftp_client.close()
        ssh.close
        return dumpcache_file

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


def find_CID_dumpcache(local_path, dumpcache_file):
    data = pd.read_csv(local_path + dumpcache_file).dropna()
    CID = list(set(map(int, data["CONTEXT_ID"].tolist())))
    CID = [format(c, 'd') for c in CID]
    return CID


def sample_RIC_per_CID(local_path, dumpcache_file, CID, LH):
    fo = open(local_path + dumpcache_file, "r")
    content = fo.readlines()
    fo4 = open(local_path + "Sample_RICs.txt", "a")
    fo4.write(f"*** {LH} ***\n")
    for c in CID:
        fo1 = open(local_path + "CID_" + c + "_RIC_LIST.csv", "w")
        fo1.write(list(content)[0])
        for line in content:
            if c in line:
                fo1.writelines(line)
        fo1.close()
        data = pd.read_csv(local_path + "CID_" + c + "_RIC_LIST.csv")
        CURR_SEQ_NUM = data["CURR_SEQ_NUM"].tolist()
        CURR_SEQ_NUM.sort()
        highest = CURR_SEQ_NUM[-1]
        highest = str(highest)
        fo2 = open(local_path + "CID_" + c + "_RIC_LIST.csv", "r")
        content_highest = fo2.readlines()
        fo3 = open(local_path + c + "_Sample_RIC.csv", "w", newline="")
        fo3.write(list(content)[0])
        patt = r"\b" + highest + "\\b"
        for l in content_highest:
            if re.findall(patt, l):
                fo3.writelines(l, )
        fo2.close()
        fo3.close()
        Sample_RIC = pd.read_csv(f"{local_path}{c}_Sample_RIC.csv")
        PUBLISH_KEY = Sample_RIC["PUBLISH_KEY"].tolist()
        DOMAIN = Sample_RIC["DOMAIN"].tolist()
        for K in PUBLISH_KEY:
            for D in DOMAIN:
                fo4.write(f"{D} - {c} - {K[0]} \n")
        os.remove(local_path + "CID_" + c + "_RIC_LIST.csv")
        #os.remove(local_path + c + "_Sample_RIC.csv")
    fo4.close()


main()
