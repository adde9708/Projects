from time import sleep
import pyinputplus as pip
import os
import sys
import random
import names
from tqdm import tqdm
from gtts import gTTS

print("")
print("Do You want to enter a DEV command?")
print("")
print("If You need help, type it!")
print("")

# If You wanna change both "Nm" and "Pssw"; push Ctrl F, to Find them.
# Afterwards, change "Name" and "Password" to what You want.
# Push Ctrl F again, to find "rspNm" and "rspPssw" to what You want.
# If You find any issues; send me an email at:
# mauro.strandberg@gmail.com and I'll try to help C:


nm = "Name"
pssw = "Password"

answ = pip.inputStr(prompt="Enter y/help/n: ")
if answ == "y":
    dev_cmnd = pip.inputStr(prompt="Enter DEV Command: ")

elif answ == "help":

    print("")
    dev_cmnd = "r00t_get-info Nm && Pssw get-r00t"
    print(dev_cmnd + " is to get access info!")
    print("")
    dev_cmnd = pip.inputStr(prompt="Enter DEV Command: ")

    if dev_cmnd == "r00t_get-info Nm && Pssw get-r00t":
        print("Log in info: You have " + nm + " as ID Name. " + pssw + " as ID Password")

elif answ == "n":

    print("")
    print("ATTENTION! BE AWARE OF HIGH VOLUME! LOWER VOLUME AT FIRST AND THEN RAISE AS PLEASED!")
    sleep(5)
    print("")

    with open("SystemName01.txt", "r") as fh:
        prcnt_txt = fh.read().replace("\n", " ")
        language = 'en'
        output = gTTS(text=prcnt_txt, lang=language, slow=False)
        output.save("SystemName01.mp3")

    os.system("start SystemName01.mp3")
    sleep(4.1)
    os.system("taskkill /IM Music.UI.exe /F")


def system_intro():
    sleep(2.5)
    print("")
    print("")
    print("ADA SUPERCOMPUTER v.0.1")
    print("")
    print("")
    sleep(1.2)
    print("This is a super secret system where Your safety and annonymity is two important factors in out business.")
    print("")
    print("Your work is to track pople we give to You and execute direct orfers.")
    print("")
    print("Our goal is to clean this world full of scumbags to make other's safe.")
    print("")
    print("You can't and will never be able to leave Your workplace.")
    print("")
    print("We have Your Bitcoin with Your bloodprint on it, that's Your signature of Your faith. Don't ever forget that. You owe us!")
    print("")
    print("LogIn info has come to You on a letter that is only per to per and destroys itself after reavealing itself to You.")
    print("")
    print("If You fail one single time, You had written Your death sentence on that moment.")
    print("")
    print("We will contact You later for You to execute our orders.")
    print("")
    print("If You choose to break or go against our orders, the execution as traitor will fall on Your family and lastly You.")
    print("")
    print("Welcome to Your new family!")
    print("")
    print("")
    sleep(1.5)
    print("--     END OF MESSAGE     -- ")
    print("")
    print("")


system_intro()


def log_in_info():
    sleep(1.5)
    print("The next coming inputs is Your ID information to be able to log in the system.")
    print("")
    print("You shall not forget Your ID or Your system will crash!")
    print("")
    sleep(1.5)
    print("To anytime hide Your fingerprints, type: 0 ")
    print("")


log_in_info()

rsp_nm = pip.inputStr(prompt="Enter ID Name: ")
rsp_pssw = pip.inputPassword(prompt="Enter ID Password: ")


def id_verify():
    sleep(3)
    print("")
    print("ID is being verified!")
    print("")
    sleep(2.5)
    print("25%")
    print("")
    sleep(2.5)
    print("50%")
    print("")
    sleep(2.5)
    print("75%")
    print("")
    sleep(2.5)
    print("100%")
    print("")
    sleep(1)
    print("Done.")
    sleep(1.5)
    print("")


id_verify()


def ext():
    sys.exit()


def cls():
    os.system("cls")


if rsp_nm == "0":
    cls()
    ext()

elif rsp_nm != nm or rsp_pssw != pssw:

    sleep(3.5)
    print("Identification failed!")
    print("")
    sleep(1.5)
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
    print("Autodestruction finalized!")
    print("")
    print("Shutdown system required!")
    print("")
    cls()
    ext()
else:
    sleep(3.5)
    print("Identification succeeded!")
    sleep(4)
    print("")
    sleep(2)
    print("Loading avaliable IDs!")
    print("")
    sleep(2)

    loop = tqdm(total=100000, position=0, leave=False)
    for k in range(100000):
        loop.set_description("Showing avaliable IDs".format(k))
        loop.update(1)
    loop.close()
    print("")
    sleep(1)

    for List in [[a * b for b in range(-101, 101)] for a in range(-101, 101)]: print(List)
    sleep(2)
    print("")
    print("The code has succesfully opened!")
    print("")
    sleep(2.5)
    print("Check for the personal ID Your are looking for!")
    print("")
    sleep(2.5)

prompt = pip.inputStr(prompt="Enter ID: ")

print("")

num_lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

