import Functions.AutomationFunctions as f
import Variables.Host_Pass_Var as v

def CID_FidFiler():
    hostname = v.hostname
    password = v.password
    config_path = "/data/Venues/LSEGTP/config/"
    local_path = "C:\\Users\\U6017127\\PycharmProjects\\HerasiMor_Framework\\Logs\\"
    f.download_fidfilter(hostname,password,config_path,local_path)
    file = local_path + "FIDFilter.txt"
    f.find_CID_FIDFilter(file,local_path)

CID_FidFiler()
















