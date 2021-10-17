import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import pandas as pd




def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/'
    )


    df = pd.read_pickle("DB/dashboard.temp",compression ='zip')
    df_grouped_by_node = df.groupby(["COLLECTTIME","ENODEBID"],as_index = False).sum()
    df_grouped_by_cluster = df[df["ENODEBID"].isin([17911, 17912, 17913])].groupby(["COLLECTTIME"], as_index = False).sum()
    metrics = list(df.columns)[5:]
    node = list(set(df["ENODEBID"].tolist()))
    cell = list(set(df["CELLNAME"].tolist()))
    # Create Dash Layout
    dash_app.layout = html.Div(children=[

    # Line chart for CELL
    html.Div(children=[
        html.Div(children='LINE CHART FOR CELL', style={"color":"white","font-size":"30px","font-weight":"600","padding":"15px 0 0 0 ","text-shadow":"1px 1px 2px black", "text-align": "center"}),
        html.Div(children=[

            # Graph Line chart for CELL by METRICS
            html.Div(children=[

                
                    html.Div(children=[
                    html.Div(children='Line chart for CELL by METRICS', style={"color":"#191970", "font-size":"20px","font-weight":"600","padding":"5px 0 5px 0"}),
                    html.Div(children='''Select mertric:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="metrics_chklst_by_metrics_cellg",
                        options=[{"label": x, "value": x} for x in metrics],
                        # value=metrics[1]
                    ),
                    html.Div(children='''Select nodes:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="node_chklst_by_metrics_cellg",
                        options=[{"label": x, "value": x} for x in node],
                        # value=[node[0]],
                        multi=True
                    ),
                    html.Div(children='''Select cells:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="cell_chklst_by_metrics_cellg",
                        options=[{"label": x, "value": x} for x in cell],
                        # value=[cell[0]],
                        multi=True
                    )
                ]),
                dcc.Graph(id="line_chart_for_cell_by_metrics")
            ],style={"width":"45%", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "background":"white", "display":"inline-block", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"}),


            # Graph Line chart for CELL by OBJECT
            html.Div(children=[
                
                html.Div(children=[
                    html.Div(children='Line chart for CELL by OBJECT', style={"color":"#191970","font-size":"20px","font-weight":"600","padding":"5px 0 5px 0"}),
                    html.Div(children='''Select cell:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="cell_chklst_by_object_cellg",
                        options=[{"label": x, "value": x} for x in cell]
                        # value=cell[0]
                    ),
                    html.Div(children='''Select mertrics:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="metrics_chklst_by_object_cellg",
                        options=[{"label": x, "value": x} for x in metrics],
                        # value=[metrics[0]],
                        multi=True
                    ),  
                ]),
                html.Div(style = {"height":"64px"}),
                dcc.Graph(id="line_chart_for_cell_by_objects")
            ],style={"width":"45%", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)","background":"white","position":"absolute", "display":"inline-block", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"})
        ])
    ], style={"border":"1px grey","background":"#949EBC", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "border-radius":"10px", "margin":"1%"}),



    # Line chart for NODE
    html.Div(children=[
        html.Div(children='Line chart for NODE', style={"color":"white","font-size":"30px","font-weight":"600","padding":"15px 0 0 0 ","text-shadow":"1px 1px 2px black", "text-align": "center"}),
        html.Div(children=[

            # Graph Line chart for NODE by METRICS
            html.Div(children=[

                
                    html.Div(children=[
                    html.Div(children='Line chart for NODE by METRICS', style={"color":"#191970", "font-size":"20px","font-weight":"600","padding":"5px 0 5px 0"}),
                    html.Div(children='''Select mertric:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="metrics_chklst_by_metrics_nodeg",
                        options=[{"label": x, "value": x} for x in metrics],
                        # value=[]
                    ),
                    html.Div(children='''Select nodes:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="node_chklst_by_metrics_nodeg",
                        options=[{"label": x, "value": x} for x in node],
                        value=[],
                        multi=True
                    )
                ]),
                dcc.Graph(id="line_chart_for_node_by_metrics")
            ],style={"width":"45%", "background":"white", "display":"inline-block", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"}),


            # Graph Line chart for NODE by OBJECT
            html.Div(children=[
                
                html.Div(children=[
                    html.Div(children='Line chart for NODE by OBJECT', style={"color":"#191970", "font-size":"20px","font-weight":"600","padding":"5px 0 5px 0"}),
                    html.Div(children='''Select node:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="node_chklst_by_object_nodeg",
                        options=[{"label": x, "value": x} for x in node]
                        # value=cell[0]
                    ),
                    html.Div(children='''Select mertrics:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="metrics_chklst_by_object_nodeg",
                        options=[{"label": x, "value": x} for x in metrics],
                        # value=[metrics[0]],
                        multi=True
                    ),  
                ]),
                dcc.Graph(id="line_chart_for_node_by_objects")
            ],style={"width":"45%","background":"white","position":"absolute", "display":"inline-block", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"})
        ])
    ], style={"border":"1px grey","background":"#949EBC", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "border-radius":"10px", "margin":"1%"}),


    # Line chart for CLUSTER
    html.Div(children=[
        html.Div(children='Line chart for CLUSTER', style={"color":"white","font-size":"30px","font-weight":"600","padding":"15px 0 0 0 ","text-shadow":"1px 1px 2px black", "text-align": "center"}),
        html.Div(children=[

            # Graph Line chart for CLUSTER by METRICS
            html.Div(children=[
                # html.Div(children='Line chart for CLUSTER by OBJECT', style={"color":"#191970", "font-size":"20px","font-weight":"600","padding":"5px 0 5px 0"}),
                html.Div(children='''Select mertrics:''', style={"padding":"5px 0 5px 0"}),
                dcc.Dropdown(
                    id="metrics_chklst_by_metrics_clusterg",
                    options=[{"label": x, "value": x} for x in metrics],
                    multi=True
                    # value=[]
                )
            ]),
            dcc.Graph(id="line_chart_for_cluster_by_metrics")
        ],style={"background":"white", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"})

    ], style={"border":"1px grey","display":"inline-block", "width":"98%","background":"#949EBC", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "border-radius":"10px", "margin":"1%"})

], style={"font-family":"verdana"})


    
    

    @dash_app.callback(
        Output("line_chart_for_cell_by_metrics", "figure"),
        [Input("metrics_chklst_by_metrics_cellg","value"),Input("cell_chklst_by_metrics_cellg","value")])
    def create_graph_by_metrics_cellgr(metric_value,cell_value):
        fig = px.line(df.loc[df['CELLNAME'].isin(list(cell_value))], y=metric_value, x="COLLECTTIME", color="CELLNAME", markers=True)
        fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height = 400
        )
        return fig

    # Function for updating cells list when nodes is choosed
    @dash_app.callback(
        Output("cell_chklst_by_metrics_cellg","options"),
        Output("cell_chklst_by_metrics_cellg","value"),
        [Input("node_chklst_by_metrics_cellg","value")])
    def set_nodes_by_metrics_cellgr(node_value):
        if node_value:
            cell_values_list = [{"label": x, "value": x} for x in set(df.loc[df['ENODEBID'].isin(node_value)]['CELLNAME'])]
            # cell_values_list = list(set(cell_values_list))
            return cell_values_list, [item['value'] for item in cell_values_list]
        else:
            return [{"label": x, "value": x} for x in cell], []

    # Function for creating graph "Line chart for CELL by OBJECT"
    @dash_app.callback(
        Output("line_chart_for_cell_by_objects", "figure"),
        [Input("cell_chklst_by_object_cellg","value"),Input("metrics_chklst_by_object_cellg","value")])
    def create_graph_by_object_cellgr(cell_value, metric_value):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        temp_df = df.loc[df["CELLNAME"] == cell_value]
        if metric_value:
            for item in metric_value:
                fig.add_traces(go.Scatter(y=temp_df[item], x=temp_df["COLLECTTIME"], name=item, mode = "markers+lines"))
        fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height = 400,
        xaxis_title="COLLECTTIME",
        yaxis_title="metric value",
        )       
        return fig

    #--------------------------------------------------------------------------------------------------------

    # Function for creating graph "Line chart for NODE by METRICS"
    @dash_app.callback(
        Output("line_chart_for_node_by_metrics", "figure"),
        [Input("metrics_chklst_by_metrics_nodeg","value"),Input("node_chklst_by_metrics_nodeg","value")])
    def create_graph_by_metrics_nodegr(metric_value,node_value):
        fig = px.line(df_grouped_by_node.loc[df_grouped_by_node['ENODEBID'].isin(list(node_value))], y=metric_value, x="COLLECTTIME", color="ENODEBID", markers=True)
        fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height = 400
        )
        return fig


    # Function for creating graph "Line chart for NODE by OBJECT"
    @dash_app.callback(
        Output("line_chart_for_node_by_objects", "figure"),
        [Input("node_chklst_by_object_nodeg","value"),Input("metrics_chklst_by_object_nodeg","value")])
    def create_graph_by_object_nodegr(node_value, metric_value):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        temp_df = df_grouped_by_node.loc[df_grouped_by_node["ENODEBID"] == node_value]
        if metric_value:
            for item in metric_value:
                fig.add_traces(go.Scatter(y=temp_df[item], x=temp_df["COLLECTTIME"], name=item, mode = "markers+lines")) 
        fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height = 400,
        xaxis_title="COLLECTTIME",
        yaxis_title="metric value",
        )       
        return fig

    #--------------------------------------------------------------------------------------------------------

    # Function for creating graph "Line chart for CLUSTER by METRICS"
    @dash_app.callback(
        Output("line_chart_for_cluster_by_metrics", "figure"),
        [Input("metrics_chklst_by_metrics_clusterg","value")])
    def create_graph_by_metrics_clustergr(metric_value):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        if metric_value:
            for item in metric_value:
                fig.add_traces(go.Scatter(y=df_grouped_by_cluster[item], x=df_grouped_by_cluster["COLLECTTIME"], name=item, mode = "markers+lines")) 
        fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height = 400,
        xaxis_title="COLLECTTIME",
        yaxis_title="metric value",
        )       
        return fig

    #--------------------------------------------------------------------------------------------------------
    return dash_app.server
