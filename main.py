import tkinter as tk
import os
import time
import subprocess
import sys

if os.geteuid() != 0:
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)  # final version

# do things that require root

CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''


def notify(title, text):
    subprocess.call(['osascript', '-e', CMD, title, text])


# things to add: make ui better, convert timer into minutes and hours, trigger notification when timer is over

def block():
    try:
        minute = int(minuteEntry.get())
    except ValueError:
        minute = 0
    try:
        hour = int(hourEntry.get())
    except ValueError:
        hour = 0
    blocklist = []
    blocklistTerms = 0
    filelocation = __file__ + "/../blocklist.txt"
    #filelocation = os.getcwd() + "/blocklist.txt"

    f = open(filelocation, "r")
    blocklist = f.readlines()
    blocklistTerms = len(blocklist)
    print(blocklist)
    f.close()

    f = open("/etc/hosts", "w")
    for i in range(blocklistTerms):
        f.write("127.0.0.1        " + blocklist[i])
    f.write("\n")
    for i in range(blocklistTerms):
        f.write("127.0.0.1        www." + blocklist[i])

    f.close()
    os.system("sudo killall -HUP mDNSResponder")

    oldTime = int(time.time())

    newTime = hour*3600 + minute*60 + int(time.time())
    total = hour*3600 + minute*60

    timer(oldTime, newTime, minute, hour, total)


def blocklist():
    filelocation = __file__ + "/../blocklist.txt"
    #filelocation = os.getcwd() + "/blocklist.txt"
    subprocess.call(['open', '-a', 'TextEdit', filelocation])


def timer(oldTime, newTime, minute, hour, total):
    global buttonClicked
    buttonClicked = False
    timerWindow = tk.Tk()
    timerWindow.geometry("200x50")
    timerWindow['bg'] = '#F29F77'
    timerWindow.title("Timer")
    second = 1
    timer = tk.Label(text="", master=timerWindow)
    cheat = tk.Button(text="Stop the block",
                      command=revert, master=timerWindow)
    cheat.pack()

    for i in range(total):
        timeLeft = total-i
        stringprinted = (str(timeLeft), "seconds remaining!")
        timer.config(text=stringprinted, font=20)
        time.sleep(1)
        timer['bg'] = '#F29F77'
        timer.pack()
        timerWindow.update_idletasks()
        timerWindow.update()
        if buttonClicked == True:
            # timerWindow.destroy()
            break
        timerWindow.protocol("WM_DELETE_WINDOW", revert)
        if i == total:
            break
    revert()
    notify("WebsiteBlocker", "Timer's up!")
    timerWindow.destroy()
    timerWindow.mainloop()


def revert():
    f = open("/etc/hosts", "w")
    f.write("")
    f.close()

    os.system("sudo killall -HUP mDNSResponder")
    print("blocking complete :)")
    global buttonClicked
    buttonClicked = not buttonClicked


mainWindow = tk.Tk()
mainWindow.title("ProcrastinatorEliminator")
mainWindow.geometry("300x300")
mainWindow['bg'] = '#F29F77'

greeting = tk.Label(text="Greetings, user. Ready to work?", master=mainWindow)
greeting['bg'] = '#F29F77'


minuteLabel = tk.Label(text="\nMinute:", master=mainWindow)
minuteLabel['bg'] = '#F29F77'
minuteEntry = tk.Entry(width=15, master=mainWindow)


hourLabel = tk.Label(text="Hour:", master=mainWindow)
hourLabel['bg'] = '#F29F77'
hourEntry = tk.Entry(width=15, master=mainWindow)


blockButton = tk.Button(text="\nBlock!\n", command=block, master=mainWindow)
blockButton['bg'] = '#F29F77'
blocklistButton = tk.Button(text="Open blocklist",
                            command=blocklist, master=mainWindow)


greeting.pack()
hourLabel.pack()
hourEntry.pack()
minuteLabel.pack()
minuteEntry.pack()
blockButton.pack()
blocklistButton.pack()


mainWindow.mainloop()
