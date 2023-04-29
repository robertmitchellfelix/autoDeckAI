#pip install dash
#pip install dash-bootstrap-components
#pip install openai
#http://127.0.0.1:8050/

import json
import openai
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

def getFlashcards(apiKey, question, temperature):
    if question.lower() == "exit":
        return None

    openai.api_key = apiKey #https://platform.openai.com/account/billing/overview

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a consistent elementary teacher. Please make a formatted text database of ten reading comprehension questions you create based on my input. Your response will use the following JSON format:  [{front: \"question, possible answer 1, possible answer 2, possible answer 3, possible answer 4\", back: \"corect answer\"}, {front:\"..\", back: \"..\"}, ...]"},
            {"role": "user", "content": question}
            ],
        temperature=temperature
        )
    saveToJson(completion.choices[0].message.content)
    return completion.choices[0].message.content

def saveToJson(content):
    data = {"response": content}
    with open("response.json", "a") as jsonFile:
        json.dump(data, jsonFile)
        jsonFile.write("\n")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Auto Deck"),
    dbc.Input(id="apiKey", type="password", placeholder="Enter OpenAI API Key", className="mb-3"),
    dbc.Row([
        dbc.Col(dbc.Checkbox(id="showKeyCheckbox", className="form-check-input"), width="auto"),
        dbc.Col(html.Label("Show API Key", htmlFor="showKeyCheckbox", className="form-check-label"))
    ], className="mb-3"),
    dbc.Textarea(id="questionText", placeholder="Enter Content", className="mb-3"),
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
    html.Div(id="responseDiv")
])

@app.callback(
    Output("responseDiv", "children"),
    Output("enterButton", "children"),
    Input("enterButton", "n_clicks"),
    State("apiKey", "value"),
    State("questionText", "value"),
    State("tempSlider", "value")
)
def askQuestion(nClicks, apiKey, question, temp):
    if nClicks is not None and apiKey:
        response = getFlashcards(apiKey, question, temp)
        return response, "Enter"
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