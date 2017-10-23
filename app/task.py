from datetime import datetime
import time
import random


def run(task_model):
    time.sleep(random.randint(0, task_model.difficulty))
    return task_model, {"end_time": datetime.utcnow(), "status": "Complete"}
