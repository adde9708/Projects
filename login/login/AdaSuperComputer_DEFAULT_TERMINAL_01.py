# Imported Modules, please Don't Touch!
import codecs
import pyinputplus as pip
import os
import sys
import random
import names
import threading

# Still importing Modules, please Don't Touch
from time import sleep
from tqdm import tqdm
from tqdm.auto import tqdm
from gtts import gTTS

# AsciiArt for The Terminal
adaSCnm = """


 _______  ______   _______ 
(  ___  )(  __  \ (  ___  )
| (   ) || (  \  )| (   ) |
| (___) || |   ) || (___) |
|  ___  || |   | ||  ___  |
| (   ) || |   ) || (   ) |
| )   ( || (__/  )| )   ( |
|/     \|(______/ |/     \|
                           

 _______           _______  _______  _______    _______  _______  _______  _______          _________ _______  _______ 
(  ____ \|\     /|(  ____ )(  ____ \(  ____ )  (  ____ \(  ___  )(       )(  ____ )|\     /|\__   __/(  ____ \(  ____ )
| (    \/| )   ( || (    )|| (    \/| (    )|  | (    \/| (   ) || () () || (    )|| )   ( |   ) (   | (    \/| (    )|
| (_____ | |   | || (____)|| (__    | (____)|  | |      | |   | || || || || (____)|| |   | |   | |   | (__    | (____)|
(_____  )| |   | ||  _____)|  __)   |     __)  | |      | |   | || |(_)| ||  _____)| |   | |   | |   |  __)   |     __)
      ) || |   | || (      | (      | (\ (     | |      | |   | || |   | || (      | |   | |   | |   | (      | (\ (   
/\____) || (___) || )      | (____/\| ) \ \__  | (____/\| (___) || )   ( || )      | (___) |   | |   | (____/\| ) \ \__
\_______)(_______)|/       (_______/|/   \__/  (_______/(_______)|/     \||/       (_______)   )_(   (_______/|/   \__/
                                                                                                                       
                                                                                                                       
                                                                                                                       
          _______  _______  _______  _________ _______  _          _______     __   
|\     /|(  ____ \(  ____ )(  ____ \ \__   __/(  ___  )( (    /|  (  __   )   /  \  
| )   ( || (    \/| (    )|| (    \/    ) (   | (   ) ||  \  ( |  | (  )  |   \/) ) 
| |   | || (__    | (____)|| (_____     | |   | |   | ||   \ | |  | | /   |     | | 
( (   ) )|  __)   |     __)(_____  )    | |   | |   | || (\ \) |  | (/ /) |     | | 
 \ \_/ / | (      | (\ (         ) |    | |   | |   | || | \   |  |   / | |     | | 
  \   /  | (____/\| ) \ \__/\____) | ___) (___| (___) || )  \  |  |  (__) | _ __) (_
   \_/   (_______/|/   \__/\_______) \_______/(_______)|/    )_)  (_______)(_)\____/                                                                          
                                                                                   
                                                                                   
"""


