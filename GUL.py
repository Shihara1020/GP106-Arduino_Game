from pyfirmata import Arduino,OUTPUT,INPUT,util
import tkinter as tk
from tkinter import ttk
import time
import random
from tkinter import messagebox
board=Arduino ("COM3")
#===============================================Definied the led pin,button and pizzo================================
#Indicate the choice of compute using 5 five led
Rock=board.digital[2]
Paper=board.digital[3]
Scissors=board.digital[4]
Lizard=board.digital[5]
spock=board.digital[6]
for led in [Rock,Paper,Scissors,Lizard,spock]:
    led.mode=OUTPUT
#--------------------------------------------------------------------------------------------

#Indicate the score of user
Score1=board.digital[7]
Score2=board.digital[8]
Score3=board.digital[9]
Score4=board.digital[10]
for score in [Score1,Score2,Score3,Score4]:
    score.mode=OUTPUT
#------------------------------------------------------------------------------------------

#Indicate the End/start/Round
Start_end_Bulb=board.digital[11]
Start_end_Bulb.mode=OUTPUT
#-----------------------------------------------------------------------------------------

#piezzor buzzer
piezzor=board.digital[12]
piezzor.mode=OUTPUT

#------------------------------------------------------------------------------------------

#switch for choices
switch_rock=board.analog[4]
switch_paper=board.analog[3]
switch_scissors=board.analog[2]
switch_lizzard=board.analog[1]
switch_spock=board.analog[0]

for switch in [switch_rock,switch_paper,switch_scissors,switch_lizzard,switch_spock]:
    switch.enable_reporting()
#-----------------------------------------------------------------------------------------

#Start/end the game
Start_end_switch=board.digital[13]
Start_end_switch.mode=INPUT
#===============================================================================================================

it=util.Iterator(board)
it.start()

#======================================================Who is winner function========================================
def who_is_winner(user_select_element):
    global round,Computer_score,User_score,selected
    #choise of compuetr 
    selected=["Rock","Paper","Scissors","Lizard","Spock"]
    computer_select_element=random.choice(selected)
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
    
    computer_leds[computer_select_element].write(1)
    #----------------------------------------------------------------------------------------------------------  
    time.sleep(0.2)
    result=""
    if computer_select_element==user_select_element:
        result="The game is a tie....."
        winner="Tie"
    else:
        win_conditions={
            "Rock":["Scissors","Lizard"],
            "Paper":["Rock","Spock"],
            "Scissors":["Paper","Lizard"],
            "Lizard":["Spock","Paper"],
            "Spock":["Rock","Scissors"]
        }
        if user_select_element in win_conditions[computer_select_element]:
            Computer_score+=1
            result="Computer win"
            winner="Computer"
        else:
            User_score+=1
            result="You win"
            winner="Player"
    
    #add choices for the table(GUI) 
    Game_page_lb.config(text=f"Computer chose: { computer_select_element}\nYour chose:{user_select_element}\n{result}")
    table.insert('',tk.END, values=(round, user_select_element,computer_select_element, winner),)
    root.update()
    Score(User_score,Computer_score)
#=========================================================================================================


#====================================diplay the user score and computer score=============================
def Score(User_score,Computer_score):
    #Turn off the all leds
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
    #Update the user score and computer score for GUI    
    label_scores.config(text=f"Player Score: {User_score}\nComputer Score: {Computer_score}")
    root.update()



#=================================Go next round function========================================
def Go_nextt_round():
    global round,start_time
    #blink the 5 leds
    for _ in range(5):
        Start_end_Bulb.write(0)
        time.sleep(0.5)
        Start_end_Bulb.write(1)
        time.sleep(0.5)
    Start_end_Bulb.write(1)
    buzz(0.5)
    for led in [Rock,Paper,Scissors,Lizard,spock]:
        led.write(0)

    round+=1
    Round.config(text='Round  ' + str(round))
    root.update()
    waiting()
    start_time=time.time()
