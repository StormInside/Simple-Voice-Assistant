from action import Action
from recognition import Recognition

act = Action()
rec = Recognition()
while True:
    rec.start(act)