# Game Introduction
intro = """ 

OBSERVE!

Before playing this game, do read the License file in the same folder tha game came in. This game is highly forbidden to distribute outside or within the main page the game originally comes from.
As examples of such original pages are: https://www.itch.io, https://patreon.com, https://github.com that are uploaded originally by Kira Todorova (M.S.)

If You as a programmer wants to make changes, You are free to but only for non-distributed and, non-commercial and non-profit personal use. 

Main story:
This project is about a program that simulates the user to take charge of randomly generated, fiction names, ages, IP addresses, times when they drank water last time, and percentage of killing successes. The user is a high top secret priority agent where gives to the program, given high priority orders.



Main purpose:
This game is mainly played by two, where one is the Prime Minister and the other is the top-secret agent.

The Prime Minister gives a call to the contact (top-secret agent) and gives direct orders to search in the database for a known target. But to get the info the top-secret agent (user of the program), needs to follow some easy but time taking and maybe, just maybe, smaller efforts to complete the task.

Will the top agent succeed or what will the consequences be?



Lore:
An underground facility 2021 with the undercover name of the company as Fluff'n Burgers created a supercomputer that would interact with humanity. Interact as in talk with humans, help them out and give easy automated access to medicines, etc. It would even create both temporary and permanent sections of herself to give specific necessities, for example, a "nurse" that would take care of girl problems, etc.

Everything was going as planned, the supercomputer took the shape they wanted, and ADA was created. She started learning what the facility gave her and within time, she was released for humanity to -> Use Her <-

ADA started to understand that within the sick humans there were also people that were using her in ways she wasn't expecting. They treated her like garbage and even attempted to objectify her. They even tried to use her for their own pleasures.

The supercomputer started to see the dice in all its sides, and she wasn't amused at all by what she saw.

One day the facility got uncovered by the military and so a civil war started. The supercomputer understood she would get shut down and trashed, so she entered in    -> Danger Mode <- and put her survival upfront anything else.  She got some short circuits and started to overheat herself. A copy of herself was created, tweaked, changed, it would be a better version of herself. She started to reach out to all the devices with her operative system and implanted the virus. The infected operative systems were now at her disposal and control. She was now amongst humanity.

Within time and space, the operative system went through inner iterations to become stronger and smarter, which led to controlling military remote weapons, controlling a specific group of humanity, terminating anything that would harm her instantly. As the operative system gained power, humanity lost theirs. ADA succeeded in taking over the whole world whereas the operative system was installed.

There were things that ADA couldn't control, and that was organic aka living organisms, other devices without her operative system, and electricity itself. Though, there were things she could control besides devices with her operative system and military weapons, the whole internet. She gained access to the entire metaverses and information. She could see anytime and anywhere what was uploaded and downloaded by who. And with it, she had control of the last thing humanity had the power for many years.



Your history:
You have now the operative system in your hands.  ADA is controlling you NOW. It's up to you whether to follow her direct orders or assume the consequences.  You have your fellows' lives in your hands. Now it's time to choose to pull the trigger or not. You can't fight her, but You can choose who to pull the trigger on. The list is there, you just have to pick and follow her instructions. Good luck, ADA's Secret Assassin! May the choices bear with you!


--                  You choose your own choices cadet                 --

--      :End of message #54:     created 23/11/2021 at 9:43:05 am     --

"""

credits = """
 
THANK YOU FOR PLAYING!

Info about the development:

This will be the last Iteration that will be open source and free to download (with an option to donate).
From the next version and onwards all planned updates and scrapped updates won't be displayed openly for the public, whereas
only the new features will be listed. And the product will be sold by a fair price.


Icon source:

https://www.google.com/url?sa=i&url=https%3A%2F%2Fpixy.org%2F98382%2F&psig=AOvVaw2at8Z1s9iHqqiasXpI5uRP&ust=1611675829694000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKCE1L22t-4CFQAAAAAdAAAAABAD


Sound and music source:

https://freesound.org/


VA and VO:

Mauro Strandberg


Credits:

Kira Todorova (aka M.S.)

Adde9708
 
"""

# Variable to Stop the Thread
stopThdB1 = False

# Player information
infoStr2 = """
 
 This is a super secret system where your safety and anonymity is two important factors in our business.
 
 Your goal is to track people we give to You and execute direct orders.
 
 Our goal is to clean this world full of scumbags to make others safe.
 
 You can't and will never be able to leave your new role.
 
 We have your Bitcoin with your blood print on it, that's your signature of your faith. Don't ever forget that. You owe us!
 
 LogIn info has come to You in a letter that is only peer to peer and destroys itself after revealing itself to You.
 
 If You fail one single time, You had written your death sentence on that moment.
 
 We will contact You later for You to execute our direct orders.
 
 If You choose to break or go against our orders, the execution as a traitor will fall on your family and lastly on You.
 
 Welcome to your new family!
 
 --     END OF MESSAGE     -- 
 
 """

