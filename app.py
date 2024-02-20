from flask import Flask, render_template, request
import json, time, requests
import google.generativeai as palm

app = Flask(__name__)

img_headers = {'Authorization': 'Token r8_Sy3eeM9zV2mfXYAh0eKT2h2206nKdaU0VTTH4', 'Content-Type': 'application/json'}
palm.configure(api_key = "AIzaSyBHiTJ-IFy9RJPlwLE13FgpuncRZ7tQG6M")
model = { "model" : "models/chat-bison-001"}

@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        if "question_text" in request.form:
            question_text = request.form.get("question_text")
            response = palm.chat(
                **model,
                messages=question_text
                ) 
            return(render_template("index.html",response_text=response.last))
        elif "question_image" in request.form:
            question_image = request.form.get("question_image")
            body = json.dumps(
                {"version": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                "input": { "prompt": question_image }}
            )
            output = requests.post('https://api.replicate.com/v1/predictions',data=body,headers=img_headers)
            time.sleep(10)
            get_url = output.json()['urls']['get']
            get_result = requests.get(get_url,headers=img_headers).json()['output']       
            return(render_template("index.html",image_text=get_result[0]))   
    else:
        return(render_template("index.html",result="waiting..........."))

if __name__ == "__main__":
    app.run()