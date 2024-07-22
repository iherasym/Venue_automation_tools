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
import sys
import subprocess

"""
This script allows the user to download the PERSIT file from a desired venue and check if the given RIC is persisted
both for MARKET_PRICE , MARKET_BY_PRICE or MARKET_BY_ORDER 
"""
def download_Persist(hostname,username,password,config_path,persist_file):

    try:

        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username=username,password=password,port=22)

        sftp_client = ssh.open_sftp()
        print(f"file {persist_file} is downloading")
        sftp_client.get(config_path + persist_file, "C:\PMAT\\x64\\" + persist_file)
        print(f"Download completed find file {persist_file} at C:\PMAT\\x64")
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
        print(f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()



"""
This function check given RIC into PERSIST file and return persisteed data for MBP.MP and MBO
"""

def check_persist(ric,persist_file):
    try:
        ric
        persist_file
        os.chdir("C:\\PMAT\\x64")

        os.system(f"PMAT dump --dll schema_V9.dll --db {persist_file} --ric {ric} --MARKET_PRICE> {ric}.txt")
        filename = f"C:\\PMAT\\x64\\{ric}.txt"
        os.startfile(filename)

        return None

    except FileNotFoundError:
        print(f"file not found make sure {persist_file} file to analyze is downloaded at C:\\PMAT\\x64")
        quit()
    except Exception as e:
        print(e)
        quit()
        
        
        
        
def output_host(hostname, psw):
    ssh = paramiko.SSHClient()  # create ssh client
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username="root", password=psw, port=22)
    stdin, stdout, stderr = ssh.exec_command(f"hostname")
    time.sleep(2)
    host = stdout.read()
    host = host.decode(encoding="utf-8")
    output_host = ''.join(c for c in host if c.isprintable())
    return output_host


def FilesDownload(hostname, WorkspacePath, psw, output_host):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print(f"ftp connection established executing\n")
        apath = '/data/che'
        apattern = '"*.log"'
        rawcommand = 'find {path} -name {pattern}'
        command = rawcommand.format(path=apath, pattern=apattern)
        stdin, stdout, stderr = ssh.exec_command(command)
        filelist = stdout.read().splitlines()

        ftp = ssh.open_sftp()
        for afile in filelist:
            (head, filename) = os.path.split(afile)
            ftp.get(afile, WorkspacePath + "\\" + output_host + "_" + str(filename))

        ftp.close()
        ssh.close()  # close connection
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


def FMSClientDownload(hostname, WorkspacePath, psw, output_host):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        ftp.get("/data/FMSClient/FMSClient.log", WorkspacePath + "\\" + output_host + "_FMSClient.log")
        ftp.close()
        ssh.close()  # close connection
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


def SCWDownload(hostname, WorkspacePath, psw, output_host):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        todaysmf = ftp.get("/data/SCWatchdog/logs/SCWatchdog.log", WorkspacePath + "\\" + output_host + "_SCWatchdog.log")
        ftp.close()
        ssh.close()  # close connection
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


def Core_fileList(WorkspacePath):
    my_dir = WorkspacePath

    files = []
    for (dirpath, dirnames, filenames) in walk(my_dir):
        files.extend(filenames)

    print(files)
    return files




