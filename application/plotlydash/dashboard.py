import dash
from dash.dependencies import Input, Output
from dash import html,dcc

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/'
    )

    # Create Dash Layout
    dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H2("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),

    ])

    init_callbacks(dash_app)

    return dash_app.server

def init_callbacks(app):
    @app.callback(
        Output('my-output','children'),
        Input('url','search'))

    def update_output_div(pathname):
        pathname = str(pathname)
        return 'Output: {}'.format(pathname)


