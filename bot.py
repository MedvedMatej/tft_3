#version 3.00
import time
from threading import Thread
from keyboardInput import press_key , D, E, F, Enter, Slash
from capture import screenCapture
from mouseInput import click

from client import Client
from vision import Vision
import random

class Tft_bot:
    def __init__(self):
        #Location for starting the client in case it's not open or we have to restart it
        self.client_location = 'C:\\Riot Games\\League of Legends\\LeagueClient.exe'
        
        #Variables for the base game loop
        self.curr_stage = 2
        self.next_stage = 3
        self.stages = {
            0: "Play_button",
            1: "Tft_select",
            2: "Find_match",
            3: "Accept_button",
            4: "Ingame",
            5: "Exit_button",
            6: "Find_match",
        }

        #Variables for ingame actions
        self.champs ="Sentinel"
        self.last_action = time.time()
        self.kliker = 0
        self.fix = time.time()

    def stage_increase(self):
        print("Povečujem iz",self.stages[self.curr_stage],"na",self.stages[self.next_stage])
        self.curr_stage = self.next_stage
        self.next_stage += 1
        if(self.next_stage > 6): self.next_stage = 2


    def stage_reset(self):
        self.curr_stage = 0
        self.next_stage = 1

    def main_game_loop(self):
        
        haystack = screenCapture.screen_shot()
        x1,y1 = Vision.locateOnScreen("ClientImages/{}.png".format(self.stages[self.next_stage]),haystack)
        if x1:
            Bot.last_action = click(x1,y1+10)
            self.stage_increase()
            self.kliker = 0

        x,y = Vision.locateOnScreen("ClientImages/{}.png".format(self.stages[self.curr_stage]),haystack)
        if x and self.curr_stage != 4:
            pass
            Bot.last_action = click(x,y+10)
            self.kliker = self.kliker +1



        #In case the bot wins
        if self.curr_stage == 4:
            x2,y2 = Vision.locateOnScreen("ClientImages/{}.png".format("Find_match"),haystack)
            if x2 :
                click(x2,y2+10)   
                self.stage_increase()      
                self.stage_increase()

        global is_main_loop_in_action
        is_main_loop_in_action = False
            
    def shop_for_champs(self):
        img = screenCapture.screen_shot()[925:1040, 475:1480]   

        loc = Vision.locateAllOnScreen("Champs/"+self.champs+".png",img)

        #Buy champs
        for x,y in loc:
            #print(pos)
            Bot.last_action = click(x+70,y-5)
            
            #Bot.last_action = click(x+30,y)
            time.sleep(0.4)

        #Need sleep or the clicks don't happen in time
        time.sleep(0.5)
        

is_main_loop_in_action = False

if __name__ == "__main__":
    Bot = Tft_bot()
    client_active = Client.is_client_open()

    if not client_active:
        Client.launch_client(Bot.client_location,client_active)
        Bot.stage_reset()
    
    """ Bot.curr_stage = 4
    Bot.next_stage = 5 """
    #Bot.stage_reset()

    while True:
        #print(time.time()-Bot.last_action)        
        print(10 - Bot.kliker)
        if time.time() - Bot.last_action > 900:
            print("No actions taken: restarting client")
            Client.kill_client()
            time.sleep(15)
            Client.launch_client(Bot.client_location)
            Bot.stage_reset()
            Bot.last_action = time.time()
            Bot.kliker = 0


        if Bot.kliker >= 10:
            Client.kill_client()
            time.sleep(15)
            Client.launch_client(Bot.client_location)
            Bot.stage_reset()
            Bot.last_action =time.time()
            Bot.kliker = 0

        if not is_main_loop_in_action:
            is_main_loop_in_action = True
            t = Thread(target=Bot.main_game_loop())
            t.start()
        
        
        if Bot.curr_stage == 4:
            time.sleep(1)   
            Bot.shop_for_champs()
            

            #in case you win
            haystack = screenCapture.screen_shot()
            x1,y1 = Vision.locateOnScreen("ClientImages/{}.png".format("ok_button"),haystack)
            if x1 :
                Bot.last_action = click(x1,y1+10)
            x,y = Vision.locateOnScreen("ClientImages/{}.png".format("Find_match"),haystack)
            if x :
                Bot.last_action = click(x,y+10)
                Bot.curr_stage = 2
                Bot.next_stage = 3

        #check for completed missions
        if Bot.curr_stage == 5:
            haystack = screenCapture.screen_shot()
            x,y = Vision.locateOnScreen("ClientImages/{}.png".format("ok_button"),haystack)
            if x :
                Bot.last_action = click(x,y+10)