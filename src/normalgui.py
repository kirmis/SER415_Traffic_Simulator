# SER415 Traffic Simulator - Team 8
# Manolito Ramirez, Jessica Gilbert, Mike Wagner,
# Carlos Franco, Arthur Rivera, and Ryan Kirmis
# Version 1.1.1

import tkinter as tk
import tkinter.ttk
import math
import time

root = tkinter.Tk()

#-------------------------------------------------------------------------------
# GLOBALS:
flowRateScalar = 1;     # used to change flow rate for specific scenarios
maxFlowRate = 1;        # used to scale max flow rate (default flow rate = 2)
sampleDelay = 500;      # delay between samples
simActive = False;      # boolean for checking if simulation is active

#-------------------------------------------------------------------------------
# GUI SETUP:

# ---Canvas---
top = tk.Canvas(root, width=850, height=625, bg="#C0C5C6")
top.pack();
top.create_text((20, 10), text="Traffic Simulator", font="MSGothic 20 bold", fill="#065535", anchor="nw")
top.create_text((570, 98), text="Cycle Timing", font="MSGothic 15 bold", fill="#065535", anchor="nw")
top.create_text((660, 347), text="Scenarios", font="MSGothic 15 bold", fill="#065535", anchor="nw")
top.create_text((660, 280), text="Max Outflow Rate", font="MSGothic 10 bold", fill="#065535", anchor="nw")
top.create_text((703, 303), text="cars/sec", font="MSGothic 8", fill="#065535", anchor="nw")
top.create_text((340, 54), text="Cycle", font="MSGothic 8 bold", fill="#065535", anchor="nw")
top.create_text((434, 54), text="Time (s)", font="MSGothic 8 bold", fill="#065535", anchor="nw")

# 'Cars In/Cars' Out text labels from West
top.create_text((43, 354), text="Cars In", font="MSGothic 8 bold", fill="#065535", anchor="nw")
top.create_text((43, 296), text="Cars Out", font="MSGothic 8 bold", fill="#065535", anchor="nw")
top.create_text((43, 396), text="Inflow Rate", font="MSGothic 8 bold", fill="#065535", anchor="nw")

# 'Cars In/Cars Out' text labels from North
top.create_text((236, 141), text="Cars In", font="MSGothic 8 bold", fill="#065535", anchor="nw")
top.create_text((309, 141), text="Cars Out", font="MSGothic 8 bold", fill="#065535", anchor="nw")
top.create_text((236, 100), text="Inflow Rate", font="MSGothic 8 bold", fill="#065535", anchor="nw")

# 'Cars In/Cars' Out text labels from East
top.create_text((497, 279), text="Cars In", font="MSGothic 8 bold", fill="#065535", anchor="nw")
top.create_text((497, 368), text="Cars Out", font="MSGothic 8 bold", fill="#065535", anchor="nw")
top.create_text((497, 321), text="Inflow Rate", font="MSGothic 8 bold", fill="#065535", anchor="nw")

# 'Cars In/Cars Out' text labels from South
top.create_text((309, 532), text="Cars In", font="MSGothic 8 bold", fill="#065535", anchor="nw")
top.create_text((237, 532), text="Cars Out", font="MSGothic 8 bold", fill="#065535", anchor="nw")
top.create_text((309, 573), text="Inflow Rate", font="MSGothic 8 bold", fill="#065535", anchor="nw")

root.geometry("850x625+503+155")
root.minsize(120, 1)
root.maxsize(1924, 1061)
root.resizable(0, 0)
root.title("Traffic Simulator GUI")
root.configure(background="#D9D9D9")

main_bg = tk.PhotoImage(file="../resources/intersection.png")


# ---Frames---
# Timing value input frame
fTiming = tk.Frame(top, bg="#707070", highlightbackground="#065535", highlightthickness=3)
fTiming.place(relx=0.67, rely=0.2, relheight=0.215, relwidth=0.277)


# ---Labels---
# Intersection image
lIntersection = tk.Label(top, image=main_bg)
lIntersection.place(relx=0.13, rely=0.3, height=341, width=371)

# Timing value input labels
lTimeNS = tk.Label(fTiming, text="N-S", bg="#707070", anchor="nw")
lTimeNSGrnArr = tk.Label(fTiming, text="N-S Green Arrow", bg="#707070", anchor="nw")
lTimeWE = tk.Label(fTiming, text="W-E", bg="#707070", anchor="nw")
lTimeWEGrnArr = tk.Label(fTiming, text="W-E Green Arrow", bg="#707070", anchor="nw")

