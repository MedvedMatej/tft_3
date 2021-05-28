import subprocess #open LeagueClient
import psutil #access list of processes
import time

class Client:
    @staticmethod
    def is_client_open():
        for proc in psutil.process_iter():
            try:
                if proc.name() == u"LeagueClient.exe":
                    return True
            except psutil.AccessDenied:
                print("Permission error or access denied on process")
        
        return False
    
    @staticmethod
    def launch_client(location,client_active=False):
        print("Opening LeagueClient")
        while(not client_active):
                subprocess.Popen(location)
                print(".",end = '')
                time.sleep(15)
                client_active = Client.is_client_open()

    @staticmethod
    def kill_client():
        kill = {"LeagueClient.exe","League of Legends.exe","RiotClientServices.exe"}

        for proc in psutil.process_iter():
            try:
                if proc.name() in kill:
                    subprocess.call(["taskkill","/F","/IM",proc.name()])
            except psutil.AccessDenied:
                print("Permission error or access denied on process")