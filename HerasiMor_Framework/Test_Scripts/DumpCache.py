import Functions.AutomationFunctions as f
import Variables.DumpCache_Variables as d
import os


def DumpCache_RICs():
  hostname = d.hostname
  password = d.password
  LH_name = d.LH_name
  LH_name = LH_name.split()
  type = d.Venue_Type
  output_host = f.output_host(hostname,password)
  local_path = f"{d.log_path} {output_host}\\"
  os.makedirs(local_path, exist_ok=True)
  today = d.today
  fo4 = open(local_path + "Sample_RICs.txt", "w")
  fo4.write(f"Sample RICs for:\n\n")
  fo4.close()
  for LH in LH_name:
    if type == "ATLAS":
      dumpcache_file = f.download_dumpcache_atlas(hostname, password, LH, local_path, today, output_host)
      CID = f.find_CID_dumpcache(local_path, dumpcache_file)
      f.sample_RIC_per_CID(type, local_path, dumpcache_file, CID, LH)
    elif type == "TD":
      dumpcache_file = f.download_dumpcache(hostname, password, LH, local_path, today, output_host)
      CID = f.find_CID_dumpcache(local_path, dumpcache_file)
      f.sample_RIC_per_CID(type, local_path, dumpcache_file, CID, LH)
  os.remove(local_path + "new_dump_file.csv")


DumpCache_RICs()