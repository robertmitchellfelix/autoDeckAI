#pip install dash
#pip install dash-bootstrap-components
#pip install openai
#http://127.0.0.1:8050/

import json
import openai
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

def getFlashcards(apiKey, question, temperature, filename):
    openai.api_key = apiKey

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a consistent elementary teacher. Please make a formatted text database of ten reading comprehension questions you create based on my input. Your response will use the following JSON format:  [{front: \"question, possible answer 1, possible answer 2, possible answer 3, possible answer 4\", back: \"corect answer\"}, {front:\"..\", back: \"..\"}, ...]"},
            {"role": "user", "content": question}
            ],
        temperature=temperature
        )
    saveToJson(completion.choices[0].message.content, filename)
    return completion.choices[0].message.content

def saveToJson(content, filename):
    data = {"response": content}
    with open(f"{filename}.json", "a") as jsonFile:
        json.dump(data, jsonFile)
        jsonFile.write("\n")

def translate(apiKey, content, temperature, filename):
    openai.api_key = apiKey

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a consistent elementary teacher fluent in Sonoran Spanish.  Please translate the following questions and answers to Sonoran Spanish.  Always retain the original formatting."},
            {"role": "user", "content": content}
            ],
        temperature=temperature
        )
    saveToJsonSpanish(completion.choices[0].message.content, filename)
    return completion.choices[0].message.content

def saveToJsonSpanish(content, filename):
    data = {"response": content}
    with open(f"{filename}_Spanish.json", "a") as jsonFile:
        json.dump(data, jsonFile)
        jsonFile.write("\n")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Auto Deck"),
    
    dbc.Input(
        id="apiKey", 
        type="password", 
        placeholder="Enter OpenAI API Key", 
        className="mb-3"
    ),

    dbc.Row([
        dbc.Col(dbc.Checkbox(id="showKeyCheckbox", className="form-check-input"), width="auto"),
        dbc.Col(html.Label("Show API Key", htmlFor="showKeyCheckbox", className="form-check-label")),
    ], className="mb-3"),

    dbc.Input(
        id="jsonFilename", 
        type="text", 
        placeholder="Enter JSON filename", 
        className="mb-3"
    ),

    dbc.Textarea(
        id="questionText", 
        placeholder="Enter Content", 
        className="mb-3"
    ),

    dbc.Row([
        dbc.Col(dbc.Checkbox(id="translateCheckbox", className="form-check-input"), width="auto"),
        dbc.Col(html.Label("Translate", htmlFor="translateCheckbox", className="form-check-label")),
    ], className="mb-3"),

    dcc.Slider(
        id='tempSlider',
        min=0,
        max=1,
        step=0.1,
        value=0.5,
        marks={i/10: str(i/10) for i in range(0, 11)},
        className="mb-3"
    ),

    html.Div(id='sliderOutput', className="mb-3"),

    dbc.Button("Enter", id="enterButton", color="primary", className="mb-3"),

    html.Div(id="responseDiv"),
])

@app.callback(
    Output("responseDiv", "children"),
    Output("enterButton", "children"),
    Input("enterButton", "n_clicks"),
    State("apiKey", "value"),
    State("questionText", "value"),
    State("tempSlider", "value"),
    State("jsonFilename", "value"),
    State("translateCheckbox", "value")
)
def askQuestion(nClicks, apiKey, question, temp, filename, translateChecked):
    if nClicks is not None and apiKey and filename and question:
        response = getFlashcards(apiKey, question, temp, filename)
        output = [html.P(response)]
        if translateChecked:
            translated_response = translate(apiKey, response, temp, filename)
            output.append(html.P(translated_response))
        return output, "Enter"
    return dash.no_update, "Enter"

@app.callback(
    Output("apiKey", "type"),
    Input("showKeyCheckbox", "value")
)
def toggleAPIKeyVisibility(checked):
    return "text" if checked else "password"

@app.callback(
    Output("sliderOutput", "children"),
    Input("tempSlider", "value")
)
def updateSliderOutput(value):
    return f"Creativity: {value}"

if __name__ == "__main__":
    app.run_server(debug=True)
