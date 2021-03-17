from app import app

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import uuid
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


dashapp = dash.Dash(__name__,
                    server=app,
                    url_base_pathname='/fake/',
                    assets_folder='templates')

dashapp.index_string = '''
        {% extends "base.html" %}
        {% import 'bootstrap/wtf.html' as wtf %}
        {% block app_content %}
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        {% endblock app_content %}
'''


dashapp.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div(["Input: ",
              dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output'),

])


@dashapp.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)
