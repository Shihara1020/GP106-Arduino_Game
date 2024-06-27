#import the inbuilt time module and random module
import random
import time
#import modules from Pyfirmata
from pyfirmata import Arduino,OUTPUT,INPUT,util
#Create an ardunio board instance
board=Arduino ("COM3")

#Create a array to store the summary of the game
summy=[]

#Set in digital pin number to indicate rock,paper,scissors,lizard and spock
Rock=board.digital[2]
Paper=board.digital[3]
Scissors=board.digital[4]
Lizard=board.digital[5]
spock=board.digital[6]
#Set up the these Led
for led in [Rock,Paper,Scissors,Lizard,spock]:
    led.mode=OUTPUT

#Set in digital pin number to indicate the score
#Score1 and Score2 represent the User score / Score3 and Score4 represent the computer score 
Score1=board.digital[7]
Score2=board.digital[8]
Score3=board.digital[9]
Score4=board.digital[10]
#Set up the these led
for score in [Score1,Score2,Score3,Score4]:
    score.mode=OUTPUT

#Set in digital pin number to indicate the start/end led
Start_end_Bulb=board.digital[11]
#Set up the led
Start_end_Bulb.mode=OUTPUT

#set in piezzor buzzer and set up 
piezzor=board.digital[12]
piezzor.mode=OUTPUT

#Set in switches for choices using analog pin
switch_rock=board.analog[4]
switch_paper=board.analog[3]
switch_scissors=board.analog[2]
switch_lizzard=board.analog[1]
switch_spock=board.analog[0]
for switch in [switch_rock,switch_paper,switch_scissors,switch_lizzard,switch_spock]:
    switch.enable_reporting()

#Switch for Start/end the game
Start_end_switch=board.digital[13]
Start_end_switch.mode=INPUT

it=util.Iterator(board)
it.start()

#Define the variable
round=0
Computer_score=0
User_score=0

#indicate state is true>led is on the game is begin
indicator_state=False
#calculate time
start_time=0

#==================================================Who is winner each round=========================================
def who_is_winner(user_select_element):
    global round,Computer_score,User_score
    #choise of compuetr 
    selected=["Rock","Paper","Scissors","Lizard","Spock"]
    computer_select_element=random.choice(selected)
    print("Computer choice:",computer_select_element)
    #Indicate the bulb(computer chioice)
    computer_leds={
        "Rock":Rock,
        "Paper":Paper,
        "Scissors":Scissors,
        "Lizard":Lizard,
        "Spock":spock
    }
    
    for led in [Rock,Paper,Scissors,Lizard,spock]:
        led.write(0)
    
    #led one corrosponding to computer choice
    computer_leds[computer_select_element].write(1)
    time.sleep(0.2)
    
    if computer_select_element==user_select_element:
        summy.append(["Round "+str(round),"User choise: "+user_select_element,"Computer choise: "+computer_select_element,f"The game is tie"])
        print("The game is tie...")
    else:
        win_conditions={
            "Rock":["Scissors","Lizard"],
            "Paper":["Rock","Spock"],
            "Scissors":["Paper","Lizard"],
            "Lizard":["Spock","Paper"],
            "Spock":["Rock","Scissors"]
        }
        if user_select_element in win_conditions[computer_select_element]:
            summy.append(["Round "+str(round),"user choise:"+user_select_element,"coumputer choice:"+computer_select_element,f"The winner is  coumputer"])
            Computer_score+=1
        else:
            summy.append(["Round "+str(round),"user choise:"+user_select_element,"computer choise:"+computer_select_element,f"The winner is user"])
            User_score+=1
    Score(User_score,Computer_score)

#======================================================================Indicate the score============================
def Score(User_score,Computer_score):
    print("User score:",User_score)
    print("Computer score:",Computer_score)
    
    for score in [Score1,Score2,Score3,Score4]:
        score.write(0)

    #display the user score
    if User_score==1:
        Score1.write(1)
    elif User_score==2:
        Score2.write(1)
    elif User_score==3:
        Score1.write(1)
        Score2.write(1)
    #display the coumputer score
    if Computer_score==1:
        Score3.write(1)
    elif Computer_score==2:
        Score4.write(1)
    elif Computer_score==3:
        Score3.write(1)
        Score4.write(1)
    

