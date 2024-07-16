"""
This script allows the user to create and download the DumpCache file for a desired venue and to get from it the most
active RICs for every CID and Domain.
"""
import paramiko
from paramiko.ssh_exception import AuthenticationException
import paramiko.sftp
import socket
import time
import datetime
import pandas as pd
import re
import csv
import os


def main():
    type = input("Is it ATLAS or TD: ")
    hostname = input("provide server Ip: ")
    password = input("provide password: ")
    LH_name = input("provide LH names separated by space: ").split()
    global output_host
    output_host = output_host(hostname, password)
    local_path = input(f"provide  location on your local machine to save dumpCache files: ") + output_host + "\\"
    os.makedirs(local_path,exist_ok=True)
    today = datetime.datetime.now().strftime("%Y%m%d")
    foSample_RICs = open(local_path + "Sample_RICs.txt", "w")
    foSample_RICs.write(f"Sample RICs for:\n\n")
    foSample_RICs.close()
    for LH in LH_name:
        if type == "ATLAS":
            dumpcache_file = download_dumpcache_atlas(hostname, password, LH, local_path, today, output_host)
            CID = find_CID_dumpcache(local_path, dumpcache_file, LH)
            sample_RIC(type, local_path, dumpcache_file, CID, LH)
        elif type == "TD":
            dumpcache_file = download_dumpcache_TD(hostname, password, LH, local_path, today, output_host)
            CID = find_CID_dumpcache(local_path, dumpcache_file, LH)
            sample_RIC(type, local_path, dumpcache_file, CID, LH)
    os.remove(local_path + "temp_dump_file.csv")
    print(f"Now all files are on your local machine in: {local_path}\nThank you. Bye :)")


# this function gets server's hostname
def output_host(hostname, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username="root", password=password, port=22)
    stdin, stdout, stderr = ssh.exec_command(f"hostname")
    time.sleep(2)
    host = stdout.read()
    host = host.decode(encoding="utf-8")
    output_host = ''.join(c for c in host if c.isprintable())
    return output_host