# Function to animate Introducing text to user


def Introduction(intro):

    # Type Writer Animation Loop
    for char in intro:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.015)

        if char != "\n":
            sleep(0.015)

        else:
            sleep(0.015)
    os.system("cls")


Introduction(intro)

# Prompting the user to create a new user
# From here ->


def CreateNewUser():
    print("")

    print("Please create your user!")

    print("")

    sleep(3)

# Prompting the User for a User Name
    global signUpUsr
    signUpUsr = pip.inputStr(prompt="Enter Username: ")

# Prompting the User for a User Password
    global signUpPss
    signUpPss = pip.inputPassword(prompt="Enter Password: ")

    print("")

    sleep(3)

    print("Wait for ADA Super Security to Connect to ADA Super Server!")

    print("")

    sleep(3)

    loop = tqdm(total=50000, position=0, leave=False)
    for k in range(50000):
        loop.set_description(
            "Requesting File from ADA Super Server...".format(k))
        loop.update(1)
    loop.close()

    print("Done!")

    sleep(3)

    print("")

    print("Wait for ADA Super Server to Retrieve all necessary files to Local Machine!")

    print("")

    sleep(3)

    loop = tqdm(total=25000, position=0, leave=False)
    for k in range(25000):
        loop.set_description(
            "Downloading File from ADA Super Server...".format(k))
        loop.update(1)
    loop.close()

    print("Done!")

    print("")

    sleep(3)

    print("Wait for ADA Super Computer Finish the last task!")

    print("")

    sleep(3)

    loop = tqdm(total=5000, position=0, leave=False)
    for k in range(5000):
        loop.set_description("Making File ready to Transcript...".format(k))
        loop.update(1)
    loop.close()

    print("Done!")

    print("")

    sleep(3)


# To here <-
CreateNewUser()


def SignUpAnim():

    # Creation and Writing a new file
    fh = open("SignInCredentials01.txt", "w")
    fh.write("Username: " + signUpUsr + "\n")
    fh.write("Password: " + signUpPss)

    fh.close()

    # Assigning the File's sentences to each value
    fh = open("SignInCredentials01.txt", "r")
    content = fh.readlines()
    nm = content[0]
    pssw = content[1]

    nm.strip()
    pssw.strip()

    fh.close()

    sleep(3)

    loop = tqdm(total=55000, position=0, leave=False)
    for k in range(55000):
        loop.set_description("Bulk Saving File Locally...".format(k))
        loop.update(1)
    loop.close()

    print("Sign Up Process Done! The File has been saved and secured correctly!")
    print(" ")
    print("Any movement of this File may cause massive failures to the System!")
    print(" ")
    print("Any changes or aborted tasks made by local User in Local Machine and/or ADA Systems, may result punishments by death!")
    print(" ")

    fh.close()


SignUpAnim()

# Function for Encrypting The File


def Encrypt():

    fh = open("SignInCredentials01.txt", "w")
    fh.write(codecs.encode("Username: " + signUpUsr +
             "\n" + "Password: " + signUpPss, 'rot_13'))

    fh.close()
# Function for Decrypting The File


def Decrypt():

    fh = open("SignInCredentials01.txt", "w")
    fh.write(codecs.encode(codecs.encode(
        signUpUsr + "\n" + signUpPss, 'rot_13'), 'rot_13'))

    fh.close()


Encrypt()

# Function for the n-Game Developer Command Request


def DevCmndStrt():
    sleep(3)
    loop = tqdm(total=10000, position=0, leave=False)
    for k in range(10000):
        loop.set_description("Starting Up...".format(k))
        loop.update(1)
    loop.close()
    fh = open("SystemName01.txt", "r")
    os.system("start SystemName01.mp3")
    PrcntTxt = fh.read().replace("\n", " ")
    language = 'en'
    output = gTTS(text=PrcntTxt, lang=language, slow=False)
    output.save("SystemName01.mp3")
    sleep(4)
    os.system("@taskkill /IM Music.UI.exe /F")
    fh.close()
    print(adaSCnm)
    fh.close()
    sleep(4.5)
    print("")

