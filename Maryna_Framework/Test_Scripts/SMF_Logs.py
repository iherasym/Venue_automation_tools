import Variables.SMF_Variables as v
import Functions.AutomationFunctions as f
import os

def SMF_Logs():
  today = v.today
  filename = "smf-log-files." + today + ".txt"
  hostname =v.hostname
  psw = v.password
  output_host = f.output_host(hostname,psw)
  path = v.Log_path
  os.makedirs(path + output_host, exist_ok=True)
  path = path + output_host
  options = v.smf_optons
  if options == "TODAY_LOG":
     f.SMF_FileDownload(hostname, path, psw,filename,output_host,today)
     f.SMF_Find_Critical(path,output_host,today)
     f.SMF_Find_Warning(path,output_host,today)
  else:
    start_date = v.smf_start_date
    end_date = v.smf_end_date
    fileList = f.DateRange(start_date, end_date,today)
    f.SMF_FilesDownload(hostname, path, fileList,output_host, psw)
    f.SMF_Find_Critical_Files(path,output_host, fileList)
    f.SMF_Find_Warning_Files(path,output_host, fileList)
  return None

SMF_Logs()



