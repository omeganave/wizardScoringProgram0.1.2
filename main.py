# Wizard Card Game Scoring Program
# Began May 1, 2023
# Evan Davies

# TO-DO LIST #
# - Scorecards should display a number if 2 or more people have the same name abbreviation.
# - Permanent score storage
# - Menu (FINISH IT)
# - Quit options between turns
# - Score/winner display at the end
# - Win limits
# - (Maybe) Bid max warning
# - Simplify end-of-turn score displays with the use of tuples

# Updated Jul 10, 2023:
# NEW #
# - Added player names
# - Added player scores at the end of each round
# ADJUSTMENTS #
# Turn number calculator is now much simpler.

# Updated Jul 12, 2023:
# FIXES #
# Fixed player scores after each round not displaying player names correctly in some cases.
# NEW #
# - Now using pyautogui. Currently just used to clear the run window after each round.
# - Scorecard complete!
# - scores.dat now clears before each game
# - Created a GitHub repository for the project

# Updated Jul 13, 2023:
# NEW #
# - Added a main menu
# ADJUSTMENTS #
# - Changed player score displays at the end of each round to display current standings


# Imports
import math
import pyautogui  # Used for clearing the run window


# Function to play the game
def playGame():
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
        print(f"Round {turn + 1} / {numTurns}")
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

        # Listing current scores
        scoresTuple = list(zip(playerNames, totalScores))
        scoresTuple.sort(key=lambda x: x[1], reverse=True)
        for position, (playerName, score) in enumerate(scoresTuple, 1):
            print(f"{position}. {playerName}: {score} points")
        f = open("scores.dat", "a")
        totalScoresStr = ",".join([str(item) for item in totalScores])
        totalScoresWrite = ""
        if turn != 0:
            totalScoresWrite += "\n"
        totalScoresWrite += totalScoresStr
        f.write(totalScoresWrite)
        f.close()
        print()
        print()
        print()
        # If at least two rounds have been played, a scorecard can be viewed
        if turn != 0:
            while True:
                showOld = input("Would you like to view score history (Y/N)? ").upper()
                if showOld != "Y" and showOld != "N":
                    print("Invalid. Enter Y or N.")
                elif showOld == "Y":
                    showScorecard(numPlayers, pNamesAbbr)
                    break
                else:
                    break

        go = input("Press enter to continue to next round: ")
        pyautogui.click(x=828, y=388)
        pyautogui.hotkey('shift', 'command', 'p')

    return


# Function to display all score updates. Currently only displays player name abbreviations.
def showScorecard(numPlayers, pNamesAbbr):
    print("|———————————————————————————|")
    pNameList = f"|   |"
    for num in range(numPlayers):
        pNameList += f"{pNamesAbbr[num]:>3}|"
    pNameList += (6 - numPlayers) * "   |"
    print(pNameList)
    print("|———————————————————————————|")
    s = open("scores.dat", "r")
    scores = s.readlines()
    turnNum = 1
    for score in scores:
        splitScores = score.split(",")
        scoreRow = "|"
        if turnNum <= 9:
            scoreRow += " "
        scoreRow += f"T{turnNum}|"
        for subscore in splitScores:
            stripped = subscore.strip()
            scoreRow += f"{stripped:>3s}|"
        scoreRow += (6 - numPlayers) * "   |"
        print(scoreRow)
        turnNum += 1
    print("|———————————————————————————|")


# Calculating number of turns.
def numTurnsCalc(players):
    numturns = 60/players
    return int(numturns)


# START OF PROGRAM
# Clearing the window
pyautogui.click(x=828, y=388)
pyautogui.hotkey('shift', 'command', 'p')

# Welcome message
print("Welcome to my Wizard scoring program!")
while True:
    # Selections
    print("Select one of the following:")
    print("1. Score a game")
    print("2. View past games")
    print("3. Credits")
    print("4. Quit")
    selection = input(">")
    if int(selection) != 1 and int(selection) != 2 and int(selection) != 3 and int(selection) != 4:
        pyautogui.click(x=828, y=388)
        pyautogui.hotkey('shift', 'command', 'p')
        print("Invalid selection")
        print()
    elif int(selection) == 1:
        pyautogui.click(x=828, y=388)
        pyautogui.hotkey('shift', 'command', 'p')
        playGame()
    elif int(selection) == 2:
        pyautogui.click(x=828, y=388)
        pyautogui.hotkey('shift', 'command', 'p')
        print(f"Nothing here yet! ({selection})")
    elif int(selection) == 3:
        pyautogui.click(x=828, y=388)
        pyautogui.hotkey('shift', 'command', 'p')
        print(f"Nothing here yet! ({selection})")
    else:
        pyautogui.click(x=828, y=388)
        pyautogui.hotkey('shift', 'command', 'p')
        while True:
            confirm = input("Are you sure you'd like to quit? (Y/N):").upper()
            if confirm != "Y" and confirm != "N":
                print("Invalid selection")
            elif confirm == "N":
                break
            else:
                print("Thanks for using my program. Goodbye!")
                exit()
        pyautogui.click(x=828, y=388)
        pyautogui.hotkey('shift', 'command', 'p')