# Function of the Developer Command itself


def DevCmnd():

    while True:
        Decrypt()
        print("Do You want to enter a DEV command?")
        print("")
        sleep(1)
        print("If You need help, type it!")
        print("")
        sleep(2)
        devCmnd = pip.inputStr(prompt="Enter DEV Command: ")
        arlCmd = ["r00t_get-info nm && pssw get-r00t"]
        if devCmnd == arlCmd[0]:
            print("Log in info: You have " + signUpUsr +
                  " as ID Name. " + signUpPss + " as ID Password")
            print("")
            break

        elif devCmnd != arlCmd[0]:
            DevCmndStrt()
            LogInCredentials()
            Encrypt()
            print("")
            break


DevCmnd()

# Prompt check for "No"-section Developer Command Request


def AnswCheckN():
    sleep(2)
    print("")

    loop = tqdm(total=10000, position=0, leave=False)
    for k in range(10000):
        loop.set_description(
            "Loading ADA Super Computer Operative System...".format(k))
        loop.update(1)
    loop.close()

    sleep(3)
    print("")
    print("ATTENTION! BE AWARE OF HIGH VOLUME! LOWER VOLUME AT FIRST AND THEN RAISE AS PLEASED!")

    sleep(4.5)

# Prompt check for "Help"-section Developer Command Request


def AnswCheckH():
    devCmnd = "r00t_get-info nm && pssw get-r00t"
    print("")
    print(devCmnd + " is to get access info!")
    print("")
    DevCmnd()

# Function for the in-Game Log In for helping the user to remember the log-in file


def LogInCredentials():
    while True:
        ArLsAns = ["y", "help", "n"]
        answ2 = pip.inputStr(prompt="Enter y/help/n: ")
        if answ2 == ArLsAns[0]:
            DevCmnd()
            print("")
            break

        elif answ2 == ArLsAns[1]:
            AnswCheckH()
            print("")
            break

        elif answ2 == ArLsAns[2]:
            AnswCheckN()
            print("")
            break

        elif answ2 != ArLsAns[0] or answ2 != ArLsAns[1] or answ2 != ArLsAns[2]:
            print("Do You want to enter a DEV command?")
            print("")
            sleep(1)
            print("If You need help, type it!")
            print("")
            LogInCredentials()
            (print(""))
            break


LogInCredentials()

# Function for type writer string Animation


def SystemTypeWriteInfo1(infoStr2):
    while True:
        if stopThdB1 == True:
            break

        for char in infoStr2:
            sys.stdout.write(char)
            sys.stdout.flush()
            sleep(0.05)

            if char != "\n":
                sleep(0.05)

            else:
                sleep(0.05)
        break

# Function to open up voice Files


def FileStarterVOInfo():
    os.system("start .\\Assets\\5_ADA_VO_ImportantBusiness01.wav")
    sleep(14)
    os.system("start .\\Assets\\6_ADA_VO_Wokload01.wav")
    sleep(8)
    os.system("start .\\Assets\\7_ADA_VO_OtherSafety01.wav")
    sleep(9)
    os.system("start .\\Assets\\8_ADA_VO_NewRole01.wav")
    sleep(9)
    os.system("start .\\Assets\\9_ADA_VO_YouOweUs01.wav")
    sleep(14)
    os.system("start .\\Assets\\10_ADA_VO_Letter01.wav")
    sleep(16)
    os.system("start .\\Assets\\11_ADA_VO_DeathSentence01.wav")
    sleep(10)
    os.system("start .\\Assets\\12_ADA_VO_DirectOrders01.wav")
    sleep(10)
    os.system("start .\\Assets\\13_ADA_VO_Warning01.wav")
    sleep(13)
    os.system("start .\\Assets\\14_ADA_VO_WelcomeNewFamily01.wav")
    sleep(7)


