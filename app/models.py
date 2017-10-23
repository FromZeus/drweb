from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    difficulty = db.Column(db.Integer, index=True)
    status = db.Column(db.String(20))

    def __init__(self, creation_time, start_time, end_time,
                 difficulty, status):
        self.creation_time = creation_time
        self.start_time = start_time
        self.end_time = end_time
        self.difficulty = difficulty
        self.status = status

    def __repr__(self):
        return "Task: {} Difficulty: {}".format(self.id, self.difficulty)

    @property
    def primary_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