#=====================================next round founction===============================================================
def Go_nextt_round():
    global round,start_time
    #the indicater is blink and go next round
    for _ in range(5):
        Start_end_Bulb.write(0)
        time.sleep(0.5)
        Start_end_Bulb.write(1)
        time.sleep(0.5)
    #Buzzing
    buzz(0.5)

    for led in [Rock,Paper,Scissors,Lizard,spock]:
        led.write(0)
    round+=1
    start_time=time.time()
    print("Next Round is beginning ......")
    print("-----------------------------Round",round,'-----------------------------------------------')

#=================================End fuction======================================
def End_the_game():
    global round,Computer_score,User_score,round,summy,indicator_state
    print("End the game")
    Start_end_Bulb.write(0)
    indicator_state=False
    round=0
    if Computer_score>User_score:
        print("The winner is Coumpter")
    elif User_score>Computer_score:
        print("The winner is user")
    else:
        print("The game is tie")
    User_score=0
    Computer_score=0
    #----------------------
    #print("bilnk 5 led...............................................")
    for _ in range(10):
        for led in [Rock,Paper,Scissors,Lizard,spock]:
            led.write(0)
        time.sleep(0.5)
        for led in [Rock,Paper,Scissors,Lizard,spock]:
            led.write(1)
        time.sleep(0.5)
    
    print("Summry of the game...")
    print_score()
    summy=[]

    for score in [Score1,Score2,Score3,Score4]:
        score.write(0)
    for led in [Rock,Paper,Scissors,Lizard,spock]:
            led.write(0)

#=======================print score in terminal==================================================
def print_score():
    for i in summy:
        print(i)
#=================================pizzo buzzer======================================================
def buzz(duration):
    #print("Buzzing......")
    piezzor.write(1)
    time.sleep(duration)
    piezzor.write(0)


while True:
    if round ==8:
        buzz(0.8)
        End_the_game()

    if Computer_score==4 or User_score==4:
        buzz(0.8)
        End_the_game()

    #first check the press start button
    indicator_button_state=Start_end_switch.read()
    time.sleep(0.1)
    if indicator_button_state==True:
        if indicator_state==True:
            print("Ending the game........")
            #The game  is end
            buzz(1)
            End_the_game()
        else:
            #The game is start
            print("Starting the game......")
            indicator_state=True
            Start_end_Bulb.write(1)
            #variable define
            round=1
            print("Round",round)
            time.sleep(0.2)
            #first round time is begin
            start_time=time.time()
    if indicator_state==True:
        #then check user chhose the item in 3min
        if time.time()-start_time<=30:
            a=switch_lizzard.read()
            b=switch_paper.read()
            c=switch_rock.read()
            d=switch_scissors.read()
            e=switch_spock.read()
            if a is not None and b is not None and c is not None and d is not None and e is not None:
                if a>0.5:
                    Lizard.write(1)
                    time.sleep(0.5)
                    Lizard.write(0)

                    print("Your choice: Lizard")
                    print("waiting...")
                    time.sleep(10)
                    who_is_winner("Lizard")
                    Go_nextt_round()
                elif b>0.5:
                    Paper.write(1)
                    time.sleep(0.5)
                    Paper.write(0)

                    print("Your choice: paper")
                    print("Waiting....")
                    time.sleep(10)
                    who_is_winner("Paper")
                    Go_nextt_round()
                elif c>0.5:
                    Rock.write(1)
                    time.sleep(0.5)
                    Rock.write(0)

                    print("Youre choice: Rock")
                    print("waiting....")
                    time.sleep(10)
                    who_is_winner("Rock")
                    Go_nextt_round()
                elif d>0.5:
                    Scissors.write(1)
                    time.sleep(0.5)
                    Scissors.write(0)

                    print("Your choice: Scissors")
                    print("waiting...")
                    time.sleep(10)
                    who_is_winner("Scissors")
                    Go_nextt_round()
                elif e>0.5:
                    spock.write(1)
                    time.sleep(0.5)
                    spock.write(0)

                    print("your choice:  Spock")
                    print("waiting...")
                    time.sleep(10)
                    who_is_winner("Spock")
                    Go_nextt_round() 
        else:
            print("Time has passed....")
            summy.append(["Round "+str(round),"The time has passed",f"The winner is  coumputer"])
            Computer_score+=1
            Start_end_Bulb.write(0)
            buzz(1)
            Score(User_score,Computer_score)
            time.sleep(10)
            Go_nextt_round()
            Start_end_Bulb.write(1)
    