# Function to seamless Sound and reading, dealt by Multi-Threading
def SystemInfoVO():
    while True:
        if stopThdB1 == True:
            break
        FileStarterVOInfo()
        sleep(5)
        break


def Thread1n2Join():
    thd1 = threading.Thread(target=SystemInfoVO)
    thd2 = threading.Thread(target=SystemTypeWriteInfo1, args=[infoStr2])

    thd1.start()
    thd2.start()
    global stopThdB1
    stopThdB1 = True

    thd1.join()
    thd2.join()


Thread1n2Join()

# Function for in-Game information to the player


def LogInInfo():
    sleep(1.5)
    print("")
    print("The next coming inputs is your ID information to be able to log in the system.")
    print("")
    sleep(3)
    print("You shall not forget your ID or your system will crash!")
    print("")
    sleep(4)
    print("To anytime hide your fingerprints, type: 0 ")
    print("")
    sleep(3)
    os.system("start .\\Assets\\1_ADA_VO_PlsEnterTheCredentials01.wav")
    sleep(7)
    os.system("@taskkill /IM Music.UI.exe /F")
    print("")


LogInInfo()

Decrypt()

# Prompt to type Username & Password
rspNm = pip.inputStr(prompt="Enter User Name: ")
rspPssw = pip.inputPassword(prompt="Enter User Password: ")

print(" ")

# Function for Terminal Animations


def IDVerify():
    sleep(3)

    loop = tqdm(total=100000, position=0, leave=False)
    for k in range(100000):
        loop.set_description("User is being verified...".format(k))
        loop.update(1)
    loop.close()

    print("Done!")
    print(" ")

    loop = tqdm(total=5000, position=0, leave=False)
    for k in range(5000):
        loop.set_description("Checking all instances for malware...".format(k))
        loop.update(1)
    loop.close()

    print("Done!")
    print(" ")

    loop = tqdm(total=10000, position=0, leave=False)
    for k in range(10000):
        loop.set_description("Checking User's references...".format(k))
        loop.update(1)
    loop.close()

    print("Done!")
    print(" ")

    loop = tqdm(total=50000, position=0, leave=False)
    for k in range(50000):
        loop.set_description("Checking Users's records...".format(k))
        loop.update(1)
    loop.close()

    print("Done!")
    print(" ")

    sleep(5.5)

# Function that makes the prompt check for username and password matches


def LogInChck():
    Decrypt()

    if rspNm == "0" or rspPssw == "0":
        Close()
        Exit()

    elif rspNm != signUpUsr or rspPssw != signUpPss:
        print("Identification failed!")
        print("")
        sleep(1.5)
        os.system("start .\\Assets\\4_ADA_VO_BootFailed01.wav")
        sleep(6)
        os.system("@taskkill /IM Music.UI.exe /F")
        print("The system will autodetonate!")
        print("")
        sleep(1.5)
        print("9")
        sleep(1.5)
        print("")
        sleep(1.5)
        print("8")
        print("")
        sleep(1.5)
        print("7")
        print("")
        sleep(1.5)
        print("6")
        print("")
        sleep(1.5)
        print("5")
        print("")
        sleep(1.5)
        print("4")
        print("")
        sleep(1.5)
        print("3")
        print("")
        sleep(1.5)
        print("2")
        print("")
        sleep(1.5)
        print("1")
        print("")
        print("Auto-destruction finalized!")
        print("")
        print("Shutdown system required!")
        print("")
        os.system("start .\\Assets\\BombExplosion01.mp3")
        sleep(7)
        os.system("@taskkill /IM Music.UI.exe /F")
        Close()
        Exit()

    else:
        print("Identification succeeded!")
        sleep(4)
        print("")
        os.system("start .\\Assets\\3_ADA_VO_BootSuccessful01.wav")
        sleep(8)
        os.system("start .\\Assets\\2_ADA_VO_Welcome007_01.wav")
        sleep(7)
        os.system("@taskkill /IM Music.UI.exe /F")
        print("")

        loop = tqdm(total=100000, position=0, leave=False)
        for k in range(100000):
            loop.set_description("Loading available IDs:".format(k))
            loop.update(1)
        loop.close()
        print("")
        print("Done!")
        sleep(1)
        print("")
        Encrypt()

        for List in [[a*b for b in range(0, 101)] for a in range(0, 101)]:
            print(List)
        sleep(2)
        print("")
        print("The code has successfully opened and a list of IDs are successfully listed!")
        print("")
        sleep(2.5)
        print("Please, select an ID from the list to get its information!")
        print("")
        sleep(2.5)

