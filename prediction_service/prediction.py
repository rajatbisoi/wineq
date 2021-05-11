import yaml
import os
import json
import joblib
import numpy as np

params_path = "params.yaml"
schema_path = os.path.join("prediction_service","schema_in.json")

class NotInRange(Exception):
    def __init__(self,message="values entered are not in range"):
        self.message = message
        super().__init__(self.message)
        
class NotInCols(Exception):
    def __init__(self,message="not in columns"):
        self.message = message
        super().__init__(self.message)
def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
        return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction  = model.predict(data).tolist()[0]

    try:
        if 3 <= prediction <= 8:
            return prediction
        else:
            raise NotInRange
    except NotInRange:
        return "Unexpected result"

def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def validate_input(dict_request):
    def _validate_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInCols

    def _validate_values(col, val):
        try:    
            schema = get_schema()
            print(*dict_request[col])
            if not (schema[col]["min"] <= float(*dict_request[col]) <= schema[col]["max"]):
                raise NotInRange
        except Exception as err:
            print(err,*dict_request[col])

    for col,val in dict_request.items():
        _validate_cols(col)
        _validate_values(col,val)
    return True

def form_response(dict_request):
    if validate_input(dict_request):
        # data = dict_request.values()
        data = np.array([ i[1][0] for i in dict(dict_request).items()]).reshape(1,-1)
        # print(data)
        # data = [list(map(float,data))]
        response = predict(data)
        return response

def api_response(dict_request):
    try:
        if validate_input(dict_request):
            data = np.array([ i[1][0] for i in dict(dict_request).items()]).reshape(1,-1)
            # data = np.array([list(dict_request.values())])
            print(data.shape)
            print(data)
            response = predict(data)
            response = {"response": response}
            return response
    except NotInRange as err:
        response = {"the_except_range": get_schema(),"response":str(err)}
        return response

    except NotInCols as err:
        response = {"the_except_columns": get_schema().keys(),"response":str(err)}
        return response