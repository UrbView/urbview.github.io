from flask import Flask, render_template, request, send_from_directory
from flask import Flask, request, Response

import os
import warnings
import json

html_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
app = Flask(__name__, template_folder='.')
warnings.warn("Be careful! This server isn't protected ad therefore should only be used in debugging; never in production.")

@app.route('/<path:path>/<file>.<extension>')
def file(path, file, extension):
    return send_from_directory(html_dir, f"{path}/{file}.{extension}")

@app.route('/<path:path>/')
def route(path):
    return render_template(f"{path}/index.html")

@app.route('/', methods = ['POST'])
def index():

    json_string = {
            'response': [
                {'confidence': 98.32, 'keywords': ['good','yes','green'], 'label': 0},
                {'confidence': 12.34, 'keywords': ['bad','no','red'], 'label': 1},
                {'confidence': 78.32, 'keywords': ['good','yes','green'], 'label': 1}
            ],
            'aggregation': {'confidence': 62.32, 'keywords': ['good','yes','green'], 'label': 0},
            'heatmap': "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAATLSURBVEhLjZZrets2EEVBkJQiO/vfQ5fQXeWLm9qyRKLnXICS0z8t7SuQwGAu5oEBprc//2in1+/l9O1bKe/vQfvrV2lvb+BXKR/X0j4+S9m3MpVWfPalln2dy3Raynw+BWVZS5nXckX+148f5f3nW1lP57Kup7K+vBQ51tfXUutUUaSW/QkV11oKSpvKeW0TdPbNyIMq+J7oz7MzZ9uCideJscgsc1poFOJ9ZqXtKawlEk4QaUFjvNUppIV24ptJZQ4p3w9C5t3vZYonXK/jyC14QUI7G4RTqaXd97JdP8t2u5WNSY2BKI/buuumdYAVTyHCCokGX7yCBbYuZEZOY0StzEGfsjYQ3sr946PcP2mxcmPurvuISyU+9fKtzGA6EScs191xsTyPR00sH+ULVp1Op7Szbg9mwiG5E7Fqg3CDeCOGO3MTLy1i4kxCSRwXQ9iwoCkDxe+kUKLvIE24QqZpndhfhEACjBAEFYLp5VLK60tpWOUCdlQ3Y60lyuumodDv9Dts8ijnP+8Nj7V7jy/ug9AJYcdc/L6cVyw6lyohaFiJzSTvFtI8rthEQF43+R6PGvugkzbmbIbIvLhBCEylEJoFWplVQ1KM1/lMzHDjCHigMXzHVc6RR+Ubi7qxKKAlbi/7hN+GrZCUnfBwiUBJt4B+yNIeiwrGuPBx37Ly3YS7Xmk/48IJosqYmMRwa+0Ku4U984SK6Y+7DsIhd8hCqIMTI7eT24qKZKv7JrbaRLo/SQ/CwzIXi8CNldxR4EoLk60aJpNbYkr5gliPkBB74tNjtG8dLkCr1YgU6G7PFmWOgegr5nUjFp9MvuGe/XorhbYTsh/XM7GVkJg6d8RMsjsW3Wk3SbWExOm+kpC/Bk0mxXc8rvhYuWIQ7yhoECalI2OiHMmC3FjogZS40R7JFCRjMY+FaH0ikbqH2xYsOFHdZ+PFajYItcDUbrjJuarJFsLSqiwnwsK+Xdi/K/N7dWGcRXWrRpbiBTOVsoH5bIcZYSHpXMlOCREyRrvgW8KsHm/o5shbwtg+K5VoJc5HhXmcQsO6HAwSRoFuQijVYxJYfECLkPnvp7uUSUe2pKs/Y6wPdUJdag2MewdZSl7I/gceZAfoDmkf63GlzmZT4q74K0BoIDFAKHuTCc992uHYobCTwDAQr+Vdgzrs5zjHx8O/wsBmM1uWRtw6vySEPPhC9IDKvxSHA9ZZTpfju3blg+grzMoA0mGR2FHcAr5F+lnQUJhcSE1+4kEqb/t4LxsXp7vwEM5B/Dz9dz0QKyELcMi/YJ/nYw5nIUFcOKAHZOOpDSIJb+9/l9u1kwUhHNshwt0SlXfSKQiZeLgPtwZfiRHofNRVK3zwmYqfChM3s/bjbIskM1RANudKyKYP/NaN3nUC3LgoCyQZRGNZEHqcYM1EHAM2aVIDN/St4UTBOwWhLt4ILmV++Q64Z14uXD+osxZ3CkE/lLUM/SEzHk9g4Qfn2ZXjBFLJ7GQM9RBIIniPFSr1jnMpCxfbWVxeciWplLhcsjy8Icy9B1IDkj8JCU+t/ogHUffeA/zkwivps/ML3AqHVWIQIfYAevNDAlZPZje+pDOdAeN960jWCUOq0t/AJTnwwjxuByE+SLWNltRyi5V9L/8A90bB3A5jOCQAAAAASUVORK5CYII="
            }

    response = Response(response=json.dumps(json_string), status=200, mimetype="application/json")
    # Add an 'Access-Control-Allow-Origin' header to the response to allow requests from any origin
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

ip = "localhost:8080" #"0.0.0.0:5000"
ip, port = ip.split(':')

app.run(host=ip, port = int(port[:]), debug = True)
