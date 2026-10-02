"""Treasure Island, as a small story graph."""
from dataclasses import dataclass, field


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
