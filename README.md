Welcome to AMP FELIX's GitHub!

Hey there! I'm Felix, a Python enthusiast and Golang developer, I'm on a mission to craft elegant solutions to complex problems through code. My fascination with Python stems from its versatility – whether I'm building web applications, automating tasks, or analyzing data, Python empowers me to turn ideas into reality with simplicity and efficiency.

My programming journey started with a curiosity to understand how technology shapes our world. As I go deeper into Python, I discovered its endless possibilities and fell in love with its clean syntax and powerful libraries. From scripting small utilities to developing scalable applications, Python has been my go-to tool for transforming concepts into tangible results.
Outside of coding, you'll often find me exploring the latest trends in tech, diving into open-source projects, or immersing myself in a good book on software engineering.


## The projects

Twelve small Python programs. Every one runs in the terminal, and all of them
also run together as a small web app.

### Try them in your browser

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m arcade
```

Then open http://127.0.0.1:5000.

### Or in the terminal

| Project | Terminal |
|---|---|
| Hangman | `python Hangman.py` |
| Rock, paper, scissors | `python main.py` |
| Treasure Island | `python treasure_island_project.py` |
| Password generator | `python pass_gen_project.py` |
| BMI calculator | `python bmi_calculator.py` |
| Leap year checker | `python leap_year_checker.py` |
| Chemical formula lookup (needs internet) | `python ChemicalFormula.py` |
| ATM (demo PIN 2050) | `python prompt.py` |
| Python Pizza | `python pizza_delivery_test.py` |
| Rollercoaster tickets | `python ask.py` |
| Love calculator | `python love_calculator.py` |
| Christmas tree | `python ChristmasTree.py` |

### How it's organised

```
projects/       the logic of every project: no input() or print()
*.py            the terminal versions, thin wrappers around projects/
arcade/         the web app (Flask): one page per project
tests/          pytest: the logic, every terminal script, every web page
Examination/    a separate A-Frame VR project, with its own README
```

Because the terminal scripts and the web pages call the same code in
`projects/`, a fix in one place reaches both.

### Tests

```bash
pip install -r requirements-dev.txt
pytest
```


## How to Reach Me

- **Email**: Oseipokufelix0@gmail.com
- **Twitter**: @__F3l1X

I'm open to collaborations and contributions! If you're interested in contributing to any of my projects or have ideas for collaboration, feel free to reach out to me via email or through any of my social media channels mentioned above.

I'm always eager to connect with fellow developers and enthusiasts. Whether you have questions, ideas, or just want to chat about Python or programming in general, don't hesitate to get in touch!

All projects shared here are licensed under the [MIT License](LICENSE), unless otherwise specified.