# Seconds labels
lSecondsNS = tk.Label(fTiming, text="s", bg="#707070", anchor="nw")
lSecondsNSGrnArr = tk.Label(fTiming, text="s", bg="#707070", anchor="nw")
lSecondsWE = tk.Label(fTiming, text="s", bg="#707070", anchor="nw")
lSecondsWEGrnArr = tk.Label(fTiming, text="s", bg="#707070", anchor="nw")

lTimeNS.place(relx=0.05, rely=0.05, height=20, width=100)
lTimeNSGrnArr.place(relx=0.05, rely=0.275, height=20, width=100)
lTimeWE.place(relx=0.05, rely=0.5, height=20, width=100)
lTimeWEGrnArr.place(relx=0.05, rely=0.725, height=20, width=100)

lSecondsNS.place(relx=0.9, rely=0.05, height=20, width=15)
lSecondsNSGrnArr.place(relx=0.9, rely=0.275, height=20, width=15)
lSecondsWE.place(relx=0.9, rely=0.5, height=20, width=15)
lSecondsWEGrnArr.place(relx=0.9, rely=0.725, height=20, width=15)

# Current Time Indicator
lCurrTime = tk.Label(top, bg = "#C8E2BB", anchor="nw")
lCurrTime.place(relx=0.51, rely=0.11, height=20, width=30)
lCurrTime["text"] = 0

# Current Cycle Indicator
lCurrCycle = tk.Label(top, bg = "#C8E2BB", anchor="nw")
lCurrCycle.place(relx=0.4, rely=0.11, height=25, width=70)
lCurrCycle["text"] = "-"

# ---Text fields---
# 'Number of cars' text fields
tCarsInW = tk.Text(top)
tCarsInN = tk.Text(top)
tCarsInE = tk.Text(top)
tCarsInS = tk.Text(top)
tCarsOutW = tk.Text(top, bg = "#C8E2BB")
tCarsOutN = tk.Text(top, bg = "#C8E2BB")
tCarsOutE = tk.Text(top, bg = "#C8E2BB")
tCarsOutS = tk.Text(top, bg = "#C8E2BB")

# 'Cycle times' text fields
tTimeNS = tk.Text(fTiming)
tTimeNSGrnArr = tk.Text(fTiming)
tTimeWE = tk.Text(fTiming)
tTimeWEGrnArr = tk.Text(fTiming)

tTimeNS.insert('1.0', '15')
tTimeNSGrnArr.insert('1.0', '15')
tTimeWE.insert('1.0', '15')
tTimeWEGrnArr.insert('1.0', '15')

tCarsInW.place(relx=0.05, rely=0.59, relheight=0.035, relwidth=0.06)
tCarsInN.place(relx=0.278, rely=0.25, relheight=0.035, relwidth=0.06)
tCarsInE.place(relx=0.585, rely=0.47, relheight=0.035, relwidth=0.06)
tCarsInS.place(relx=0.363, rely=0.875, relheight=0.035, relwidth=0.06)
tCarsOutW.place(relx=0.05, rely=0.498, relheight=0.035, relwidth=0.06)
tCarsOutN.place(relx=0.363, rely=0.25, relheight=0.035, relwidth=0.06)
tCarsOutE.place(relx=0.585, rely=0.612, relheight=0.035, relwidth=0.06)
tCarsOutS.place(relx=0.278, rely=0.875, relheight=0.035, relwidth=0.06)

tTimeNS.place(relx=0.65, rely=0.05, height=20, width=45)
tTimeNSGrnArr.place(relx=0.65, rely=0.275, height=20, width=45)
tTimeWE.place(relx=0.65, rely=0.5, height=20, width=45)
tTimeWEGrnArr.place(relx=0.65, rely=0.725, height=20, width=45)

tCarsInW.insert('1.0', '15')
tCarsInN.insert('1.0', '15')
tCarsInE.insert('1.0', '15')
tCarsInS.insert('1.0', '15')
tCarsOutW.insert('1.0', '0')
tCarsOutN.insert('1.0', '0')
tCarsOutE.insert('1.0', '0')
tCarsOutS.insert('1.0', '0')

# 'Inflow' rates
tInflowW = tk.Text(top)
tInflowN = tk.Text(top)
tInflowE = tk.Text(top)
tInflowS = tk.Text(top)

