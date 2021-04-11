# Deal or No Deal #
# Eric Anderson #
# April 11th, 2021 #

import time
import random
import statistics

###################################################################
# Functions

# User input error handling function (differentiated by input prompt)
def input_error_handle(txt_str,err_num):
    entry = 0
    entry = input(txt_str)
    if err_num == 2:
        txt_str = "Pick a case number between 1 and 26: "
    if err_num == 1 or err_num == 2:
        while True:
            try:
                entry = int(entry)
                if entry >= 1 and entry <= 26 and entry not in cases_chosen:
                    break
                else:
                    if entry in cases_chosen:
                        entry = input("That case has already been selected. Pick a case: ")
                    else:
                        entry = input(txt_str)
            except ValueError:
                entry = input(txt_str)
        cases_chosen.append(entry)
    elif err_num == 3:
        entry = str(entry)
        while entry.lower() != "deal" and entry.lower() != "no deal":
            entry = input("I know the pressure is on. But please type 'Deal' or 'No Deal': ")
    elif err_num == 4 or err_num == 5:
        entry = str(entry)
        while entry.lower() != "no" and entry.lower() != "yes":
            entry = input("I know the pressure is on. But please type 'Yes' or 'No': ")
    elif err_num == 0:
        entry = str(entry)
        while len(entry) < 1 or len(entry) > 26:
            entry = input("I'm cordial, but don't mess with me. Please type a reasonably lengthy name: ")
    elif err_num == 6:
        entry = str(entry)
        while entry.lower() != "yes":
            entry = input("Don't be nervous. Type 'Yes' or exit the game (but why waste the opportunity of a lifetime?): ")
    return entry


# Display cases function
def display_cases(cd,anim):
    print("---------------------------------------------")
    print("    -------     Cases To Open     -------    ")
    print("---------------------------------------------")
    time.sleep(0.25)
    for i in range(20,27):
        print("  " + str(cd[i-1]) + "  ", end='')
        time.sleep(0.06-anim)
    print(" \n")
    for i in range(14,20):
        if i == 14:
            print("     " + str(cd[i-1]) + "  ", end='')
        else:
            print("  " + str(cd[i-1]) + "  ", end='')
        time.sleep(0.06-anim)
    print(" \n")
    for i in range(7,14):
        if i < 10:
            print("   " + str(cd[i-1]) + "  ", end='')
        else:
            print("  " + str(cd[i-1]) + "  ", end='')
        time.sleep(0.06-anim)
    print(" \n")
    for i in range(1,7):
        if i == 1:
            print("     " + str(cd[i-1]) + "  ", end='')
        else:
            print("   " + str(cd[i-1]) + "  ", end='')
        time.sleep(0.06-anim)
    print(" ")
    print("---------------------------------------------")


# Display board function
def display_board():
    print("--------------------")
    print(" -  Money Board  - ")
    print("--------------------")
    print(str(case_values_orig[0]) + " " + str(case_values_orig[13]))
    print(str(case_values_orig[1]) + " " + str(case_values_orig[14]))
    print(str(case_values_orig[2]) + " " + str(case_values_orig[15]))
    print(str(case_values_orig[3]) + " " + str(case_values_orig[16]))
    print(str(case_values_orig[4]) + " " + str(case_values_orig[17]))
    print(str(case_values_orig[5]) + " " + str(case_values_orig[18]))
    print(str(case_values_orig[6]) + " " + str(case_values_orig[19]))
    print(str(case_values_orig[7]) + " " + str(case_values_orig[20]))
    print(str(case_values_orig[8]) + " " + str(case_values_orig[21]))
    print(str(case_values_orig[9]) + " " + str(case_values_orig[22]))
    print(str(case_values_orig[10]) + " " + str(case_values_orig[23]))
    print(str(case_values_orig[11]) + " " + str(case_values_orig[24]))
    print(str(case_values_orig[12]) + " " + str(case_values_orig[25]))
    print("--------------------")


# Remove case from stage function
def rmv_case(cd,index):
    if (index + 1) < 10:
        cd[index] = " "
    else:
        cd[index] = "  "


