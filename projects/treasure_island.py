"""Treasure Island, as a small story graph."""
from dataclasses import dataclass, field

BANNER = r'''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
'''


@dataclass
class Scene:
    prompt: str
    choices: dict = field(default_factory=dict)    # answer -> next scene id


@dataclass
class Ending:
    message: str
    won: bool = False


STORY = {
    'start': Scene('Choose a path. Left or Right?', {'left': 'lake', 'right': 'hole'}),
    'hole': Ending('You fell into a hole. Game Over!'),
    'lake': Scene('Swim or wait?', {'swim': 'trout', 'wait': 'doors'}),
    'trout': Ending('You are attacked by trout. Game Over!'),
    'doors': Scene('Which door? Red, Blue or Yellow?',
                   {'red': 'fire', 'blue': 'beasts', 'yellow': 'treasure'}),
    'fire': Ending('You are burned by fire. Game Over!'),
    'beasts': Ending('Eaten by beasts. Game Over!'),
    'treasure': Ending('Congratulations, you won! The treasure box is yours :)', won=True),
}

START = 'start'


def step(scene_id, answer):
    """The scene an answer leads to. An answer the scene doesn't offer raises
    ValueError, so the same question is asked again (the old version sent an
    unknown door straight back to the start)."""
    scene = STORY[scene_id]
    if not isinstance(scene, Scene):
        raise ValueError('The game is over')
    choice = answer.strip().lower()
    if choice not in scene.choices:
        options = ', '.join(c.title() for c in scene.choices)
        raise ValueError(f'Please enter one of: {options}')
    return scene.choices[choice]
