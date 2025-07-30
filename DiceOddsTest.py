"""
LibTest.py
===
Test Suite for the libraries I've created.
-----

Authors: 
-----
Dominic Choi
    GitHub: [CarrotBRRR](https://github.com/CarrotBRRR)
"""

import sys
import DiceOddsLib.DiceOdds as DiceOdds

def test_parse_die():
    """
    Test the parse_die function.
    """
    assert DiceOdds.parse_die('d6') == 6
    assert DiceOdds.parse_die('d20') == 20
    assert DiceOdds.parse_die('d100') == 100

    try:
        DiceOdds.parse_die('dabc')
    except ValueError as e:
        assert str(e) == "Invalid die format: dabc"

    try:
        DiceOdds.parse_die('abc')
    except ValueError as e:
        assert str(e) == "Invalid die format: abc"
    try:
        DiceOdds.parse_die('d')
    except ValueError as e:
        assert str(e) == "Invalid die format: d"
    try:
        DiceOdds.parse_die('d0')
    except ValueError as e:
        assert str(e) == "Invalid die format: d0"
    try:
        DiceOdds.parse_die('d-1')
    except ValueError as e:
        assert str(e) == "Invalid die format: d-1"

def test_parse_args():
    """
    Test the parse_args function.
    """
    args = ['d6', 'd8', '-p', '-g']
    dice, flags = DiceOdds.parse_args(args)
    assert dice == ['d6', 'd8']
    assert flags == ['-p', '-g']

    args = ['-o', 'd10', '-r']
    dice, flags = DiceOdds.parse_args(args)
    assert dice == ['d10']
    assert flags == ['-o', '-r']
    args = ['d4', '-h']
    dice, flags = DiceOdds.parse_args(args)
    assert dice == ['d4']
    assert flags == ['-h']
    args = ['-g', 'd6', 'd8']
    dice, flags = DiceOdds.parse_args(args)
    assert dice == ['d6', 'd8']
    assert flags == ['-g']
    args = ['d6', 'd8', '-p']
    dice, flags = DiceOdds.parse_args(args)
    assert dice == ['d6', 'd8']
    assert flags == ['-p']
    args = ['-o', '-g', 'd10']
    dice, flags = DiceOdds.parse_args(args)
    assert dice == ['d10']
    assert flags == ['-o', '-g']
    args = ['-r', 'd4']
    dice, flags = DiceOdds.parse_args(args)
    assert dice == ['d4']
    assert flags == ['-r']

def test_process_flags():
    """
    Test the process_flags function.
    """
    flags = ['-p', '-o', '-g', '-r']
    show_prob, show_occurrences, show_graph, do_roll, show_help = DiceOdds.process_flags(flags)
    assert show_prob == True
    assert show_occurrences == True
    assert show_graph == True
    assert do_roll == True
    assert show_help == False

    flags = ['-p', '-o', '-g', '-r', '-h']
    show_prob, show_occurrences, show_graph, do_roll, show_help = DiceOdds.process_flags(flags)
    assert show_prob == False
    assert show_occurrences == False
    assert show_graph == False
    assert do_roll == False
    assert show_help == True

    flags = ['-p', '-o', '-g']
    show_prob, show_occurrences, show_graph, do_roll, show_help = DiceOdds.process_flags(flags)
    assert show_prob == True
    assert show_occurrences == True
    assert show_graph == True
    assert do_roll == False
    assert show_help == False

    flags = ['-r']
    show_prob, show_occurrences, show_graph, do_roll, show_help = DiceOdds.process_flags(flags)
    assert show_prob == False
    assert show_occurrences == False
    assert show_graph == False
    assert do_roll == True
    assert show_help == False

def test_DiceOdds():
    args = ['d6', 'd8', '-p', '-o', '-g', '-r']
    DiceOdds.DiceOdds(args)


def test_DiceOddsLib():
    print("Testing DiceOddsLib...")

    print("\tTesting parse_die...")
    test_parse_args()
    print("\ttest_parse_args passed!")

    print("\tTesting parse_args...")
    test_parse_die()
    print("\ttest_parse_die passed!")

    print("\tTesting process_flags...")
    test_process_flags()
    print("\ttest_process_flags passed!")

    print("\tTesting DiceOdds...")
    test_DiceOdds()
    print("\tDiceOdds passed!")
    print("DiceOddsLib passed!")

    return True   

def main():
    """
    Main function to run the tests.
    """
    print("Running tests...")
    if test_DiceOddsLib():
        print("All tests passed!")
    else:
        print("Some tests failed.")

if __name__ == "__main__":
    main()
    sys.exit(0)