tInflowW.place(relx=0.05, rely=0.657, relheight=0.035, relwidth=0.06)
tInflowN.place(relx=0.278, rely=0.185, relheight=0.035, relwidth=0.06)
tInflowE.place(relx=0.585, rely=0.5375, relheight=0.035, relwidth=0.06)
tInflowS.place(relx=0.363, rely=0.940, relheight=0.035, relwidth=0.06)

tInflowW.insert('1.0', '0.2')
tInflowN.insert('1.0', '0.2')
tInflowE.insert('1.0', '0.2')
tInflowS.insert('1.0', '0.2')

# Lane percentages text field
tRightW = tk.Text(lIntersection, bg="#90EEBF")
tStraightW = tk.Text(lIntersection, bg="#90EEBF")
tLeftW = tk.Text(lIntersection, bg="#90EEBF")

tRightN = tk.Text(lIntersection, bg="#90EEBF")
tStraightN = tk.Text(lIntersection, bg="#90EEBF")
tLeftN = tk.Text(lIntersection, bg="#90EEBF")

tRightE = tk.Text(lIntersection, bg="#90EEBF")
tStraightE = tk.Text(lIntersection, bg="#90EEBF")
tLeftE = tk.Text(lIntersection, bg="#90EEBF")

tRightS = tk.Text(lIntersection, bg="#90EEBF")
tStraightS = tk.Text(lIntersection, bg="#90EEBF")
tLeftS = tk.Text(lIntersection, bg="#90EEBF")

tRightW.place(relx=0.06, rely=0.663, height=20, width=20)
tStraightW.place(relx=0.06, rely=0.589, height=20, width=20)
tLeftW.place(relx=0.06, rely=0.513, height=20, width=20)

tRightN.place(relx=0.305, rely=0.04, height=20, width=20)
tStraightN.place(relx=0.374, rely=0.04, height=20, width=20)
tLeftN.place(relx=0.442, rely=0.04, height=20, width=20)

tRightE.place(relx=0.89, rely=0.29, height=20, width=20)
tStraightE.place(relx=0.89, rely=0.366, height=20, width=20)
tLeftE.place(relx=0.89, rely=0.438, height=20, width=20)

tRightS.place(relx=0.645, rely=0.915, height=20, width=20)
tStraightS.place(relx=0.577, rely=0.915, height=20, width=20)
tLeftS.place(relx=0.51, rely=0.915, height=20, width=20)

tRightW.insert('1.0', '.2')
tStraightW.insert('1.0', '.7')
tLeftW.insert('1.0', '.1')

tRightN.insert('1.0', '.2')
tStraightN.insert('1.0', '.7')
tLeftN.insert('1.0', '.1')

tRightE.insert('1.0', '.2')
tStraightE.insert('1.0', '.7')
tLeftE.insert('1.0', '.1')

tRightS.insert('1.0', '.2')
tStraightS.insert('1.0', '.7')
tLeftS.insert('1.0', '.1')

# 'Max flow rate' input text fields
tMaxFlowRate = tk.Text(top)
tMaxFlowRate.place(relx=0.775, rely=0.48, height=25, width=40)
tMaxFlowRate.insert('1.0', '2.0')

# Scenarios
currScenario = tk.StringVar(top)
currScenario.set("None") # set default scenario to 'None'

# Drop down menu
scenarios = tk.OptionMenu(top, currScenario, "None", "Construction", "Weather", "Accident")
scenarios.place(relx=0.775, rely=0.6, height=25, width=125)

# ---Buttons---
# 'Run Simulation' button
bRunSim = tk.Button(top, text="Run Simulation", bg = "#90EE90")
bRunSim.place(relx=0.054, rely=0.11, height=34, width=97)

bStopSim = tk.Button(top, text="Stop", bg = "#FFCCCB", state="disabled")
bStopSim.place(relx=0.18, rely=0.11, height=34, width=40)

# ---Boolean Indicators---
#rbSimRunning = tk.Radiobutton(top, text ="")
#rbSimRunning.place(relx=0.2, rely=0.11, height=25, width=25)
#rbSimRunning.deselect()

#-------------------------------------------------------------------------------
# FUNCTIONS

cycleLengths = [0, 0, 0, 0] # cycle lengths (in s)

startTime = 0
currTime = 0
currSecond = 0
currCycle = 0