while True:

    if (len(prompt) < 1 or len(prompt) > 5 and not num_lst[0]
            and not num_lst[1] and not num_lst[2]
            and not num_lst[3] and not num_lst[4]
            and not num_lst[5] and not num_lst[6]
            and not num_lst[7] and not num_lst[8]
            and not num_lst[9]):

        print("ID not Found!")
        print("")
        print("Try with another ID!")
        print("")
        print(prompt)

    else:
        print("Do You want to know the typed ID?")
        print("")
        sleep(1.5)
        print("If yes, type y. If no, type n.")
        rsp_answer1 = pip.inputStr(prompt="Enter answer: ")

        rndm_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        rndm_fnm = names.get_full_name()
        rndm_drnk_wtr_h = random.randint(0, 24)
        rndm_drnk_wtr_m = random.randint(0, 60)
        rndm_drnk_wtr_s = random.randint(0, 60)
        break


def answ_chk1():
    if rsp_answer1 == "n":
        rndm_kll = (str(random.uniform(0.0, 100.0)))
        print("")
        sleep(1)
        print("The chosen ID has a " + rndm_kll + "% of killing sucess!")
        print("")

    elif rsp_answer1 == "y":
        rndm_age = (str(random.randint(20, 70)))
        rndm_kll = (str(random.uniform(0.0, 100.0)))
        print("")
        sleep(1)
        print("The chosen ID has " + rndm_fnm + " as name.")
        sleep(1)
        print("The chosen ID is " + rndm_age + " years old.")
        print("")
        sleep(1)
        print("The chosen ID has " + rndm_ip + " as an IP.")
        print("")
        sleep(1)
        print("")
        sleep(1)
        print("The chosen ID drank water at " + str(rndm_drnk_wtr_h) + ":" + str(rndm_drnk_wtr_m) + ":" + str(rndm_drnk_wtr_s) + " last time.")
        print("")
        sleep(1)
        print("The chosen ID has a " + rndm_kll + "% of killing sucess!")
        sleep(1)
        print("")


answ_chk1()


def answ_chk2():
    sleep(2)
    print("Do You want to kill the chosen ID?")
    print("")
    sleep(1.5)
    print("If yes, type y. If no, type n.")
    rsp_answer2 = pip.inputStr(prompt="Enter answer: ")
    if rsp_answer2 == "y":
        print("")
        sleep(2)
        print("An ICBM misile will be sent soon to the chosen ID!")
        print("")
        sleep(1)
        print("**Starting Sounds of Nuclear Alarm.**")
        print("")
        sleep(1)
        toot = "Toooooooot!!!"
        print(toot)
        sleep(4)
        print("")
        print(toot)
        sleep(4)
        print("")
        print(toot)
        sleep(4)
        print("")
        print(toot)
        sleep(3)
        print("")
        sleep(2)
        print("Engine of ICBM has started!")
        print("")
        sleep(2)
        print("Thrusts ignited at:")
        sleep(1)

        with open("Percentage01.txt", "r") as fh:
            prcnt_txt = fh.read().replace("\n", " ")
            language = 'en'
            output = gTTS(text=prcnt_txt, lang=language, slow=False)
            output.save("PercentageT2S-01.mp3")
        os.system("start PercentageT2S-01.mp3")

        sleep(6)
        print("")
        sleep(118.05)
        os.system("@echo off")
        os.system("@taskkill /IM Music.UI.exe /F")
        print("Waiting...")
        print("")

        for i, _ in enumerate(list(range(1000001))):
            print(i, end='\r')

        loop = tqdm(total=100000, position=0, leave=False)
        for k in range(100000):
            loop.set_description("Backtracking to last working system trail...".format(k))
            loop.update(1)
        loop.close()

        loop = tqdm(total=100000, position=0, leave=False)
        for k in range(100000):
            loop.set_description("Preparing to fix...".format(k))
            loop.update(1)
        loop.close()

        loop = tqdm(total=100000, position=0, leave=False)
        for k in range(100000):
            loop.set_description("Fixing startup...".format(k))
            loop.update(1)
        loop.close()

        loop = tqdm(total=100000, position=0, leave=False)
        for k in range(100000):
            loop.set_description("Stabilazing startup...".format(k))
            loop.update(1)
        loop.close()

        loop = tqdm(total=100000, position=0, leave=False)
        for k in range(100000):
            loop.set_description("Stabilazing...".format(k))
            loop.update(1)
        loop.close()

        loop = tqdm(total=100000, position=0, leave=False)
        for k in range(100000):
            loop.set_description("Thrusts Ignite Process startup...".format(k))
            loop.update(1)
        loop.close()

        loop = tqdm(total=100000, position=0, leave=False)
        for k in range(100000):
            loop.set_description("Igniting thrusts...".format(k))
            loop.update(1)
        loop.close()

        loop = tqdm(total=100000, position=0, leave=False)
        for k in range(100000):
            loop.set_description("Continuation of launch proceure...".format(k))
            loop.update(1)
        loop.close()

        print("ICBM launched!")
        print("")

    elif rsp_answer2 == "n":
        sleep(3)
        print("")
        print("The chosen ID will live for one more day!")
        print("")


def reprt_pr_mnstr():
    print("")
    print("A message will be compiled before sending it to the Primary Minister of Tolyavgrad Vyboska!")
    print("")
    print("Compiling message...")
    sleep(5)
    print("")
    print("Message compiled!")
    print("")


answ_chk2()

print("Preparing to send report...")
print("")
sleep(4)
loop = tqdm(total=100000, position=0, leave=False)
for k in range(100000):
    loop.set_description("Sending...".format(k))
    loop.update(1)
loop.close()

reprt_pr_mnstr()

sleep(1)
print("Report sent!")
sleep(3)
print("")
