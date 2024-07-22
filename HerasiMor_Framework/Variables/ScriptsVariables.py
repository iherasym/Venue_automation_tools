import datetime

today=datetime.datetime.now().strftime("%Y%m%d")
hostname = input("Enter IP address for your server: ")
password = input("Enter password for your server: ")
LH_name = input("Enter LH names divaded by space: ")
Venue_Type = input("Please enter venue type ATLAS or TD: ")
smf_optons = input("Please choose SMF date TODAY_LOG or MULTILE_DAYS: ")
smf_start_date = input("Please enter start date for smf log: ")
smf_end_date = input("Please enter end date for smf log : ")
Nic_Cards = input("Please provide NIC Card to block: DDN or EXCH?: ").upper()
Protocols = input("Please provide protocol you want to block UDP, TCP, BOTH: U,T,B: ").upper()
Nic_Side = input("Please specify which NIC card you want to block: A, B or All ").upper()
Persist_Type = input("Plese choose persist between DAT or LOADED: ")
Pcap_lenght = input("please enter pcap length you want to capture: ")
PortBlocker_lenght = input("Please enter time you want to block the ports in seconds: ")
log_path = "C:\\Users\\U6017127\\PycharmProjects\\HerasiMor_Framework\\Logs"
tools_path = "C:\\Users\\U6017127\\PycharmProjects\\HerasiMor_Framework\Tools"










