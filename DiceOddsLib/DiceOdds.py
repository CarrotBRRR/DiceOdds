"""
DiceOdds.py
===
Command line tool to calculate the odds of rolling a certain sum with multiple dice.
It can also roll the dice and show the result.
Can also be used as a library.

Usage:
python DiceOdds.py [dice1] ... [-p|--prob] [-g|--graph] [-o|--occ] [-r|--roll]

Authors: 
-----
Dominic Choi
    GitHub: [CarrotBRRR](https://github.com/CarrotBRRR)
"""

import sys
import re
from collections import Counter
from itertools import product
from pandas import DataFrame
import random as rand

def parse_die(arg : str) -> int:
    """
    Parses a die argument in the form of d[faces] and returns the number of faces on the die.
    """
    match = re.fullmatch(r'd(\d+)', arg.lower())
    if not match or int(match.group(1)) < 1:
        raise ValueError(f"Invalid die format: {arg}")
    
    return int(match.group(1))

def parse_args(args : list) -> tuple:
    """
    Separates command line arguments into dice and flags.
    """
    dice = []
    flags = []

    for arg in args:
        if arg.startswith('-'):
            flags.append(arg)

        else:
            try:
                dice.append(arg)
            except ValueError as e:
                print(e)
                sys.exit(1)

    return dice, flags

def process_flags(flags : list) -> tuple:
    """
    Processes command line flags and returns a tuple of boolean values indicating which flags are set.
    """

    flag_args = [
        '-p', '--prob',
        '-o', '--occ',
        '-g', '--graph',
        '-r', '--roll',
        '-h', '--help'
    ]

    for flag in flags:
        if flag not in flag_args:
            print(f"Invalid flag: {flag}")
            sys.exit(1)

    show_prob = '-p' in flags or '--prob' in flags
    show_occurrences = '-o' in flags or '--occ' in flags 
    show_graph = '-g' in flags or '--graph' in flags 

    do_roll = '-r' in flags or '--roll' in flags 

    show_help = '-h' in flags or '--help' in flags or 'help' in flags or (not show_prob and not show_occurrences and not show_graph and not do_roll)
    if show_help:
        print("Usage: python DiceOdds.py [dice1] ... [-p|--prob] [-g|--graph] [-o|--occ] [-r|--roll]")
        print()
        print("Example: python DiceOdds.py d6 d8 -p -g -o")
        print()
        print("Flags:")
        print("-p, --prob: Show probabilities")
        print("-o, --occ: Show occurrences")
        print("-g, --graph: Show a graph of occurrences")
        print("-r, --roll: Roll the specified dice")
        print("-h, --help: Show this help message")

        show_prob = False
        show_occurrences = False
        show_graph = False
        do_roll = False

    return show_prob, show_occurrences, show_graph, do_roll, show_help


def generate_all_rolls(dice_faces : list) -> list:
    """
    Generates all possible rolls for the given dice faces.
    """
    ranges = [range(1, faces + 1) for faces in dice_faces] # Create ranges for each die
    return list(product(*ranges)) # Return all combinations of faces

def process_dice(dice_faces : list) -> tuple:
    """
    Calculates the probabilities of sums for the given dice faces.
    """
    results = []
    
    rolls = generate_all_rolls(dice_faces) # Generate all possible rolls
    sum_counts = Counter(sum(roll) for roll in rolls) # Count occurrences of each sum (get roll value)
    total_combinations = len(rolls) # Total number of combinations

    # Find the maximum occurrences for scaling the graph
    max_occurrences = max(sum_counts.values())

    for total in sorted(sum_counts):
        # Calculate the probability for each sum
        count = sum_counts[total]
        probability = count / total_combinations

        # Create a graph representation
        graph = get_graph_line(count, max_occurrences)

        # Append the results
        results.append((int(total), probability, int(count), graph))

    return results, total_combinations

def print_graph(df: DataFrame):
    """
    Prints a graph representation of the sums and their occurrences.
    """
    max_sum = int((df['Sum'].max()))
    max_sum_len = len(str(max_sum)) # number of digits
    max_occurrences = int(df['Occurrences'].max())

    spaces = ' ' * (max_sum_len - 5)
    graph = f"Sums {spaces}| Graph"
    # Create a graph with proper spacing
    for index, row in df.iterrows():
        # Determine the number of spaces needed for alignment
        sum_len = len(str(int(row['Sum'])))
        n_spaces = max((max_sum_len - sum_len), (4 - sum_len))
        spaces = ' ' * n_spaces

        occurrences = get_graph_line(int(row['Occurrences']), max_occurrences)

        graph += f"\n{spaces}{int(row['Sum'])} | {occurrences} {int(row['Occurrences'])}"

    print(graph)

def get_graph_line(n_occurrences : int, max_occurrences : int) -> str:
    """
    Returns a graph string for the given occurrences.
    """
    if max_occurrences > 50:
        # return '█' * int((n_occurrences / max_occurrences) * 100 + 1)
        return '=' * int((n_occurrences / max_occurrences) * 50 + 1)
    else:
        # return '█' * n_occurrences
        return '=' * n_occurrences

def DiceOdds(args : list = None):
    # Extract flags and die arguments
    if args is None:
        args = sys.argv[1:]

    if not args:
        print("Usage: python DiceOdds.py [dice1] ... [-p|--prob] [-g|--graph]")
        sys.exit(1)

    # Separate flags from dice arguments
    dice, flags = parse_args(args)

    show_prob, show_occurrences, show_graph, do_roll, show_help = process_flags(flags)

    if show_help:
        return

    if not dice:
        print("Error: No dice specified.")
        sys.exit(1)

    try:
        dice_faces = [parse_die(arg) for arg in dice]

    except ValueError as e:
        print(e)
        sys.exit(1)

    # Process the dice
    results, total_combinations = process_dice(dice_faces)

    # Convert to DataFrame
    df = DataFrame(results, columns=['Sum', 'Probability', 'Occurrences', 'Graph'])

    print()
    
    if show_prob and show_occurrences and show_graph:
        print(df.to_string(index=False, columns=['Sum', 'Occurrences', 'Probability', 'Graph']))
        print()

    elif show_prob and show_occurrences:
        print(df.to_string(index=False, columns=['Sum', 'Occurrences', 'Probability']))
        print()

    elif show_prob and show_graph:
        print(df.to_string(index=False, columns=['Sum', 'Probability', 'Graph']))
        print()

    elif show_occurrences and show_graph:
        print(df.to_string(index=False, columns=['Sum', 'Occurrences','Graph']))
        print()

    elif show_prob:
        print(df.to_string(index=False, columns=['Sum', 'Probability']))
        print()

    elif show_occurrences:
        print(df.to_string(index=False, columns=['Sum', 'Occurrences']))
        print()
    
    elif show_graph:
        print_graph(df)
        print()
    
    if not do_roll or show_graph or show_occurrences or show_prob:
        print(f"Total combinations: {total_combinations}")
        print()

    if do_roll:
        # Do a roll
        roll = sum(rand.choice(generate_all_rolls(dice_faces)))
        print(f"Your Roll is: {roll}")
        print()

if __name__ == "__main__":
    DiceOdds()