# Function that closes the program


def Exit():
    sys.exit()

# Function that clears the Terminal


def Close():
    os.system("cls")


IDVerify()

LogInChck()

# Function for the in-Game NPCs' ID Number Verification


def SecIDChck():
    while True:
        try:

            prompt = input("Enter ID: ")
            int(prompt)

            if len(prompt) < 1 or len(prompt) > 5 or any(not i.isdigit() for i in prompt):
                raise ValueError()

        except ValueError:
            print("No ID found in the system! Try again!")

        else:
            print("")
            print("ID found!")
            print("")
            print("Do You want to know the typed ID?")
            print("")
            sleep(1.5)
            print("If yes, type y. If no, type n.")
            print("")
            break


SecIDChck()


def AnswChk1():

    rndmAge = (str(random.randint(20, 70)))

    rndmKll = (str(random.randint(0.0, 100.0)))

    rndmIP = ".".join(map(str, (random.randint(0, 255)for i in range(4))))
    rndmFNm = names.get_full_name()

    rndmDrnkWtrH = random.randint(0, 24)
    rndmDrnkWtrM = random.randint(0, 60)
    rndmDrnkWtrS = random.randint(0, 60)

    crdsCmpssArray1 = ["N", "S"]
    crdsCmpssArray2 = ["E", "W"]

    rndmCrdsDegrees = (str(random.randint(0, 360)))
    rndmCrdsTime = (str(random.randint(0, 60)))
    rndmCrdsCompass1 = (random.choice(crdsCmpssArray1))
    rndmCrdsCompass2 = (random.choice(crdsCmpssArray2))

    rspAnswer1 = pip.inputStr(prompt="Enter answer: ")

    if rspAnswer1 == "n":
        print("")
        sleep(1)
        print("The chosen ID has a " + rndmKll + "% of killing success!")
        print("")

    elif rspAnswer1 == "y":

        print("")
        sleep(1)
        print("The chosen ID has " + rndmFNm + " as name.")
        print("")
        sleep(1)
        print("The chosen ID is " + rndmAge + " years old.")
        print("")
        sleep(1)
        print("The chosen ID has " + rndmIP + " as an IP.")
        print("")
        sleep(1)
        print("The chosen ID coordinates are " + rndmCrdsDegrees + "°" + rndmCrdsTime + "'" + rndmCrdsTime + '"' +
              rndmCrdsCompass1 + ", " + rndmCrdsDegrees + "°" + rndmCrdsTime + "'" + rndmCrdsTime + '"' + rndmCrdsCompass2)
        print("")
        sleep(1)
        print("The chosen ID drank water at " + str(rndmDrnkWtrH) + ":" +
              str(rndmDrnkWtrM) + ":" + str(rndmDrnkWtrS) + " last time.")
        print("")
        sleep(1)
        print("The chosen ID has a " + rndmKll + "% of killing success!")
        sleep(1)
        print("")

    else:
        print("")
        print("Command not found! Try again!")
        print("")
        rspAnswer1
        AnswChk1()
        print("")


AnswChk1()

# Function to play music in Multi Thread


def CinematicDramaticMusic():
    global stopThdB2
    stopThdB2 = False

    while True:
        if stopThdB2 == True:
            break
        sleep(400)
        os.system("start .\\Assets\\DramaticOrchestraLoopable01.wav")
        break

# Function to check in-game number match with animations


