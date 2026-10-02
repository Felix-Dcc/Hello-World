from projects.treasure_island import BANNER, START, STORY, Ending, step
from terminal import run


def main():
    print(BANNER)
    print("""  Welcome to Treasure Island.
Your mission is to find the treasure!
      """)

    scene = START
    while not isinstance(STORY[scene], Ending):
        answer = input(STORY[scene].prompt + ' \n')
        try:
            scene = step(scene, answer)
        except ValueError as e:
            print(e)          # ask the same question again

    print(STORY[scene].message)


if __name__ == '__main__':
    run(main)
