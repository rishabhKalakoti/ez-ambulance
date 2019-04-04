from bottle import Bottle, run, template, static_file, request, route, redirect
import os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

@app.get("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root=os.path.join(dir_path, "static"))

run(app, host="localhost", port=8080)
