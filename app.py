from logging import exception
from flask import Flask, json , render_template , request , jsonify
import os
from scipy.sparse.data import _data_matrix
import yaml
import joblib
import numpy as np
from src import get_data
from prediction_service import prediction


params_path = "params.yaml"
webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")
app = Flask(__name__, static_folder = static_dir, template_folder=template_dir)

@app.route("/",methods = ['GET','POST'])
def index():

    if request.method == 'POST':

        try:
            if request.form:
                # data = [ i[1][0] for i in dict(request.form).items()]
                data_req = dict(request.form)
                # data = [list(map(float, data))]
                response = prediction.form_response(data_req)
                return render_template("index.html", response=response)
            elif request.json:
                response = prediction.api_response(request.json)
                return jsonify(response) 

        except Exception as err:
            print(err)
            error = str(err)
            print(error)
            return render_template("404.html", error=err)
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000 , debug=True) 