# this function downloads DumpCache files from TD venue to user's local machine
def download_dumpcache_TD(hostname, password, LH, local_path, today, output_host):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=password, port=22)
        print(f"---------------------------------------------------\nPlease wait, dumpcache creation for {LH}:")
        stdin, stdout, stderr = ssh.exec_command(f"cd /data/che/bin ; pwd ; ./Commander -n linehandler -c 'dumpcache {LH}'")
        time.sleep(10)
        outp = stdout.readlines()
        dumpcache_file = LH + "_" + today + ".csv"
        stdin, stdout, stderr = ssh.exec_command(f"find / -name " + dumpcache_file)
        time.sleep(2)
        config_ph = stdout.read()
        config_ph = config_ph.decode(encoding="utf-8")
        config_ph = ''.join(c for c in config_ph if c.isprintable())
        sftp_client = ssh.open_sftp()
        sftp_client.get(config_ph, local_path + output_host + "_" + dumpcache_file)
        print("    (1/3) - " + dumpcache_file + " is downloaded")
        dumpcache_file = output_host + "_" + dumpcache_file
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
        print(f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


# this function downloads DumpCache files from ATLAS venue to user's local machine
def download_dumpcache_atlas(hostname, password, LH, local_path, today, output_host):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=password, port=22)
        print(f"---------------------------------------------------\nPlease wait, dumpcache creation for {LH}:")
        stdin, stdout, stderr = ssh.exec_command(f"cd .. ; cd tmp ; commander.sh {LH} cache dump > {LH}_{today}.csv")
        time.sleep(10)
        outp = stdout.readlines()
        dumpcache_file = LH + "_" + today + ".csv"
        sftp_client = ssh.open_sftp()
        path = "/tmp/" + dumpcache_file
        sftp_client.get(path, local_path + output_host + "_" + dumpcache_file)
        print("    (1/3) - " + dumpcache_file + " is downloaded")
        dumpcache_file = output_host + "_" + dumpcache_file
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
        print(f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


# this function gets the list of CONTEXT_ID for each LineHandler
def find_CID_dumpcache(local_path, dumpcache_file, LH):
    temp = local_path + dumpcache_file
    CID_all = []
    with open(temp, newline='') as new_csv_file:
        new_csv_file = csv.DictReader(new_csv_file)
        data = list(new_csv_file)
    def getColumn(name):
        return [row[name] for row in data]
    for n in getColumn('CONTEXT_ID'):
        CID_all.append(n)
    while ("" in CID_all):
        CID_all.remove("")
    CID = list(set((CID_all)))
    for c in CID:
        if c == '0':
            CID.remove(c)
    print(f"    (2/3) - CONTEXT_ID: {CID}")
    return CID


# this function gets the most active Sample RICs for each CONTEXT_ID
def sample_RIC(type, local_path, dumpcache_file, CID, LH):
    data = pd.read_csv(local_path + dumpcache_file)
    if type == "TD":
        drop_columns = ['ITEM_ID', 'LAST_UPDATED', 'LAST_ACTIVITY', 'TIME_CREATED', 'VEHICLEID']
    elif type == "ATLAS":
        drop_columns = ['VEHICLE_ID', 'LAST_UPDATED', 'LAST_ACTIVITY', 'TIME_CREATED', 'ISSUTYPE']
    data.drop(columns = drop_columns, inplace=True, axis=1)
    data.to_csv(local_path + 'temp_dump_file.csv', index=False)
    temp_dump_file = 'temp_dump_file.csv'
    fo = open(local_path + temp_dump_file, "r")
    content = fo.readlines()
    foSample_RICs = open(local_path + "Sample_RICs.txt", "a")
    foSample_RICs.write(f"*** {LH} ***\n")
    for c in CID:
        foRIC_LIST = open(local_path + "CID_" + c + "_RIC_LIST.csv", "w")
        foRIC_LIST.write(list(content)[0])
        patt1 = r"\b" + c + "\\b"
        for line in content:
            if re.findall(patt1, line):
                foRIC_LIST.writelines(line)
        foRIC_LIST.close()
        data = pd.read_csv(local_path + "CID_" + c + "_RIC_LIST.csv")
        CURR_SEQ_NUM = data["CURR_SEQ_NUM"].tolist()
        CURR_SEQ_NUM.sort()
        highest = CURR_SEQ_NUM[-1]
        highest = str(highest)
        foHighest = open(local_path + "CID_" + c + "_RIC_LIST.csv", "r")
        content_highest = foHighest.readlines()
        foRICs = open(local_path + c + "_Sample_RIC.csv", "w", newline="")
        foRICs.write(list(content)[0])
        patt2 = r"\b" + highest + "\\b"
        for l in content_highest:
            if re.findall(patt2, l):
                foRICs.writelines(l, )
        foHighest.close()
        foRICs.close()
        Sample_RIC = pd.read_csv(f"{local_path}{c}_Sample_RIC.csv")
        PUBLISH_KEY = Sample_RIC["PUBLISH_KEY"].tolist()
        DOMAIN = Sample_RIC["DOMAIN"].tolist()
        for K in PUBLISH_KEY:
            for D in DOMAIN:
                foSample_RICs.write(f"{D} - {c} - {K} \n")
                break
            break
        os.remove(local_path + "CID_" + c + "_RIC_LIST.csv")
        os.remove(local_path + c + "_Sample_RIC.csv")
    foSample_RICs.close()
    print(f"    (3/3) - Sample RICs are gathered")


main()

#TD
#10.167.119.144
#Reuters1
#OPTIQ04 OPTIQ06 OPTIQ08 OPTIQ09
#C:\Users\UC502266\Documents\Functional\OPTIQ\Euronext_Cash_SBE335\Python_test\

#ATLAS
#10.167.157.83
#Reuters1
#CSA01
#C:\Users\UC502266\Documents\Functional\CSA\
