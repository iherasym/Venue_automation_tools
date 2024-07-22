import datetime

today=datetime.datetime.now().strftime("%Y%m%d")
hostname = input("Enter IP address for your server: ")
password = input("Enter password for your server: ")
smf_optons = input("Please choose SMF date TODAY_LOG or MULTILE_DAYS: ")
if smf_optons != "TODAY_LOG":
   smf_start_date = input("Please enter start date for smf log: ")
   smf_end_date = input("Please enter end date for smf log : ")
Log_path = "C:\\Users\\U6017127\\PycharmProjects\\HerasiMor_Framework\\Logs\\"