# Remove dollar amount from money board function
def rmv_dollar(cd,amt):
    cd2 = cd.copy()
    for z in range(0,26):
        cd2[z] = str(cd2[z].replace(" ",""))
    replacement = ""
    for b in range(0,len(amt)+1):
        replacement = replacement + " "
    r_index = cd2.index(amt)
    cd[r_index] = replacement


# Delete dollar amount from integer array, for offer calculation
def del_offer(cd,amt):
    if amt == "$0.01":
      r_index = cd.index(0.01)
    else:
        r_index = cd.index(int(''.join(filter(str.isdigit, amt))))
    del cd[r_index]


# Swap cases at end of game
def swap_case(cd,current_val):
    s_index = cd.index(current_val)
    del cd[s_index]
    return int(cd[0])

    
###################################################################
# Gameplay #

print("Eric Anderson")
print("April 11th, 2021")

end_game = False # Allows for replaying of the game, so long as the player specifies
winnings = [] # Should a player play more than once, this stores their winnings per game
profit = [] # winnings minus value inside chosen case
while not end_game:

    # "Global variables" - arrays to store case/dollar amounts
    num_round = [6,5,4,3,2,1,1,1,1,1] # Cases to open per round
    
    # Increment 1 to 26 for display
    cases_display = []
    for c in range(1,27):
        cases_display.append(c) 

    # Money board. Weird spacing to accommodate character lengths on the board output
    case_values_orig = [' $0.01', ' $1', ' $5', ' $10', ' $25', ' $50', ' $75', ' $100', ' $200', ' $300', ' $400', ' $500', ' $750',
                        '  $1,000', '     $5,000', '     $10,000', '    $25,000', '    $50,000', '    $75,000', '    $100,000', '   $200,000',
                        '   $300,000', '   $400,000', '   $500,000', '   $750,000', '   $1,000,000']

    # Preserve ordered copy of money board, create shuffled version for gameplay
    case_values = case_values_orig.copy()
    random.shuffle(case_values)
    case_values_int = case_values.copy()

    # Shuffled cases in the integer type
    for a in range(0,26):
        if case_values_int[a] == " $0.01":
          case_values_int[a] = 0.01
        else:
            case_values_int[a] = int(''.join(filter(str.isdigit, case_values_int[a])))
        
    case_values_int_sorted = case_values_int.copy()
    case_values_int_sorted.sort()
     
    # Slowly populates as player chooses cases, prevents re-choosing.
    cases_chosen = []
    
    # Track the banker's offers per game
    offers = [] 

    # Initialize genie (10% chance of summoning, gives player some perks)
    genie = random.randint(91,100)*10000
    case_clue = 0
    case_penny = random.randint(1,5)
    if case_penny == 3: 
        case_clue = case_values.index(" $0.01") + 1
    else:
        case_clue = case_values.index(case_values_orig[18:26][random.randint(0,7)]) + 1
    if genie == 1000000:
        print("\n\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n\n")
        time.sleep(2.5)
        print("Psst. Hello, player.\n")
        time.sleep(2.5)
        print("I am a genie.\n")
        time.sleep(2.5)
        print("You are among the 10% of players who summon me.\n")
        time.sleep(3.5)
        print("Therefore, I will grant you a gift for your serendipity.\n")
        time.sleep(3.5)
        print("Each round, I will secretly provide one or two case numbers that are guaranteed to have low amounts.\n")
        time.sleep(5.5)
        print("I foresee you doing quite well.\n")
        time.sleep(2.5)
        print("Before I go... something about Case " + str(case_clue) + " feels magical. Interpret that however you would like.\n")
        time.sleep(5.5)
        print("Ciao!")
        time.sleep(1.5)
        print("\n\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n\n")

    # Begin gameplay text
    # Obtain name and case choice, give instructions (dramatically...)
    print(" ")
    print("----------------------------")
    print("Welcome to Deal or No Deal!")
    print("----------------------------")
    time.sleep(2.5)
    print(".\n.")
    print("Get ready to play for $1,000,000!")
    time.sleep(2.5)
    print(".\n.")
    if len(winnings) == 0:
      player = input_error_handle("But first... what is your name? ",0)
      print(".\n.")
      print("Great to have you with us, " + str(player) + ". I hope you walk out of here with a lot of money.")
      print(".\n.")
      time.sleep(4.5)
      print("Okay! Let's bring out the cases. Ladies, please.")
    else:
      print("Okay, " + str(player) + "! The cases have been re-randomized. Let's bring them out. Ladies, please.")
    time.sleep(2.5)
    print(".\n.")
    display_cases(cases_display,0)
    time.sleep(1.5)
    print(".\n.")

    your_case = input_error_handle("You know the rules, " + str(player) + ". Pick a case number between 1 and 26: ",1)
    rmv_case(cases_display,int(your_case)-1)

    print(".\n.")
    print("You picked case " + str(your_case) + ".")
    time.sleep(1.5)
    print(".\n.")
    print("That is your case to keep throughout the game, unless you decide to sell it, which we'll discuss later.")
    time.sleep(4.5)
    print(".\n.")
    print("After each round of opening cases, the banker will offer to buy your case, at which time I will ask: ")
    time.sleep(4.5)
    print(".\n.")
    print("Deal... ", end='')
    time.sleep(2)
    print("or no deal?")
    time.sleep(2.5)
    print(".\n.")
    print("This is a game of risk, a game of timing, a game of luck. Will you have the guts to play all the way to the end?")
    time.sleep(4.5)
    print(".\n.")
    ready = input_error_handle("Are you ready, " + str(player) + "? ",6)
    print(".\n.")
    print("Then let's play Deal or No Deal! We'll start by opening 6 cases.")
    time.sleep(4.5)
    print(".\n.")
    print("The dollar amounts in those cases are not in yours. Let's hope you have $1,000,000.")
    time.sleep(4.5)
    print(".\n.\n")

    # Start the game
    play = 1
    penny_gone = False
    mil_gone = False
    top_amts_gone = 0
    for r in range(1,len(num_round)): # Loop controlling round number
        # Genie's suggestions, if a player is lucky to have the genie
        if case_penny == 3:
            genie_suggest = [x for x in case_values_int_sorted if (x < statistics.median(case_values_int_sorted) and x != 0.01)]
        else:
            genie_suggest = [x for x in case_values_int_sorted if x < statistics.median(case_values_int_sorted)] 
        random.shuffle(genie_suggest)
        if r < 5 and len(genie_suggest) >= 2:
            genie_suggest = genie_suggest[0:2]
            g_sort = [case_values_int.index(genie_suggest[0])+1,case_values_int.index(genie_suggest[1])+1]
            g_sort.sort()
            genie_1 = g_sort[0]
            genie_2 = g_sort[1]
        elif r < 7 and len(genie_suggest) >= 1:
            genie_suggest = genie_suggest[0:1]
            genie_1 = case_values_int.index(genie_suggest[0])+1
        dollars_chosen = [] # Captures values picked in current round
        if play == 1:
            print("--------------------")
            print("      Round " + str(r))
            for case in reversed(range(1,num_round[r-1]+1)): # Loop controlling number of cases left per round
                if case == 1:
                    print("   " + str(case) + " case to open")
                else:
                    print("  " + str(case) + " cases to open")
                if case == num_round[r-1]:
                  print("--------------------")
                else:
                  print(" ")
                display_board()
                display_cases(cases_display,0.06)
                print("Your case: " + str(your_case))
                if genie == 1000000:
                    if r < 5 and len(genie_suggest) >= 2:
                      print("Genie's suggestions: " + str(genie_1) + " and " + str(genie_2))
                    elif r < 7 and len(genie_suggest) >= 1:
                       print("Genie's suggestion: " + str(genie_1))
                    else:
                        print("Genie's suggestion: You gotta take it from here!")
                print("\n")
                choice = input_error_handle("Pick a case: ",2)
                choice_amt = str(case_values[int(choice)-1]).replace(" ","")
                dollars_chosen.append(int(''.join(filter(str.isdigit,choice_amt))))
                extra_drama = random.randint(1,11)
                if (extra_drama <= r - 1.5 + (6-case)*0.5): # Add some case-opening dramatic text, more likely as rounds and cases progress
                    if penny_gone:
                        print("Please, let's keep it a low number. Ideally, let's see $" + str("{:,}".format(min(case_values_int_sorted))) + ".")
                        if r > 4:
                            time.sleep(4.5)
                            print("Anything but $" + str("{:,}".format(max(case_values_int_sorted))) + ".")
                    elif top_amts_gone > 5:
                        print("Come on, please... we need a low number here.")
                    else:
                        print("Please, let's see a low number. Ideally, let's see that penny.")
                    time.sleep(4.5)
                    print(".\n.")
                    print("Open the case...")
                    time.sleep(4.5)
                else:
                    print("Alright, open the case...")
                    time.sleep(2.5)
                print("\n\n")
                print("   " + choice_amt)
                print("\n")
                time.sleep(2.5)
                text_time = time.time()

                if choice_amt == "$1,000,000": # LOTS of Situational text based on extreme case choices #
                    mil_gone = True
                    print("Oh, no! You knocked out $1,000,000.")
                    time.sleep(2.5)
                if choice_amt == "$0.01":
                    penny_gone = True
                    print("Nice! You found the penny!")
                    time.sleep(2.5)
                if (statistics.mean(case_values_int_sorted[0:len(case_values_int_sorted)-1]) < 12000) and (int(''.join(filter(str.isdigit,choice_amt))) == max(case_values_int_sorted)):
                    print("... That is devastating.")
                    time.sleep(3.5)
                if int(''.join(filter(str.isdigit,choice_amt))) < statistics.median(case_values_int_sorted): 
                    if choice_amt != "$0.01":
                        print("Great selection! $" + str("{:,}".format(int(''.join(filter(str.isdigit,choice_amt))))) + " is off the board!")
                        time.sleep(4.5)
                    if int(''.join(filter(str.isdigit,choice_amt))) <= 100 and random.randint(1,5) == 5:
                        print("I bet you're happy about that one!")
                        time.sleep(4.5)
                if int(''.join(filter(str.isdigit,choice_amt))) == max(case_values_int_sorted):
                    print("That was the largest amount in play. Oof. But, you could still win $" + str("{:,}".format(case_values_int_sorted[len(case_values_int_sorted)-2])) + ".")
                    time.sleep(3.5)
                if int(''.join(filter(str.isdigit,choice_amt))) >= 100000:
                    top_amts_gone = top_amts_gone + 1
                    if top_amts_gone == 7:
                        print("Unfortunately, all top 7 amounts are gone.")
                    elif top_amts_gone != 7:
                        print("Don't fret: even though $" + str("{:,}".format(int(''.join(filter(str.isdigit,choice_amt))))) + " is gone, " + str((7-top_amts_gone)) + " of the top 7 amounts are still available.") 
                        time.sleep(2.5)
                        if int(''.join(filter(str.isdigit,choice_amt))) != max(case_values_int_sorted):
                           print("Including $" + str("{:,}".format(case_values_int_sorted[len(case_values_int_sorted)-2])) + "!")
                    time.sleep(4.5)
                if int(''.join(filter(str.isdigit,choice_amt))) == case_values_int_sorted[len(case_values_int_sorted)-2] and int(''.join(filter(str.isdigit,choice_amt))) < 100000:
                     print("Hey, that's okay, that's okay! You still have $" + str("{:,}".format(max(case_values_int_sorted))) + " in play.")
                     time.sleep(4.5)
                if int(''.join(filter(str.isdigit,choice_amt))) == min(case_values_int_sorted):
                     if penny_gone:
                       print("You knocked out the lowest number! You cannot finish the game with less than $" + str("{:,}".format(case_values_int_sorted[1])) + ".")
                       time.sleep(4.5)
                     elif int(''.join(filter(str.isdigit,choice_amt))) != 1:
                       print("You knocked out the lowest number! You cannot finish the game with less than $1.")
                       time.sleep(4.5)
                if time.time() - text_time < 2.5:
                    print("Not bad: $" + str("{:,}".format(int(''.join(filter(str.isdigit,choice_amt))))) + " is not in your case.")
                    time.sleep(2.5)
                print("\n\n")

                rmv_case(cases_display, int(choice)-1) # Remove selected case from screen
                rmv_dollar(case_values_orig, choice_amt) # Remove revealed dollar amount from board
                del_offer(case_values_int_sorted, choice_amt) # Remove dollar amount from offer consideration
                

            # Calculate offer. Grows closer to expected value of remaining dollar amounts
            # as rounds progress. Random normal noise skews offer about +/- 5%.
            # Offer_compare is used to determine what the host says (good round vs bad round).
            offer_compare = 50000
            if r != 1:
                offer_compare = offer
            offer_var = 1 - random.gauss(1,0.05)
            offer = round(statistics.mean(case_values_int_sorted)*(.30 + offer_var + r*.08)/10)*10
            if r < 6 and max(dollars_chosen) <= 50000:
                print("The highest amount you knocked out that round was $" + "{:,}".format(max(dollars_chosen)) + ". Well done!")
                time.sleep(4.5)
                print(".\n.")
            if r != 1:
                if (offer_compare*0.89) >= offer:
                    if r < 6:
                        print("Round " + str(r) + " is finally over. Boy, that was rough. Now we'll hear another offer from the banker.")
                    else:
                        print("Round " + str(r) + " is over. That round was rough. But now we'll hear another offer from the banker.")
                elif (offer_compare*1.2) <= offer:
                    print("Round " + str(r) + " is over, that was a fantastic round! Now we'll hear another offer from the banker.")
                else:
                    print("Round " + str(r) + " is over; that was a decent round. Let's see how the banker will react.")
            elif r != 1 and offer < 25000:
                print("That was rough, but the first round is over. Now we'll hear another offer from the banker.")
            else:
                print("Round " + str(r) + " is over. Now we'll hear an offer from the banker. He wants to buy your case for as little as possible.")
                time.sleep(1.5)
            time.sleep(4.5)        
            print(".\n.")
            print("[Ring Ring Ring] ... there he is. ... Hello?")
            time.sleep(2.5)
            if len(offers) != 0:
                print(".\n.")
                print(" ")
                print("Previous offers:")
                for o in range(1,r):
                    print("$" + str("{:,}".format(offers[o-1])))
                print(" ")
            time.sleep(6.5)
            print(".\n.")
            if r > 2 and top_amts_gone < 4 and (offer_compare*1.25) <= offer:
                print("This is a player's board. The banker admits you are making him nervous.")
                time.sleep(4.5)
                print(".\n.")
            elif r > 1 and top_amts_gone > 4 and mil_gone and (offer_compare*0.7) >= offer:
                print("The banker is laughing at how poorly you just did. How cruel of him.")
                time.sleep(4.5)
                print(".\n.")
            if len(offers) > 3 and (offer > offers[len(offers)-1]*1.1) and (offers[len(offers)-1] > offers[len(offers)-2] and
                                   (offers[len(offers)-2] > offers[len(offers)-3]) and offer >= 100000):
                print("You seem to be intimidating him. He is embarrassed to be offering this much money.")
                time.sleep(4.5)
                print(".\n.")
            elif len(offers) > 2:
                if (offer > offers[len(offers)-1]*1.1) and (offers[len(offers)-1] > offers[len(offers)-2]):
                    print("The offers continue to climb.")
                    time.sleep(4.5)
                    print(".\n.")
                elif (offer < offers[len(offers)-1]*1.1) and (offers[len(offers)-1] < offers[len(offers)-2]):
                    print("The offers continue to drop. You are making the banker feel very confident.")
                    time.sleep(4.5)
                    print(".\n.")
                elif (offer < offers[len(offers)-1]*1.1) and (offers[len(offers)-1] > offers[len(offers)-2]) and (offers[len(offers)-2] > offers[len(offers)-3]):
                    print("It seems the banker enjoyed that round... but don't get discouraged.")
                    time.sleep(4.5)
                    print(".\n.")
                elif (offer > offers[len(offers)-1]*1.1) and (offers[len(offers)-1] < offers[len(offers)-2]):
                    print("Things are looking better for you. Let's keep the momentum going up.")
                    time.sleep(4.5)
                    print(".\n.")
            if (offer_compare*1.60) <= offer and r != 1 and offer >= 50000:
                print("This offer skyrocketed. Are you ready to hear it?")
                time.sleep(3.5)
                print(".\n.")
            elif (offer_compare*1.25) <= offer and offer >= 100000:
                print("This is an excellent offer. Six figures. Are you ready to hear it?")
                time.sleep(3.5)
                print(".\n.")
            elif (offer_compare*1.25) <= offer and offer >= 30000:
                print("This is an excellent offer. Are you ready to hear it?")
                time.sleep(3.5)
                print(".\n.")               
            elif (offer_compare*0.60) >= offer and offer >= 750:
                print("This offer plummeted. Are you ready to hear it?")
                time.sleep(3.5)
                print(".\n.")
            if r == 1:
                print("Okay, your first offer is...")
            else:
                print("Okay, your new offer is...")
            time.sleep(3.5)
            print("\n")
            print("   $" + str("{:,}".format(offer)))
            print("\n")
            offers.append(offer)
            time.sleep(2.5)
            reaction = random.randint(1,10)
            if reaction < 7:
                print("Think about it for a second. Look at the board:")
            else:
                print("Before you make your decision, look at the board:")
            time.sleep(2.5)
            display_board()
            time.sleep(4.5)
            print(".\n.")
            if r > 2: # Gives probability of leaving with more than a large figure
                if max(case_values_int_sorted) >= 100000:
                    cutoff = [x for x in case_values_int_sorted if x >= 100000]
                    if len(cutoff) == 1:
                        print("There is a " + str(round(len(cutoff) / len(case_values_int_sorted)*100)) +
                              "% chance that your case holds $" + str("{:,}".format(min(cutoff))) + ".")
                    else:
                        print("There is a " + str(round(len(cutoff) / len(case_values_int_sorted)*100)) +
                              "% chance that your case holds at least $" + str("{:,}".format(min(cutoff))) + ".")
                    time.sleep(4.5)
                    print(".\n.")
                elif max(case_values_int_sorted) < 100000 and max(case_values_int_sorted) >= 1000:
                    cutoff = [x for x in case_values_int_sorted if x >= max(case_values_int_sorted)]
                    if len(cutoff) == 1:
                        print("There is a " + str(round(len(cutoff) / len(case_values_int_sorted)*100)) +
                              "% chance that your case holds $" + str("{:,}".format(min(cutoff))) + ".")
                    else:
                        print("There is a " + str(round(len(cutoff) / len(case_values_int_sorted)*100)) +
                              "% chance that your case holds at least $" + str("{:,}".format(min(cutoff))) + ".")                        
                    time.sleep(4.5)
                    print(".\n.")
            if r > 3 and random.randint(1,10-r) < 2 and statistics.mean(case_values_int_sorted) > 10000:
                print("Do you have the guts to go all the way, " + str(player) + "?")
                time.sleep(4.5)
                print(".\n.")                   
            if r == 9:
                print("This is the final offer. If you say 'No Deal', we'll be done opening cases.")
            elif num_round[r] == 1:
                print("If you say no deal, you must open " + str(num_round[r]) + " more case.")
            else:
                print("If you say no deal, you must open " + str(num_round[r]) + " more cases.")     
            time.sleep(4.5)
            print(".\n.")
            print("Now I must ask you, " + str(player) + ": ", end = '')
            print("Deal... ", end='')
            time.sleep(2)
            d_o_n_d = input_error_handle("or no deal? ",3)
            
            # Different scenarios depending on answer. No Deal loops back. Deal ends loop, reveals results.
            if d_o_n_d.lower() in "deal":
                print(".\n.")
                print("Deal! You're walking out of here with $" + str("{:,}".format(offer)) + "! Wow!")
                time.sleep(4.5)
                print(".\n.")
                print("But was that a good deal?")
                time.sleep(2.5)
                print(".\n.")
                print("You sold your case (case number " + str(your_case) + ") for $" + str("{:,}".format(offer)) + ". It was worth:")
                your_case_dollar = str(case_values[int(your_case)-1]).replace(" ","")
                time.sleep(5.5)
                print("\n")
                print("   " + your_case_dollar)
                print("\n")
                time.sleep(3.5)
                if int(''.join(filter(str.isdigit, your_case_dollar))) >= int(offer):
                    if int(''.join(filter(str.isdigit, your_case_dollar))) >= 5000:
                        print("You didn't make such a great deal, " + str(player) + ". However, you're still walking out of here with a lot of money.")
                    else:
                        print("You didn't make such a great deal, " + str(player) + ". But that's how the cookie crumbles sometimes.")
                    if int(''.join(filter(str.isdigit, your_case_dollar))) == 1000000:
                        print("You could have been a MILLIONAIRE!")
                else:
                    print("You made an excellent deal, " + str(player) + "! You walked away at the appropriate time.")     
                play = 0
                time.sleep(4.5)
                print(".\n.")
                print("Ladies, open your cases.")
                time.sleep(2.5)
                print(".\n.")
                print(" ")
                for end in range(1,27):
                    if end not in cases_chosen:
                        if case_values[int(end)-1] == " $0.01":
                           print("Case " + str(end) + ": $0.01")
                        else:
                           print("Case " + str(end) + ": " + str(case_values[int(end)-1]).replace(" ",""))
                time.sleep(4.5)
                your_new_case_dollar = offer
            else:
                print(".\n.")
                if r == len(num_round) - 1:
                    print("No Deal! We are finished opening cases.")
                else:
                    print("No Deal! We're moving on to Round " + str(r+1) +". Good luck!")
                time.sleep(3.5)
                print(".\n.")
                print("\n")

    # Only two cases remaining, last phase of game if no offers accepted. A ton of if/else statements to account for the $0.01 string.
    if play == 1:
        if case_values[int(your_case)-1] == " $0.01":
            your_case_dollar = 0.01
            remaining = [your_case_dollar,str(swap_case(case_values_int_sorted,your_case_dollar))]
            remaining[1] = int(''.join(filter(str.isdigit,"{:,}".format(int(''.join(filter(str.isdigit, remaining[1])))))))
            remaining.sort()
            print("There are only two cases remaining, one with $0.01 and another with $" + "{:,}".format(int(''.join(filter(str.isdigit,str(remaining[1]))))) + ".")
        elif 0.01 in case_values_int_sorted:
            your_case_dollar = "{:,}".format(int(''.join(filter(str.isdigit, str(case_values[int(your_case)-1]).replace(" ","")))))
            remaining = [your_case_dollar,0.01]
            remaining[0] = int(''.join(filter(str.isdigit, remaining[0])))
            remaining.sort()
            print("There are only two cases remaining, one with $0.01 and another with $" + "{:,}".format(int(''.join(filter(str.isdigit,str(remaining[0]))))) + ".")
        else:
            your_case_dollar = "{:,}".format(int(''.join(filter(str.isdigit, str(case_values[int(your_case)-1]).replace(" ","")))))
            remaining = [your_case_dollar,str(swap_case(case_values_int_sorted,int(''.join(filter(str.isdigit, your_case_dollar)))))]
            remaining = [int(''.join(filter(str.isdigit, remaining[0]))),
                         int(''.join(filter(str.isdigit,"{:,}".format(int(''.join(filter(str.isdigit, remaining[1])))))))]
            remaining.sort()
            print("There are only two cases remaining, one with $" + "{:,}".format(int(''.join(filter(str.isdigit,str(remaining[0]))))) +
                  " and another with $" + "{:,}".format(int(''.join(filter(str.isdigit,str(remaining[1]))))) + ".")
        time.sleep(4.5)
        print(".\n.")
        print("You chose to decline all of the banker's offers, meaning you are leaving here with one of these two amounts.")
        time.sleep(4.5)
        print(".\n.")
        swap = input_error_handle(str(player) + ", would you like to swap cases ('Yes' or 'No')? ",4)
        print(".\n.")
        your_new_case_dollar = 0
        time.sleep(0.5)
        if swap.lower() in "yes":
            if case_values_int_sorted[0] == 0.01:
                your_new_case_dollar = 0.01
            else:
                your_new_case_dollar = "{:,}".format(int(case_values_int_sorted[0]))
            print("Alright. Was swapping the smart choice? Let's find out. You are going home with: ")
        else:
            your_new_case_dollar = your_case_dollar
            print("Alright. You are going home with the amount in your case. Your case is holding: ")
        time.sleep(5.5)
        if "$" in case_values_orig[0] and isinstance(your_new_case_dollar, float):
            your_new_case_dollar = "0.01"
        print("\n")
        print("   $" + your_new_case_dollar)
        print("\n")
        time.sleep(2.5)
        if int(''.join(filter(str.isdigit, str(your_new_case_dollar)))) == 1000000:
            print("You're a MILLIONAIRE!")
        elif your_new_case_dollar == "0.01":
            print("You've won a penny! Just as improbable as winning $1,000,000; but much less exciting.")
            time.sleep(4.5)
            print(".\n.")
            print("After we cut out the taxes, we'll send you what's left of the coin.")
            print(".\n.")
            time.sleep(4.5)
        if swap.lower() in "yes":
            if int(''.join(filter(str.isdigit, str(your_new_case_dollar)))) <= int(''.join(filter(str.isdigit, str(your_case_dollar)))):
                print("You shouldn't have swapped, " + str(player) + "! However, you're still walking out of here with some money.")
                print(".\n.")
                if isinstance(your_case_dollar, float):
                    print("Your original case held $0.01.")
                else:
                    print("Your original case held $" + "{:,}".format(int(''.join(filter(str.isdigit, str(your_case_dollar))))) + ".")
            else:
                if isinstance(your_case_dollar, float):
                    print("Good call on the swap, " + str(player) + "! Your original case held $0.01.")
                else:
                    print("Good call on the swap, " + str(player) + "! Your original case held $" + "{:,}".format(int(''.join(filter(str.isdigit, str(your_case_dollar))))) + ".")
        else:
            if case_values_int_sorted[0] >= int(''.join(filter(str.isdigit, str(your_new_case_dollar)))):
                print("You should have swapped, " + str(player) + "! However, you're still walking out of here with a fair deal of money.")
                print(".\n.")
                if your_new_case_dollar == "0.01":
                    print("Your case held $0.01.")
                else:
                    print("Your case held $" + "{:,}".format(int(''.join(filter(str.isdigit, str(your_new_case_dollar))))) + ".")
            else:
                if your_new_case_dollar == "0.01":
                    print("Glad you kept your case, " + str(player) + "! Your case held $0.01.")
                else:
                    print("Glad you kept your case, " + str(player) + "! Your case held $" + "{:,}".format(int(''.join(filter(str.isdigit, str(your_new_case_dollar))))) + ".")
        if genie == 1000000 and case_penny == 3: # Genie could trick player in keeping $0.01
            time.sleep(4.5)
            print(".\n.")
            print("Looks like the genie tricked you! Mwahahaha!")
    winnings.append(int(''.join(filter(str.isdigit, str(your_new_case_dollar)))))
    profit.append(int(''.join(filter(str.isdigit, str(your_new_case_dollar)))) - int(''.join(filter(str.isdigit, str(your_case_dollar)))))
    time.sleep(4.5)
    print("\n")
    print("-----------------------------------------------------------")
    print("Congratulations, " + str(player) + "! Thanks for playing.")
    print(" ")
    print("Earnings and profit for today:")
    for w in range(1,len(winnings)+1):
        if profit[w-1] < 0:
            if genie == 1000000:
                print("Game " + str(w) + ": $" + "{:,}".format(winnings[w-1]) + " (-$" + "{:,}".format(abs(profit[w-1])) + ") with genie") 
            else:
                print("Game " + str(w) + ": $" + "{:,}".format(winnings[w-1]) + " (-$" + "{:,}".format(abs(profit[w-1])) + ")")
        else:
            if genie == 1000000:
                print("Game " + str(w) + ": $" + "{:,}".format(winnings[w-1]) + " (+$" + "{:,}".format(abs(profit[w-1])) + ") with genie")
            else:
                print("Game " + str(w) + ": $" + "{:,}".format(winnings[w-1]) + " (+$" + "{:,}".format(abs(profit[w-1])) + ")")
    print(" ")
    if sum(profit) < 0:
        print("Total:  $" + "{:,}".format(sum(winnings)) + " (-$" + "{:,}".format(abs(sum(profit))) + ")")
    else:
        print("Total:  $" + "{:,}".format(sum(winnings)) + " (+$" + "{:,}".format(abs(sum(profit))) + ")")              
    print("-----------------------------------------------------------")
    print("\n")
    time.sleep(2.5)
    play_again = input_error_handle("Play again? ",5)
    if play_again.lower() == "no":
        end_game = True
        print("Goodbye!")
    else:
        print("Okay, here we go!")
    time.sleep(2.5)
    print("\n")

# END #
