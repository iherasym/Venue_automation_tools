import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket


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