#=============================================waiting function===============================
def waiting():
    Game_page_lb.config(text="You can choise now...")
    rocklabel.config(state="disabled")
    paperlabel.config(state="disabled")
    scissorslabel.config(state="disabled")
    Lizardlabel.config(state="disabled")
    Spocklabel.config(state="disabled")
    root.update()

#========================================END the game==========================================
def End_the_game():
    global Computer_score,User_score,indicate_state
    #print("Restart the game")
    Game_page_lb.config(text="Game End")
    rocklabel.config(state="disabled")
    paperlabel.config(state="disabled")
    Spocklabel.config(state="disabled")
    Lizardlabel.config(state="disabled")
    scissorslabel.config(state="disabled")
    root.update()
    #turn off the start button
    Start_end_Bulb.write(0)
    indicate_state=False
    #blink the 5 leds
    for _ in range(10):
        for led in [Rock,Paper,Scissors,Lizard,spock]:
            led.write(0)
        time.sleep(0.5)
        for led in [Rock,Paper,Scissors,Lizard,spock]:
            led.write(1)
        time.sleep(0.5)
    #Display the massege who is winner    
    if Computer_score==User_score:
        messagebox.showinfo("who is winner","Good game the game is tie")
    elif Computer_score<User_score:
        messagebox.showinfo("who is winner","Good game the game is win you  happy")
    elif Computer_score>User_score:
        messagebox.showinfo("who is winner","Hard luck the game is lost")
    #turn off the bulb
    for score in [Score1,Score2,Score3,Score4]:
        score.write(0)
    for led in [Rock,Paper,Scissors,Lizard,spock]:
            led.write(0)
    reset_game()

# Function to reset the game
def reset_game():
    global Computer_score,User_score,round
    round=1
    Computer_score= 0
    User_score = 0
    Game_page_lb.config(text="Please press the start button to start the game")
    Round.config(text='The Game is starting')
    label_scores.config(text="Player Score: 0 \nComputer Score: 0")
    for i in table.get_children():
        table.delete(i)
    root.update()
#===============================buzzing==============================
def buzz(duration):
    piezzor.write(1)
    time.sleep(duration)
    piezzor.write(0)

