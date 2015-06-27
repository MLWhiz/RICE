"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary

import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    dict_scr = {}
    for elem in hand:
        if elem in dict_scr.keys():
            dict_scr[elem]+=elem
        else:
            dict_scr[elem]=elem
    scr = 0
    for _,value in dict_scr.items():
        if value>scr:
            scr=value
    return scr


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = [x for x in range(1,num_die_sides+1)]
    all_tuples=gen_all_sequences(outcomes,num_free_dice)
    all_final_tuples = [tuple(list(x)+list(held_dice)) for x in all_tuples]
    all_scores = [score(x) for x in all_final_tuples]
    expected_val = sum(all_scores)/float(len(all_scores))
    return expected_val

#print score((2, 2))
#print expected_value((2, 2), 6, 2) 

#expected 5.83333333333 but received 11.0

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    answer = set([()])
    for ind in range(0,len(hand)):
        temp_set = set()
        for partial_sequence in answer:      
            new_sequence = list(partial_sequence)
            new_sequence.append(hand[ind])
            temp_set.add(tuple(new_sequence))
        answer = set(list(answer)+list(temp_set))
    return answer

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    holds=gen_all_holds(hand)
    scr = 0.0
    best_hold = ()
    for hold in holds: 
        val = expected_value(hold, num_die_sides, len(hand)-len(hold))
        if  val > scr: 
            scr = val
            best_hold = hold
        #print val,hold
    return (scr, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 2, 2, 6, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()

print expected_value((2, 2), 6, 2) 

#expected 5.83333333333 but received 11.0
#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



