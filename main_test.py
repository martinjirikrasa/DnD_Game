from dungeon_test import Dungeon
from map_entities import Hero
import subprocess

if __name__ == "__main__":
    ## new game or continue
    continue_game = input("Do you want to start a new game?: Y/N\n")

    if continue_game == "N":
        input_file = input("Copy file name here and save it to this directory: ")

        dungeon = Dungeon.load(file=input_file)
        hero_name = "ben"
    elif continue_game == "Y":
        hero_name = input("What is your hero name? ")
        dungeon = Dungeon(size=(10 ,10), hero_name=hero_name)
    else:
        print("Please restart the game and type Y or N if you want to continue or not.")
        exit(0)
    while True:
        subprocess.Popen("cls", shell=True).communicate()
        print(dungeon)
        print(dungeon.message)
        action = input(f"Select an action {hero_name}: (L)EFT, (R)IGHT, (D)OWN, (U)P, (A)TTACK, (Q)UIT\n")
        if action == "Q":
            print("You coward!")
            exit(0)
        else:
            dungeon.hero_action(action)
        if dungeon.hero.hp < 1:
            print(dungeon.message)
            exit(0)