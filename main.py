from taipy import Gui

page = """
# Soccer Predictor

<|toggle|theme|>
"""

Gui(page = page).run(use_reloader = True, debug = False, title = "Soccer Predictor")