from flask import render_template, request, jsonify, abort
from datetime import datetime

from app import app
from .models import Task
from .bus import Bus
from .forms import CreateTaskForm, RetriveTaskForm

from config import HOST, QUEUE, USER, PASSWORD


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",
                           title="Dr.Web")


@app.route("/create", methods=["GET", "POST"])
def create():
    form = CreateTaskForm()
    if form.validate_on_submit():
        t = Task(status="In queue",
                 creation_time=datetime.utcnow(),
                 start_time=None,
                 end_time=None,
                 difficulty=form.difficulty.data)
        Bus.DataBase.send_task_to_db(t)
        with Bus.Queue(HOST, USER, PASSWORD) as queue:
            queue.send_task_to_queue(t, QUEUE)
        return jsonify({"id": t.id})

    return render_template("create.html",
                           title="Create new task",
                           form=form)


@app.route("/status", methods=["GET"])
def status():
    form = RetriveTaskForm()
    id = request.args.get("id")
    if id is not None and id != "":
        t = Task.query.get(id)
        if t is not None:
            t = Bus.DataBase.get_task_from_db(int(id))
            return jsonify({"status": t.status,
                            "creation_time": t.creation_time,
                            "start_time": t.start_time,
                            "end_time": t.end_time,
                            "difficulty": t.difficulty})
        else:
            return abort(404)

    return render_template("status.html",
                           title="Get status of task",
                           form=form)