carsInW = 0
carsInN = 0
carsInE = 0
carsInS = 0
carsOutW = 0
carsOutN = 0
carsOutE = 0
carsOutS = 0

"""
description- Starts simulation when user clicks 'Run Simulation' button
parameters-
return-
"""
def startSim(event=None):
    global currTime, startTime, currSecond, currCycle, simActive

    cycleLengths[0] = int(tTimeNS.get("1.0", "end-1c"));
    cycleLengths[1] = int(tTimeNSGrnArr.get("1.0", "end-1c"));
    cycleLengths[2] = int(tTimeWE.get("1.0", "end-1c"));
    cycleLengths[3] = int(tTimeWEGrnArr.get("1.0", "end-1c"));

    simActive = True
    bRunSim["state"] = "disabled"
    bStopSim["state"] = "normal"

    startTime = time.time()
    currTime = time.time() - startTime
    currSecond = 0
    if (currCycle == 0):
        root.after(0, cycleNS)
    elif (currCycle == 1):
        root.after(0, cycleNSGrnArr)
    elif (currCycle == 2):
        root.after(0, cycleWE)
    elif (currCycle == 3):
        root.after(0, cycleWEGrnArr)
    else:
        simActive = False
        bRunSim["state"] = "normal"
        bStopSim["state"] = "disabled"
        lCurrCycle["text"] = "-"
        lCurrTime["text"] = 0
        currCycle = 0
"""
description-
parameters-
return-
"""
def cycleNS():
    global currTime, startTime, currSecond, currCycle, cycleLengths, simActive
    global carsInN, carsInS, carsOutS, carsOutW, carsOutN, carsOutE

    if (simActive):
        if (currSecond == 0):
            carsInN = float(tCarsInN.get("1.0", "end-1c"))
            carsInS = float(tCarsInS.get("1.0", "end-1c"))

            carsOutS = float(tCarsOutS.get("1.0", "end-1c"))
            carsOutW = float(tCarsOutW.get("1.0", "end-1c"))
            carsOutN = float(tCarsOutN.get("1.0", "end-1c"))
            carsOutE = float(tCarsOutE.get("1.0", "end-1c"))

            lCurrCycle["text"] = "N/S"

        if (currTime < cycleLengths[currCycle]):
            if (currTime > currSecond):
                inflowCars()

                lCurrTime["text"] = currSecond + 1

                currRate = calculateCurrRate(currTime)

                tCarsInN.delete("1.0", tk.END)
                if (carsInN <= 0):
                    tCarsInN.insert("1.0", 0)
                else:
                    tCarsOutS.delete("1.0", tk.END)
                    tCarsOutW.delete("1.0", tk.END)

                    rightLaneCars = currRate * float(tRightN.get("1.0", "end-1c"))
                    straightLaneCars = currRate * float(tStraightN.get("1.0", "end-1c"))
                    carsInN -= (rightLaneCars + straightLaneCars)
                    carsOutS += straightLaneCars
                    carsOutW += rightLaneCars
                    tCarsInN.insert("1.0", math.floor(carsInN))
                    tCarsOutS.insert("1.0", math.floor(carsOutS))
                    tCarsOutW.insert("1.0", math.floor(carsOutW))

                tCarsInS.delete("1.0", tk.END)
                if (carsInS <= 0):
                    tCarsInS.insert("1.0", 0)
                else:
                    tCarsOutN.delete("1.0", tk.END)
                    tCarsOutE.delete("1.0", tk.END)

                    rightLaneCars = currRate * float(tRightS.get("1.0", "end-1c"))
                    straightLaneCars = currRate * float(tStraightS.get("1.0", "end-1c"))
                    carsInS -= (rightLaneCars + straightLaneCars)
                    carsOutN += straightLaneCars
                    carsOutE += rightLaneCars
                    tCarsInS.insert("1.0", math.floor(carsInS))
                    tCarsOutN.insert("1.0", math.floor(carsOutN))
                    tCarsOutE.insert("1.0", math.floor(carsOutE))

                currSecond += 1
            currTime = time.time() - startTime
            root.after(sampleDelay, cycleNS)
        else:
            currCycle += 1
            root.after(0, startSim)
