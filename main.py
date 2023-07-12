# Wizard Card Game Scoring Program
# Began May 1, 2023
# Evan Davies

# TO-DO LIST #
# - Finish scorecard
# - Save scores permanently
# - Clear scores file at start of each game
# - Scorecards should display a number if 2 or more people have the same name abbreviation.

# Updated Jul 10, 2023:
# NEW #
# - Added player names
# - Added player scores at the end of each round
# ADJUSTMENTS #
# Turn number calculator is now much simpler.
# WIP #
# - Scorecards
# - Score storage

# Updated Jul 12, 2023:
# FIXES #
# Fixed player scores after each round not displaying player names correctly in some cases.
# NEW #
# - Now using pyautogui. Currently just used to clear the run window after each round.
# - Scorecard now displays player names (mostly) correctly
# - scores.dat now clears before each game



# Imports
import math
import pyautogui

# Function to display all score updates. Currently only displays player name abbreviations.
def showScorecard():
    print("|———————————————————————————|")
    pNameList = f"|   |"
    for num in range(numPlayers):
        pNameList += f"{pNamesAbbr[num]:>3}|"
    pNameList += (6 - numPlayers) * "   |"
    print(pNameList)
    s = open("scores.dat", "r")
    scores = s.readlines()
    for score in scores:
        print(score.strip())




# Calculating number of turns.
def numTurnsCalc(players):
    numturns = 60/players
    return int(numturns)

# START OF PROGRAM
# Setup

# Clearing the scores file to start a new game
open("scores.dat", "w").close()

# Number of players
while True:
    try:
        numPlayers = int(input("Enter number of players (3-6): "))
    except:
        print("Must be an integer.")
    else:
        if 3  > numPlayers or numPlayers > 6:
            print("Number of players must be between 3 and 6.")
        else:
            break

# Setting up lists for player names and abbreviations for the scorecard
playerNames = []
pNamesAbbr = []

# Collecting player names
for player in range(numPlayers):
    while True:
        name = input(f"Enter player {player+1}'s name: ").title()
        if name == "":
            print("Must not be blank. Try again.")
        elif "," in name == True:
            print("Name may not contain commas. Try again.")
        else:
            break
    playerNames.append(name)
    pNamesAbbr.append(name[0:3])

# Calling turn calculator
numTurns = numTurnsCalc(numPlayers)

# Setting up lists for bids and scores for each round
bidsList = []
totalScores = []

# Making a zero in each list for each player
for player in range(numPlayers):
    bidsList.append(0)
    totalScores.append(0)

for turn in range(numTurns):
    # Displaying turn number
    print(f"Round {turn + 1}")
    print()
    for player in range(numPlayers):
        while True:
            # Collecting bids
            try:
                bid = int(input(f"Enter bid for {playerNames[player]}: "))
            except:
                print("Must be an integer.")
            else:
                if bid < 0:
                    print("Must bid 0 or higher.")
                elif bid > (turn + 1):
                    print("Cannot bid higher than the cards in your hand.")
                else:
                    bidsList[player] = bid
                    break

    print()
    print()
    print()

    for player in range(numPlayers):
        while True:
            # Collecting wins (could use work)
            try:
                wins = int(input(f"Enter number of wins for {playerNames[player]}: "))
            except:
                print("Must be an integer.")
            else:
                if wins < 0:
                    print("Cannot win less than 0.")
                elif wins > (turn+1):
                    print("Cannot win that many this round.")
                else:
                    if wins == bidsList[player]:
                        totalScores[player] += 20 + (wins*10)
                        break
                    elif wins > bidsList[player]:
                        totalScores[player] -= (wins - bidsList[player]) * 10
                        break
                    elif wins < bidsList[player]:
                        totalScores[player] -= (bidsList[player] - wins) * 10
                        break
    print()
    print()
    print()

    # Listing
    for i in range(len(totalScores)):
        print(f"{playerNames[i]}: {totalScores[i]}")
    print(f"")
    f = open("scores.dat", "a")
    totalScoresStr = ", ".join([str(item) for item in totalScores])
    totalScoresWrite = ""
    if turn != 0:
        totalScoresWrite += "\n"
    totalScoresWrite += totalScoresStr
    f.write(totalScoresWrite)
    f.close()
    print()
    print()
    print()
    if turn != 0:
        while True:
            showOld = input("Would you like to view score history (Y/N)? ").upper()
            if showOld != "Y" and showOld != "N":
                print("Invalid. Enter Y or N.")
            elif showOld == "Y":
                showScorecard()
                break
            else:
                break
    go = input("Press enter to continue to next round: ")
    pyautogui.click(x=828, y=388)
    pyautogui.hotkey('shift', 'command', 'p')