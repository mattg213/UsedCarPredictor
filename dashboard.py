import dash
from dash import html, dcc, Input, Output, State
from car_deal_analysis import determine_deal

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Car Deal Analyzer"),
    html.Label("Make:"),
    dcc.Input(id='make_name', type='text'),
    html.Label("Model:"),
    dcc.Input(id='model_name', type='text'),
    html.Label("Year:"),
    dcc.Input(id='year', type='number'),
    html.Label("User Price:"),
    dcc.Input(id='user_price', type='number'),
    html.Button('Submit', id='submit-button'),
    html.Button('Reset', id='reset-button'),
    html.Div(id='output')
])

# Combine the callbacks
@app.callback(
    [
        Output('make_name', 'value'),
        Output('model_name', 'value'),
        Output('year', 'value'),
        Output('user_price', 'value'),
        Output('output', 'children')
    ],
    [Input('submit-button', 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [
        State('make_name', 'value'),
        State('model_name', 'value'),
        State('year', 'value'),
        State('user_price', 'value'),
    ],
    prevent_initial_call=True
)
def update_output(submit_n_clicks, reset_n_clicks, make_name, model_name, year, user_price):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'reset-button':
        return '', '', None, None, ''

    if triggered_id == 'submit-button':
        deal = determine_deal(make_name, model_name, year, user_price)
        return make_name, model_name, year, user_price, f"The car is a {deal}"

# Run the app
if __name__ == '__main__':
   app.run_server(debug=True)