#================================start the game=========================
def start_the_game():
    global round,indicate_state,Computer_score,User_score,start_time,selected
    #define the variable
    indicate_state=False
    Computer_score=0
    User_score=0
    round=1

    while True:
        root.update()
        if Computer_score==4 or User_score==4:
            buzz(0.8)
            End_the_game()
        if round ==8:
            buzz(0.8)
            End_the_game()
        #read the start end switch
        button_state = Start_end_switch.read()
        time.sleep(0.1)

        if button_state==True:
            if indicate_state==True:#the led is one-->the game is end
                #The game  is end
                buzz(0.8)
                End_the_game()
            else:
                #The game is start
                indicate_state=True
                Start_end_Bulb.write(1)
                #variable define
                time.sleep(0.2)
                Game_page_lb.configure(text="The Game is begining...")
                Round.config(text="Round 1")
                root.update()
                time.sleep(5)
                waiting()
                #first round time is begin
                start_time=time.time()
                
        if indicate_state==True:
            if time.time()-start_time<=30:
                a=switch_lizzard.read()
                b=switch_paper.read()
                c=switch_rock.read()
                d=switch_scissors.read()
                e=switch_spock.read()
                if a is not None and b is not None and c is not None and d is not None and e is not None:
                    if a>0.5:
                        Lizardlabel.config(state="normal")
                        Game_page_lb.config(text="Please waiting to computer choice the item..")
                        root.update()
                        Lizard.write(1)
                        time.sleep(0.5)
                        Lizard.write(0)
                        
                        time.sleep(5)
                        who_is_winner("Lizard")
                        Go_nextt_round()

                    elif b>0.5:
                        paperlabel.config(state="normal")
                        Game_page_lb.config(text="Please waiting to computer choice the item..")
                        root.update()

                        Paper.write(1)
                        time.sleep(0.5)
                        Paper.write(0)

                        time.sleep(5)
                        who_is_winner("Paper")
                        Go_nextt_round()

                    elif c>0.5:
                        rocklabel.config(state="normal")
                        Game_page_lb.config(text="Please waiting to computer choice the item..")
                        root.update()

                        Rock.write(1)
                        time.sleep(0.5)
                        Rock.write(0)

                        time.sleep(5)
                        who_is_winner("Rock")
                        Go_nextt_round()

                    elif d>0.5:
                        scissorslabel.config(state="normal")
                        Game_page_lb.config(text="Please waiting to computer choice the item..")
                        root.update()
                        Scissors.write(1)
                        time.sleep(0.5)
                        Scissors.write(0)

                        time.sleep(5)
                        who_is_winner("Scissors")
                        Go_nextt_round()

                    elif e>0.5:
                        Spocklabel.config(state="normal")
                        Game_page_lb.config(text="Please waiting to computer choice the item..")
                        root.update()

                        spock.write(1)
                        time.sleep(0.5)
                        spock.write(0)

                        time.sleep(5)
                        who_is_winner("Spock")
                        Go_nextt_round()
            else:
                #the time is passed
                Start_end_Bulb.write(0)
                buzz(0.5)
                Computer_score+=1
                #inside the table
                computer_select_element=random.choice(selected)
                Game_page_lb.config(text=f"Computer chose: { computer_select_element}\nYour chose:Time has passed\nComputer win")
                table.insert('',tk.END, values=(round, "Time has passed",computer_select_element,"Computer win"),)
                root.update()

                Score(User_score,Computer_score)
                time.sleep(5)
                Go_nextt_round()
                Start_end_Bulb.write(1)

        time.sleep(0.2)

#=========================================================GUI======================================================== 
root = tk.Tk()
#size of the user inter face
root.geometry("900x900")
root.title("Mini Game")
root.resizable(False,False)
root.configure(bg="#f0f0f0")

#Round number
round_count=1
#Title of the game
title = tk.Label(root, text="Scissors Paper Rock Spock Lizard Game", font=("Arial", 15), bg="#0097e8", fg="white")
title.pack()
#space=tk.label(root,text="")
#space.pack()
#display the round
Round=tk.Label(root, text='The Game is starting', fg="#0097e8", font=("Arial", 13))
Round.pack(pady=20)
#Create the header
Game_page_lb=tk.Label(root, text="Please press the start button to start the game", fg="#0097e8", font=("Arial", 8))
Game_page_lb.pack(pady=10)

#-------------------------------------choices list---------------------------------------
rocklabel=tk.Label(root, text="Rock - Press button 1", font=("Arial", 8))
rocklabel.pack(pady=5)
paperlabel=tk.Label(root, text="Paper - Press button 2", font=("Arial", 8))
paperlabel.pack(pady=5)
scissorslabel=tk.Label(root, text="Scissors - Press button 3", font=("Arial", 8))
scissorslabel.pack(pady=5)
Lizardlabel=tk.Label(root, text="Lizard - Press button 4", font=("Arial", 8))
Lizardlabel.pack(pady=5)
Spocklabel=tk.Label(root, text="Spock - Press button 5", font=("Arial", 8))
Spocklabel.pack(pady=5)
#--------------------------------------------------------------------------------------------
label_scores =  tk.Label(root, text=f"Player Score: 0 \nComputer Score: 0", font=("Arial", 10))
label_scores.pack(pady=5)
table = ttk.Treeview(root, columns=('Round', 'Player Choice', 'Computer Choice', 'Winner'),show="headings")

#-------------------------------------create a table-------------------------------------------
table.heading("Round",text='Round')
table.heading("Player Choice",text='Player Choice')
table.heading("Computer Choice",text='Computer Choice')
table.heading("Winner",text='Winner')
table.pack()

#call the start game
start_the_game()
root.mainloop()