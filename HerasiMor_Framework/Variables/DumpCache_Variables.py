import datetime

today=datetime.datetime.now().strftime("%Y%m%d")
hostname = input("Enter IP address for your server: ")
password = input("Enter password for your server: ")
LH_name = input("Enter LH names divaded by space: ")
log_path = "C:\\Users\\U6017127\\PycharmProjects\\HerasiMor_Framework\\Logs\\"
Venue_Type = input("Please enter venue type ATLAS or TD: ")