def Core_Find_Exceptions(WorkspacePath, files, today, output_host):
    try:
        my_dir = WorkspacePath + "\\"
        print(my_dir)
        patt = r"\bException\b"
        fo1 = open(my_dir + output_host + "_EXEPTIONS_log-" + today + ".txt", "w")
        for f in files:
            fo = open(my_dir + f, "r")  # open host file in read mode
            fo1 = open(my_dir + output_host + "_EXEPTIONS_log-" + today + ".txt", "a")
            fo1.write(f"\n ************************* EXCEPTION ERRORS IN  {f} ************************************\n \n")
            files_lines = fo.readlines()  # readlines create a list with each line of the file
            for each_line in files_lines:  # loop into list crreated
                if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                    if each_line != "":
                        fo1.write(each_line)  # write line on errorlog file
        filename = my_dir + "\\" + output_host + "_EXEPTIONS_log-" + today + ".txt"
        os.system(f"copy {filename} C:\\Users\\U6017127\\.jenkins\\workspace\\Venue_Core_Logs_Check")
        fo.close()
        fo1.close()

    except TimeoutError:
        print(
            f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
    except FileNotFoundError:
        print(f"File not found make sure  file to analyze is downloaded at C:\\Users\\U6017127\\.jenkins\\workspace\\Venue_Core_Logs_Check" )
        quit()
    except Exception as e:
        print(e)
        quit()
        


def download_dumpcache(hostname, password, LH, local_path, today ,output_host):
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
        config_ph = config_ph.decode(encoding="utf-8")
        config_ph = ''.join(c for c in config_ph if c.isprintable())
        sftp_client = ssh.open_sftp()
        print("DumpCache file is downloading")
        sftp_client.get(config_ph, local_path + output_host + "_" + dumpcache_file)
        dumpcache_file = output_host + "_" + dumpcache_file
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
        print(f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()

def download_dumpcache_atlas(hostname, password, LH, local_path, today, output_host):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=password, port=22)
        print("I am connected to download DumpCache file")
        stdin, stdout, stderr = ssh.exec_command(f"cd .. ; cd tmp ; commander.sh {LH} cache dump > {LH}_{today}.csv")
        time.sleep(10)
        outp = stdout.readlines()
        dumpcache_file = LH + "_" + today + ".csv"
        print(dumpcache_file)
        sftp_client = ssh.open_sftp()
        print("DumpCache file is downloading")
        path = "/tmp/" + dumpcache_file
        sftp_client.get(path, local_path + output_host + "_" + dumpcache_file)
        dumpcache_file = output_host + "_" + dumpcache_file
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
        print(f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()

def find_CID_dumpcache(local_path, dumpcache_file):
    file = local_path + dumpcache_file
    def getColumn(name):
        return [row[name] for row in data]

    with open(file, newline='') as new_csv_file:
        new_csv_file = csv.DictReader(new_csv_file)
        data = list(new_csv_file)
    CID_all = []

    for u in getColumn('CONTEXT_ID'):
        CID_all.append(u)

    while ("" in CID_all):
        CID_all.remove("")
    CID = list(set((CID_all)))
    return CID


def sample_RIC_per_CID(type, local_path, dumpcache_file, CID, LH):
    data = pd.read_csv(local_path + dumpcache_file)
    if type == "TD":
        columns_to_drop = ['ITEM_ID', 'LAST_UPDATED', 'LAST_ACTIVITY', 'TIME_CREATED', 'VEHICLEID']
    elif type == "ATLAS":
        columns_to_drop = ['VEHICLE_ID', 'LAST_UPDATED', 'LAST_ACTIVITY', 'TIME_CREATED', 'ISSUTYPE']
    data.drop(columns=columns_to_drop, inplace=True, axis=1)
    data.to_csv(local_path + 'new_dump_file.csv', index=False)
    new_dump_file = 'new_dump_file.csv'
    fo = open(local_path + new_dump_file, "r")
    content = fo.readlines()
    fo4 = open(local_path + "Sample_RICs.txt", "a")
    fo4.write(f"*** {LH} ***\n")
    for c in CID:
        fo1 = open(local_path + "CID_" + c + "_RIC_LIST.csv", "w")
        fo1.write(list(content)[0])
        patt1 = r"\b" + c + "\\b"
        for line in content:
            if re.findall(patt1, line):
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
        patt2 = r"\b" + highest + "\\b"
        for l in content_highest:
            if re.findall(patt2, l):
                fo3.writelines(l, )
        fo2.close()
        fo3.close()
        Sample_RIC = pd.read_csv(f"{local_path}{c}_Sample_RIC.csv")
        PUBLISH_KEY = Sample_RIC["PUBLISH_KEY"].tolist()
        DOMAIN = Sample_RIC["DOMAIN"].tolist()
        for K in PUBLISH_KEY:
            for D in DOMAIN:
                fo4.write(f"{D} - {c} - {K} \n")
                break
            break
        os.remove(local_path + "CID_" + c + "_RIC_LIST.csv")
        os.remove(local_path + c + "_Sample_RIC.csv")
        
    fo4.close()
        

def find_eth_ddna(hostname,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp=ssh.open_sftp()
        print("ftp connection estabilished collecting NIC card value for DDNA")
        ftp.get("/etc/hosts",path+"\\hosts.txt")
        ftp.close()
        ssh.close() # close connection
        # patt=r"\d{1-3}.\d{1-3}.\d{1-3}.\d{1-3}" # patt tofind ip addresses
        patt = r"DDNA-eth\d"
        fo = open(path+"\\hosts.txt", "r") # open hosts file in read mode
        files_lines = fo.readlines() # readlines create a list with each line of the file
       # print(files_lines)
        for each_line in files_lines:     # loop into list created
            if re.findall(patt, each_line):   # only print when you fine key word DDNA
                eth_ddn=(each_line[-6]+each_line[-5]+each_line[-4]+each_line[-3]+each_line[-2]).strip("-")
                break
        fo.close()
        print(f"Reading completed: NIC for DDNA is {eth_ddn}")
        return str(eth_ddn)
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
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def find_eth_exch(hostname,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp=ssh.open_sftp()
        print("ftp connection estabilished collecting NIC card value for EXCHA")
        ftp.get("/etc/hosts",path+"\\hosts.txt")
        ftp.close()
        ssh.close() # close connection
        # patt=r"\d{1-3}.\d{1-3}.\d{1-3}.\d{1-3}" # patt tofind ip addresses
        patt = r"EXCHIPA-eth\d"
        fo = open(path+"\\hosts.txt", "r") # open hosts file in read mode
        files_lines = fo.readlines() # readlines create a list with each line of the file
       # print(files_lines)
        for each_line in files_lines:     # loop into list created
            if re.findall(patt, each_line):   # only print when you fine key word DDNA
                eth_exch=(each_line[-6]+each_line[-5]+each_line[-4]+each_line[-3]+each_line[-2]).strip("-")
                break
        fo.close()
        print(f"Reading completed: NIC for DDNA is {eth_exch}")
        return str(eth_exch)
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
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()
    except Exception as e:
        print(e)
        quit()


def tcpdump_installation(hostname,psw):
   try:
       ssh = paramiko.SSHClient()  # create ssh client
       ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       ssh.connect(hostname=hostname, username="root", password=psw, port=22)
       print("Checking tcpdump version installed on remote server")
       stdin, stdout, stderr = ssh.exec_command("tcpdump --help")
       file_lines = stderr.readlines()
       patt = r"\btcpdump version\b"
       for line in file_lines:
         if re.findall(patt, line):
            line
            break
         else:
            line = ""

       if bool(line) == True:
         print("The version installed is:", line)
       else:
         print("tcpdum not installed on your machine installing now")
         stdin, stdout, stderr = ssh.exec_command("yum -y install tcpdump")
         time.sleep(20)
         print("Installation completed")
         stdin, stdout, stderr = ssh.exec_command("tcpdump --help")
         file_lines = stderr.readlines()
         patt = r"\btcpdump version\b"
         for line in file_lines:
             if re.findall(patt, line):
                 line
                 break
             else:
                 line = ""
         if bool(line) == True:
            print("The version installed is:", line)
            ssh.close()
         return None
   except ConnectionError:
       print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
   except ConnectionRefusedError:
       print("connection is refused make sure password for the server is correct")
   except Exception as e:
       print(e)

def collect_pcap_ddna(hostname,eth_ddn,filename,seconds,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        stdin, stdout, stderr = ssh.exec_command(f"tcpdump -i  {eth_ddn} port 7777 -w {filename}")
        print(f"Capturing {filename}")
        time.sleep(seconds)
        stdin, stdout, stderr = ssh.exec_command("pkill -f tcpdump")
        print(f"{filename} capture completed")
        ftp = ssh.open_sftp()
        print(f"ftp connection established downloading {filename}")
        ftp.get(filename,path+"\\"+filename)
        ftp.close()
        ssh.close()  # close connection
        print(f"Download completed, you can find your {filename} at {path}")
        return None
    except FileNotFoundError:
        print("Pcap file not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
        quit()
    except Exception as e:
        print(e)
        quit()

def collect_pcap_exch(hostname,eth_exch,filename,seconds,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        stdin, stdout, stderr = ssh.exec_command(f"tcpdump -i  {eth_exch} -w {filename}")
        print(f"Capturing {filename}")
        time.sleep(seconds)
        stdin, stdout, stderr = ssh.exec_command("pkill -f tcpdump")
        print(f"{filename} capture completed")
        ftp = ssh.open_sftp()
        print(f"ftp connection established downloading {filename}")
        ftp.get(filename,path+"\\"+filename)
        ftp.close()
        ssh.close()  # close connection
        print(f"Download completed, you can find your {filename} at {path}")
        return None
    except FileNotFoundError:
        print("Pcap file not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
        quit()
    except Exception as e:
        print(e)
        quit()

def Rm_file(hostname,filename,psw):
       ssh = paramiko.SSHClient()  # create ssh client
       ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       ssh.connect(hostname=hostname, username="root", password=psw, port=22)
       print("connected")
       stdin, stdout, stderr = ssh.exec_command(f"rm -- {filename}")
       print("remote file deleted")
       ssh.close()
       return None
       


def install_port_blocker(hostname,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print("ftp connection installing portblocker")
        print(path + "\\portblocker.tar")
        ftp.put(path+"\\portblocker.tar", "/root/portblocker.tar")
        time.sleep(15)
        ftp.close()
        print("Upload file completed ")
        stdin, stdout, stderr = ssh.exec_command("tar -vxf portblocker.tar")
        print("portblocker.tar unzipped checking version:")
        stdin, stdout, stderr = ssh.exec_command("chmod a+x portblocker")
        stdin, stdout, stderr = ssh.exec_command("chmod a+x PortBlocker_Eng.ko")
        stdin, stdout, stderr = ssh.exec_command("./portblocker -version")

        file_out = stdout.readlines()
        for line in file_out:
            if line in file_out:
                print(line)
        file_err = stderr.readlines()
        for err in file_err:
            if err in file_err:
                print(
                    f"{err}\n Portblocker in not installed on your machine\n make sure 'portblocker.tar' file is in your working path")
                ssh.close()
        return None
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except TimeoutError:
        print("PoertBlocker file not found make sure the server ip and local path provided are correct\n Plese double check Portblocket.tar File is located in given Directory")
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
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def collect_NICs(hostname,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print("ftp colletting server NICs information")
        ftp.get("/etc/hosts", path+"\\hosts.txt")
        ftp.close()
        ssh.close()  # close connection
        # patt=r"\d{1-3}.\d{1-3}.\d{1-3}.\d{1-3}" # patt tofind ip addresses
        patt1 = r"\bDDNA-eth\d"
        patt2 = r"\bDDNB-eth\d"
        patt3 = r"\bEXCHIPA-eth\d"
        patt4 = r"\bEXCHIPB-eth\d"
        fo = open(path+"\\hosts.txt",
                  "r")  # open hosts file in read mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        server_eth = {"eth1": [], "eth2": [], "eth3": [], "eth4": []}
        for each_line in files_lines:  # loop into list created
            if re.findall(patt1, each_line):  # only print when you fine key word DDNA
                server_eth["eth1"].append(each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
            elif re.findall(patt2, each_line):
                server_eth["eth2"].append(each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
            elif re.findall(patt3, each_line):
                server_eth["eth3"].append(each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
            elif re.findall(patt4, each_line):
                server_eth["eth4"].append(each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
        fo.close()
        print(f"NIC Card for DDNA is {server_eth.get('eth1')}")
        print(f"NIC Card for DDNB is {server_eth.get('eth2')}")
        print(f"NIC Card for EXCHA is {server_eth.get('eth3')}")
        print(f"NIC Card for EXCHB is {server_eth.get('eth4')}")
        ssh.close()
        return server_eth
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
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def block_Ports(hostname,eth1,eth2,eth3,eth4,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        print("Connected to remote host")
        a = sys.argv[3] # input("Please provide NIC Card to block: DDN or EXCH?: ").upper()
        b = sys.argv[4] #("Please provide protocol you want to block UDP, TCP, BOTH: U,T,B: ").upper()
        c = sys.argv[5] #("Please specify which NIC card you want to block: A, B or All ").upper()
        try:
          wait=sys.argv[6]
          wait = int(wait)
        except ValueError:
            print("please provide time in seconds")
        seconds = str(wait)
        if a == "DDN" and b=="B" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r B -s B -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All DDN NIC cards traffic is blocked ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "DDN" and b== "U" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r U -s U -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on DDN NIC ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "DDN" and b == "T" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r T -s T -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN NIC")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "EXCH" and b == "B" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r B -s B -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All Exchange NIC cards traffic is blocked for")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "EXCH" and b== "U" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r U -s U -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "EXCH" and b == "T" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r T -s T -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on Exchange NIC")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")

###### Only A NIC will be block #############

        elif a == "DDN" and b == "B" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"A DDN NIC card traffic is blocked ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "DDN" and b == "U" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on DDN-A NIC ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "DDN" and b == "T" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN-A NIC ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "B" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"All Exchange NIC-A cards traffic are blocked")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "U" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC-A ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "T" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + "-r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on Exchange NIC-A ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()

######## only B NIC will be blocked #######################

        elif a == "DDN" and b == "B" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth2 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"All traffic on DDN-B NIC card is blocked ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "DDN" and b == "U" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth2 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on DDN NIC-B ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "DDN" and b == "T" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth2 + " -r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN NIC-B ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "B" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth4 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"All traffic on Exchange NIC-B cards is blocked")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "U" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth4 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC-B")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "T" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth4 + " -r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on Exchange NIC-B ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()

        else:
            print(f"WRONG SELECTIONS\n Your current selection is:\n NIC Cards to Block={a}\n Protocol:{b},please check all the inforamtion are correct")
            block_Ports(hostname,eth1,eth2,eth3,eth4,psw)
        ssh.close()
        return None
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except TimeoutError:
        print("Host file not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def remove_portblocker(hostname,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        stdin, stdout, stderr = ssh.exec_command("rm portblocker.tar")
        stdin, stdout, stderr = ssh.exec_command("rm portblocker")
        stdin, stdout, stderr = ssh.exec_command("rm PortBlocker_Eng.ko")
        stdin, stdout, stderr = ssh.exec_command("./portblocker -version")

        file_out = stdout.readlines()
        for line in file_out:
            if line in file_out:
                print(line)
        file_err = stderr.readlines()
        for err in file_err:
            if err in file_err:
                print(f"{err}\n Portblocker has been uninstalled")
                ssh.close()
        return None
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except TimeoutError:
        print("Host file not found make sure the server ip and local path provided are correct")
        quit()
    except FileNotFoundError:
        print("PortBlocker is not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def SMF_FileDownload(hostname, path, psw,filename,output_host,today):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print("ftp connection established executing:")
        todaysmf = ftp.get("/ThomsonReuters/smf/log/" + filename,path + "\\" + output_host + "_smf-log-files." + today + ".txt")
        ftp.close()
        ssh.close()  # close connection
        return todaysmf
    except TimeoutError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except FileNotFoundError:
        print("SMF file not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except AuthenticationException:
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()

def DateRange(start_date,end_date,today):
    daterange = pd.date_range(start_date, end_date)

    date_ls = []
    for single_date in daterange:
        single_date = str(single_date.strftime("%Y%m%d"))
        date_ls.append(single_date)

    fileList = []
    for date in date_ls:
       if date == today:
          filename = "smf-log-files." + date + ".txt"
          fileList.append(filename)
       else:
          filename = "smf-log-files." + date + "_235959.txt"
          fileList.append(filename)
    return fileList


def SMF_FilesDownload(hostname, path, fileList,output_host, psw):
    try:
        fileList
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print(f"ftp connection established executing\n")
        ftp = ssh.open_sftp()
        for file in fileList:
            ftp.get("/ThomsonReuters/smf/log/" + file, path + "\\" + output_host + "_" + file)
        ftp.close()
        ssh.close()  # close connection
        return None
        return todaysmf
    except TimeoutError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except FileNotFoundError:
        print(
            "SMF file not found make sure the server ip and local path provided are correct\n double check dates and days range provided are also in the correct format")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except AuthenticationException:
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
        quit()
    except Exception as e:
        print(e)
        quit()


def SMF_Find_Critical(path,output_host, today):
    try:
        patt = r"\bCritical\b"
        fo = open(path + "\\" + output_host + "_smf-log-files." + today + ".txt", "r")  # open host file in read mode
        fo2 = open(path + "\\" + output_host + "_CRITICAL_log-" + today + ".txt", "w")  # open file in write mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        for each_line in files_lines:  # loop into list crreated
            if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                fo2.write(each_line)  # write line on errorlog file
        fo.close()
        fo2.close()
        return None
    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        quit()
    except Exception as e:
        print(e)
        quit()


def SMF_Find_Warning(path,output_host, today):
    try:
        patt = r"\bWarning\b"
        fo = open(path + "\\" + output_host + "_smf-log-files." + today + ".txt", "r")  # open host file in read mode
        fo2 = open(path + "\\" + output_host + "_WARNING_log-" + today + ".txt", "w")  # open file in write mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        for each_line in files_lines:  # loop into list crreated
            if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                fo2.write(each_line)  # write line on errorlog file
        fo.close()
        fo2.close()
        return None
    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        quit()
    except Exception as e:
        print(e)
        quit()


def SMF_Find_Critical_Files(path,output_host, fileList):
    try:
        my_dir = path
        patt = r"\bCritical\b"
        files = []
        for f in fileList:
            files.append("".join(output_host + "_" + f))
        for f in files:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\" + output_host + "_CRITICAL-logs-MULTIPLE_FILES.txt", "a")
            fo1.write(f"\n****************************************** CRITICAL ERRORS IN  {f}  **************************************************** \n \n")
            files_lines = fo.readlines()  # readlines create a list with each line of the file
            for each_line in files_lines:
                if re.findall(patt, each_line):
                    if each_line != "":
                        fo1.write(each_line)  # write line on errorlog file
        fo.close()
        fo1.close()
        return None

    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        quit()
    except Exception as e:
        print(e)
        quit()


def SMF_Find_Warning_Files(path,output_host, fileList):
    try:
        my_dir = path
        patt = r"\bWarning\b"
        files = []
        for f in fileList:
            files.append("".join(output_host + "_" + f))
        for f in files:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\" + output_host + "_WARNING-log-MULTIPLE_FILES.txt", "a")
            fo1.write(f"\n***************************************** WARNING ERRORS IN  {f} ***************************************************************\n \n")
            files_lines = fo.readlines()  # readlines create a list with each line of the file
            for each_line in files_lines:  # loop into list crreated
                if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                    if each_line != "":
                        fo1.write(each_line)  # write line on errorlog file
        fo.close()
        fo1.close()
        return None
    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        quit()
    except Exception as e:
        print(e)
        quit()
        
def Atlas_upload_and_run_script(hostname, password, lh_name):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {hostname}...")
        ssh.connect(hostname=hostname, username="root", password=password, port=22)

        sftp_client = ssh.open_sftp()
        local_script_path = "run_persist_viewer.sh"
        remote_script_path = f"/tmp/run_persist_viewer.sh"

        print(f"Uploading {local_script_path} to {remote_script_path}...")
        sftp_client.put(local_script_path, remote_script_path)
        sftp_client.chmod(remote_script_path, 0o755)

        command = f"/tmp/run_persist_viewer.sh {lh_name}"
        command2 = f"chmod +x /tmp/persist_viewer.sh"
        command3 = f"sudo chmod 775 /tmp/run_persist_viewer.sh"
        print(f"Giving Permission: {command2}")
        ssh.exec_command(command2)
        ssh.exec_command(command3)
        print(f"Running command: {command}")
        stdin, stdout, stderr = ssh.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()  # Wait for command to complete

        if exit_status == 0:
            print("Shell script executed successfully.")
            print(f"Output: {stdout.read().decode()}")
        else:
            print(f"Shell script failed with exit status {exit_status}.")
            print(f"Errors: {stderr.read().decode()}")
            return False

        sftp_client.close()
        ssh.close()
        return True

    except (
    socket.gaierror, TimeoutError, FileNotFoundError, ConnectionError, ConnectionRefusedError, AuthenticationException,
    SSHException) as e:
        print(f"Error during SSH operation: {e}")
        return False


def Atlas_download_persist(hostname, password, config_path, persist_file):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {hostname} for file download...")
        ssh.connect(hostname=hostname, username="root", password=password, port=22)

        sftp_client = ssh.open_sftp()
        remote_file_path = config_path + persist_file
        local_file_path = f"C:\\Users\\U6017127\.jenkins\\workspace\\TD_ATLAS_Persit_Analysis\\{persist_file}"

        print(f"Checking if the remote file {remote_file_path} exists...")
        try:
            sftp_client.stat(remote_file_path)
            print(f"File {remote_file_path} exists. Proceeding with download.")
        except FileNotFoundError:
            print(f"File {remote_file_path} does not exist.")
            sftp_client.close()
            ssh.close()
            return False

        print(f"Downloading file {persist_file} from {remote_file_path} to {local_file_path}")
        sftp_client.get(remote_file_path, local_file_path)
        print(f"Download completed. Find the file {persist_file} at C:\\PMAT\\x64")

        sftp_client.close()
        ssh.close()
        return True

    except (socket.gaierror, TimeoutError, FileNotFoundError, ConnectionError, ConnectionRefusedError, AuthenticationException,SSHException) as e:
        print(f"Error during SFTP operation: {e}")
        return False


def Atlas_delete_txt_files(hostname, password, config_path):
    ssh = paramiko.SSHClient()  # create ssh client
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=hostname, username="root", password=password, port=22)

        stdin, stdout, stderr = ssh.exec_command(f"rm {config_path}*.txt")
        stdout.channel.recv_exit_status()  # Ensure command execution is complete

        print("The persist  file in the remote /tmp directory has been removed correctly")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        ssh.close()

    return None


def Atlas_check_persist(ric_list,persist_file):
    try:
        os.chdir("C:\\PMAT\\x64")

        for r in ric_list:
            os.system(f"PMAT dump --dll schema_V9.dll --db {persist_file} --ric {r} > {r}.txt")
            filename = f"C:\\PMAT\\x64\\{r}.txt"
            os.startfile(filename)

    except FileNotFoundError:
        print(f"File not found. Make sure {persist_file} file to analyze is downloaded at C:\\PMAT\\x64")
        quit()
    except Exception as e:
        print(e)
        quit()


def download_fidfilter(hostname,password,config_path,local_path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=password,port=22)
        print("I am connected to download FIDFilter file")
        sftp_client = ssh.open_sftp()
        print("FIDFilter.txt is downloading")
        file = sftp_client.get(config_path + "FIDFilter.txt", local_path + "\\FIDFilter.txt")
        print("FIDFilter.txt - downloading completed")
        sftp_client.close()
        ssh.close
        return file

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



def find_CID_FIDFilter(file,local_path):
    try:
        fo=open(file, "r")
        fo1=open( local_path + "file_CID.txt", "w")
        content=fo.readlines()
        fo.close()
        for l in content:
            if "LIST NUMBER:" in l:
                fo1.write(l)
        fo1.close()
        fo1=open(local_path +"file_CID.txt", "r")
        CID_FIDFilter=[]
        patt=r"\d\d\d\d"
        for p in fo1:
            CID_FIDFilter.extend(re.findall(patt, p))
        fo1.close()
        return CID_FIDFilter

    except FileNotFoundError:
        print("Host file not found make sure the server ip and local path provided are correct")
    except Exception as e:
        print(e)



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



def get_host_today(hostname,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username="root", password=password, port=22)
    stdin,stdout,stderr = ssh.exec_command(f"date +'%Y''%m''%d'")
    time.sleep(2)
    return stdout.read().decode(encoding="utf-8").strip()