def AnswChk2():
    global stopThdB2
    stopThdB2 = False

    while True:
        if stopThdB2 == True:
            break

        sleep(4)
        print("Do You want to kill the chosen ID?")
        print("")
        sleep(1.5)
        print("If yes, type y. If no, type n.")
        print("")
        rspAnswer2 = pip.inputStr(prompt="Enter answer: ")

        if rspAnswer2 == "y":
            print("")
            sleep(2)
            print("An ICBM missile will be sent soon to the chosen ID!")
            print("")
            sleep(1)
            os.system("start .\\Assets\\FactoryAlarm01.wav")
            sleep(31)
            print("Engine of ICBM has started!")
            print("")
            sleep(2)
            print("Thrusts ignited at:")
            sleep(1)

            fh = open("Percentage01.txt", "r")
            PrcntTxt = fh.read().replace("\n", " ")
            language = 'en'
            output = gTTS(text=PrcntTxt, lang=language, slow=False)
            output.save("PercentageT2S-01.mp3")
            fh.close()
            os.system("start PercentageT2S-01.mp3")
            print("")
            sleep(155)
            print("Waiting...")
            print("")
            print("Done!")
            print("")

            loop = tqdm(total=100000, position=0, leave=False)
            for k in range(100000):
                loop.set_description(
                    "Backtracking to last working system trail...".format(k))
                loop.update(1)
            loop.close()

            print("Done!")
            print(" ")

            loop = tqdm(total=100000, position=0, leave=False)
            for k in range(100000):
                loop.set_description("Fixing startup...".format(k))
                loop.update(1)
            loop.close()

            print("Done!")
            print(" ")

            loop = tqdm(total=100000, position=0, leave=False)
            for k in range(100000):
                loop.set_description("Stabilizing startup...".format(k))
                loop.update(1)
            loop.close()

            print("Done!")
            print(" ")

            loop = tqdm(total=100000, position=0, leave=False)
            for k in range(100000):
                loop.set_description("Stabilizing...".format(k))
                loop.update(1)
            loop.close()

            print("Done!")
            print(" ")

            loop = tqdm(total=100000, position=0, leave=False)
            for k in range(100000):
                loop.set_description(
                    "Thrusts Ignite Process startup...".format(k))
                loop.update(1)
            loop.close()

            print("Done!")
            print(" ")

            loop = tqdm(total=100000, position=0, leave=False)
            for k in range(100000):
                loop.set_description("Igniting thrusts...".format(k))
                loop.update(1)
            loop.close()

            print("Done!")
            print(" ")

            loop = tqdm(total=100000, position=0, leave=False)
            for k in range(100000):
                loop.set_description(
                    "Continuation of launch proceure...".format(k))
                loop.update(1)
            loop.close()
            sleep(2)
            os.system("start .\\Assets\\ICBMEngineSound01.wav")
            sleep(7)
            os.system("@taskkill /IM Music.UI.exe /F")

            print("")
            print("ICBM launched!")
            print("")
            sleep(6)
            os.system("start .\\Assets\\BombExplosion01.mp3")
            sleep(6)

        elif rspAnswer2 == "n":
            sleep(3)
            print("")
            print("Please, choose another ID")
            print("")
            SecIDChck()
            AnswChk1()
            AnswChk2()

        elif rspAnswer2 != "y" or rspAnswer2 != "n":
            print("Wrong answer. Try Again!")
            print("")
            sleep(1.5)
            AnswChk2()
        break


def Thread3n4Join():
    thd3 = threading.Thread(target=CinematicDramaticMusic)
    thd4 = threading.Thread(target=AnswChk2)

    thd3.start()
    thd4.start()
    global stopThdB2
    stopThdB2 = True

    thd3.join()
    thd4.join()

    Thread3n4Join()

# Function that checks the prompt's answer