"""
description-
parameters-
return-
"""
def cycleNSGrnArr():
    global currTime, startTime, currSecond, currCycle, cycleLengths, simActive
    global carsInN, carsInS, carsOutE, carsOutW

    if (simActive):
        if (currSecond == 0):
            carsInN = float(tCarsInN.get("1.0", "end-1c"))
            carsInS = float(tCarsInS.get("1.0", "end-1c"))

            carsOutE = float(tCarsOutE.get("1.0", "end-1c"))
            carsOutW = float(tCarsOutW.get("1.0", "end-1c"))

            lCurrCycle["text"] = "N/S Arrow"

        if (currTime < cycleLengths[currCycle]):
            if (currTime > currSecond):
                inflowCars()

                lCurrTime["text"] = currSecond + 1

                currRate = calculateCurrRate(currTime)

                tCarsInN.delete("1.0", tk.END)
                if (carsInN <= 0):
                    tCarsInN.insert("1.0", 0)
                else:
                    tCarsOutE.delete("1.0", tk.END)

                    leftLaneCars = currRate * float(tLeftN.get("1.0", "end-1c"))
                    carsInN -= leftLaneCars
                    carsOutE += leftLaneCars
                    tCarsInN.insert("1.0", math.floor(carsInN))
                    tCarsOutE.insert("1.0", math.floor(carsOutE))

                tCarsInS.delete("1.0", tk.END)
                if (carsInS <= 0):
                    tCarsInS.insert("1.0", 0)
                else:
                    tCarsOutW.delete("1.0", tk.END)

                    leftLaneCars = currRate * float(tLeftS.get("1.0", "end-1c"))
                    carsInS -= leftLaneCars
                    carsOutW += leftLaneCars
                    tCarsInS.insert("1.0", math.floor(carsInS))
                    tCarsOutW.insert("1.0", math.floor(carsOutW))

                currSecond += 1
            currTime = time.time() - startTime
            root.after(sampleDelay, cycleNSGrnArr)
        else:
            currCycle += 1
            root.after(0, startSim)
"""
description-
parameters-
return-
"""
def cycleWE():
    global currTime, startTime, currSecond, currCycle, cycleLengths, simActive
    global carsInW, carsInE, carsOutE, carsOutS, carsOutW, carsOutN

    if (simActive):
        if (currSecond == 0):
            carsInW = float(tCarsInW.get("1.0", "end-1c"))
            carsInE = float(tCarsInE.get("1.0", "end-1c"))

            carsOutE = float(tCarsOutE.get("1.0", "end-1c"))
            carsOutS = float(tCarsOutS.get("1.0", "end-1c"))
            carsOutW = float(tCarsOutW.get("1.0", "end-1c"))
            carsOutN = float(tCarsOutN.get("1.0", "end-1c"))

            lCurrCycle["text"] = "W/E"

        if (currTime < cycleLengths[currCycle]):
            if (currTime > currSecond):
                inflowCars()

                lCurrTime["text"] = currSecond + 1

                currRate = calculateCurrRate(currTime)

                tCarsInW.delete("1.0", tk.END)
                if (carsInW <= 0):
                    tCarsInW.insert("1.0", 0)
                else:
                    tCarsOutE.delete("1.0", tk.END)
                    tCarsOutS.delete("1.0", tk.END)

                    rightLaneCars = currRate * float(tRightW.get("1.0", "end-1c"))
                    straightLaneCars = currRate * float(tStraightW.get("1.0", "end-1c"))
                    carsInW -= (rightLaneCars + straightLaneCars)
                    carsOutE += straightLaneCars
                    carsOutS += rightLaneCars
                    tCarsInW.insert("1.0", math.floor(carsInW))
                    tCarsOutE.insert("1.0", math.floor(carsOutE))
                    tCarsOutS.insert("1.0", math.floor(carsOutS))

                tCarsInE.delete("1.0", tk.END)
                if (carsInE <= 0):
                    tCarsInE.insert("1.0", 0)
                else:
                    tCarsOutW.delete("1.0", tk.END)
                    tCarsOutN.delete("1.0", tk.END)

                    rightLaneCars = currRate * float(tRightE.get("1.0", "end-1c"))
                    straightLaneCars = currRate * float(tStraightE.get("1.0", "end-1c"))
                    carsInE -= (rightLaneCars + straightLaneCars)
                    carsOutW += straightLaneCars
                    carsOutN += rightLaneCars
                    tCarsInE.insert("1.0", math.floor(carsInE))
                    tCarsOutW.insert("1.0", math.floor(carsOutW))
                    tCarsOutN.insert("1.0", math.floor(carsOutN))

                currSecond += 1
            currTime = time.time() - startTime
            root.after(sampleDelay, cycleWE)
        else:
            currCycle += 1
            root.after(0, startSim)