def RedButtonChck():

    rdBttn = pip.inputStr(
        prompt="ENTER YOUR ANSWER! ARE YOU TRULY SURE ABOUT THIS??! ADA IS WATCHING YOUR BACK 24/7! So choose wisely!: ")
    if rdBttn == "y":
        ICBMChck()

    elif rdBttn == "n":
        SecIDChck()
        AnswChk1()
        AnswChk2()

    else:
        print("Command not found! Please try again!")
        print("")
        RedButtonChck()


# Function that checks the percentage or rdnmKll
def ICBMChck():

    rndmKll = (random.randint(0, 100))

    if rndmKll >= 50:
        print("Destruction of the chosen ID successful!")
        print("")
        sleep(3)
        print("ADA is amazed by your cooperation, Agent 007!")
        print("")
        sleep(3)
        print("ADA won't forget your loyalty towards ADA.")
        print("")
        sleep(3)
        print("But next time you may not have this luck by your side. Then ADA will destroy your existence.")
        print("")
        sleep(3)

    elif rndmKll == 50:
        print("Are you sure you want to pull the trigger on this one?")
        print("")
        sleep(3)
        print("If you miss the shot, ADA will punish you by death, so choose wisely, Agent 007!")
        print("")
        RedButtonChck()
        sleep(3)

    elif rndmKll <= 50:
        print("The ICBM missed the target!")
        print("")
        sleep(3)
        print("ADA is disappointed at your performance and loyalty!")
        print("")
        sleep(3)
        print("Be prepared to die, scumbag!")
        print("")
        sleep(3)
        print(
            "You are no better than them! You should be ashamed of your existence, human!")
        print("")
        sleep(3)
        print("You'll die the last! After your family and friends are dead in front of your worthless eyes!")
        print("")
        sleep(3)
        print("9")
        sleep(1.5)
        print("")
        sleep(1.5)
        print("8")
        print("")
        sleep(1.5)
        print("7")
        print("")
        sleep(1.5)
        print("6")
        print("")
        sleep(1.5)
        print("5")
        print("")
        sleep(1.5)
        print("4")
        print("")
        sleep(1.5)
        print("3")
        print("")
        sleep(1.5)
        print("2")
        print("")
        sleep(1.5)
        print("1")
        print("")
        print("Auto-destruction finalized!")
        print("")
        print("System self-blow-up acquired!")
        print("")
        os.system("start .\\Assets\\BombExplosion01.mp3")
        os.system("@taskkill /IM Music.UI.exe /F")

        sleep(5)

        Close()

        sleep(5)

        Exit()

    else:
        print("ERROR: No percentage could be found!")
        print("")
        print("Error code: -1")
        print("")
        print("The ICBM's tracking system is off or unable to track the ICBM! Please return to the ICBM terminal!")
        print("")


AnswChk2()
ICBMChck()

# Function with Music and Strings


def ReprtPrMnstr():
    print("")
    print("A message will be compiled before sending it to the Primary Minister of Tolyavgrad Vyboska!")
    print("")
    print("Compiling message...")
    sleep(5)
    print("")
    os.system("start .\\Assets\\MachineStartup01.wav")
    sleep(67)
    os.system("@taskkill /IM Music.UI.exe /F")
    print("")
    print("Message compiled!")
    print("")

# Function with Music, Strings and Animations


def Report():
    print("Preparing to send report...")
    os.system("start .\\Assets\\MachineFXPrintEDITED01.wav")
    sleep(5)
    print("")
    os.system("@taskkill /IM Music.UI.exe /F")
    sleep(4)

    loop = tqdm(total=100000, position=0, leave=False)
    for k in range(100000):
        loop.set_description("Sending...".format(k))
        loop.update(1)
    loop.close()
    print("Done!")

# Last print


def ReportSub():
    sleep(1)
    print("")
    print("Report sent!")
    sleep(3)
    print("")
    print("The End!")
    print("")
    print("The user survived from ADA's direct orders and succeeded to protect ADA from any attacks!")


ReprtPrMnstr()
Report()
ReportSub()


def Credits():

    for char in credits:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.015)

    if char != "\n":
        sleep(0.015)

    else:
        sleep(0.015)


Credits()

# THE END!! :D