"""
description-
parameters-
return-
"""
def cycleWEGrnArr():
    global currTime, startTime, currSecond, currCycle, cycleLengths, simActive
    global carsInW, carsInE, carsOutN, carsOutS

    if (simActive):
        if (currSecond == 0):
            carsInW = float(tCarsInW.get("1.0", "end-1c"))
            carsInE = float(tCarsInE.get("1.0", "end-1c"))

            carsOutN= float(tCarsOutN.get("1.0", "end-1c"))
            carsOutS = float(tCarsOutS.get("1.0", "end-1c"))

            lCurrCycle["text"] = "W/E Arrow"

        if (currTime < cycleLengths[currCycle]):
            if (currTime > currSecond):
                inflowCars()

                lCurrTime["text"] = currSecond + 1

                currRate = calculateCurrRate(currTime)

                tCarsInW.delete("1.0", tk.END)
                if (carsInW <= 0):
                    tCarsInW.insert("1.0", 0)
                else:
                    tCarsOutN.delete("1.0", tk.END)

                    leftLaneCars = currRate * float(tLeftW.get("1.0", "end-1c"))
                    carsInW -= leftLaneCars
                    carsOutN += leftLaneCars
                    tCarsInW.insert("1.0", math.floor(carsInW))
                    tCarsOutN.insert("1.0", math.floor(carsOutN))

                tCarsInE.delete("1.0", tk.END)
                if (carsInE <= 0):
                    tCarsInE.insert("1.0", 0)
                else:
                    tCarsOutS.delete("1.0", tk.END)

                    leftLaneCars = currRate * float(tLeftE.get("1.0", "end-1c"))
                    carsInE -= leftLaneCars
                    carsOutS += leftLaneCars
                    tCarsInE.insert("1.0", math.floor(carsInE))
                    tCarsOutS.insert("1.0", math.floor(carsOutS))

                currSecond += 1
            currTime = time.time() - startTime
            root.after(sampleDelay, cycleWEGrnArr)
        else:
            currCycle += 1
            root.after(0, startSim)
"""
description-
parameters-
return-
"""
def inflowCars():
    global carsInW, carsInN, carsInE, carsInS

    carsInW += float(tInflowW.get("1.0", "end-1c"))
    carsInN += float(tInflowN.get("1.0", "end-1c"))
    carsInE += float(tInflowE.get("1.0", "end-1c"))
    carsInS += float(tInflowS.get("1.0", "end-1c"))

    tCarsInW.delete("1.0", tk.END)
    tCarsInN.delete("1.0", tk.END)
    tCarsInE.delete("1.0", tk.END)
    tCarsInS.delete("1.0", tk.END)

    tCarsInW.insert("1.0", math.floor(carsInW))
    tCarsInN.insert("1.0", math.floor(carsInN))
    tCarsInE.insert("1.0", math.floor(carsInE))
    tCarsInS.insert("1.0", math.floor(carsInS))


"""
description- Stops the simulation if running
parameters-
return-
"""
def stopSim(event=None):
    global simActive
    simActive = False
    bRunSim["state"] = "normal"
    bStopSim["state"] = "disabled"

"""
description- Returns the traffic flow rate at a specific time since GREEN light activated
parameters-
return-
"""
def calculateCurrRate(t):
    global maxFlowRate
    maxFlowRate = float(tMaxFlowRate.get("1.0", "end-1c")) / 2
    return (maxFlowRate * (math.tanh(t-3) + 1))

"""
description- Updates flow rate scalar based on scenario selection
parameters-
return-
"""
def scenarioChange(*args):
    # change based on selected scenario
    if (currScenario.get() == "None"):
        flowRateScalar = 1 #UPDATE
    elif (currScenario.get() == "Construction"):
        flowRateScalar = 1 #UPDATE
    elif (currScenario.get() == "Weather"):
        flowRateScalar = 1 #UPDATE
    elif (currScenario.get() == "Accident"):
        flowRateScalar = 1 #UPDATE

# CALLBACK BINDINGS
bRunSim.bind("<Button-1>", startSim)
bStopSim.bind("<Button-1>", stopSim)

currScenario.trace('w', scenarioChange)

#-------------------------------------------------------------------------------
# HELPER FUNCTIONS

root.mainloop()
