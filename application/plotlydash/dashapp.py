import dash_core_components as dcc

import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
from dash_extensions.enrich import DashProxy, ServersideOutput, ServersideOutputTransform,Dash
import pandas as pd
import numpy as np
from datetime import *



def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    app = Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )

    def metrics_from_file(instructions_file):
        with open(instructions_file,'rt') as f:
            formulas = [formulas_temp.strip() for formulas_temp in f.readlines() if not formulas_temp.isspace()] # checking for empty lines
        metrica_dic = {}
        for formula in formulas:
            metrica = formula[:formula.find('=')].strip() # formula name (before first '=' )
            expression = formula[formula.find('=') + 1:] # formula expression (after first '=' )
            metrica_dic[metrica] = expression.strip()
        return metrica_dic

    # app = dash.Dash(__name__)
    # df = pd.read_csv("LTE2.csv", parse_dates=["COLLECTTIME"])
    # df_grouped_by_node = df.groupby(["COLLECTTIME","ENODEBID"],as_index = False).sum()
    # df_grouped_by_cluster = df[df["ENODEBID"].isin([17911, 17912, 17913])].groupby(["COLLECTTIME"], as_index = False).sum()
    # metrics = ['Call_Completion']
    # node = list(set(df["ENODEBID"].tolist()))
    # cell = list(set(df["CELLNAME"].tolist()))
    #----------------------------------------SETTINGS BLOCK---------------------------------------------
    # Function that upload pickle and keynames when reload
    @app.callback(ServersideOutput('main_df_store', 'data'),
        ServersideOutput('keynames_store', 'data'),
        Output('settings_datarange', 'start_date'), Output('settings_datarange', 'end_date'),
        Output('interval_1_timeov', 'start_date'), Output('interval_1_timeov', 'end_date'),
        Output('interval_2_timeov', 'start_date'), Output('interval_2_timeov', 'end_date'),
        [Input('onload', 'children')])
    def get_input_pickle(some_input):
        path='DB/dashboard.temp'
        df = pd.read_pickle(path, compression = 'zip')
        start_date = str(df[df.attrs['data_time_field_name']].min()).split()[0].split('-')
        end_date = str(df[df.attrs['data_time_field_name']].max()).split()[0].split('-')

        keys_names = {'zte_type': df.attrs['zte_type'],'data_time_field_name': df.attrs['data_time_field_name'],
        'node_name': df.attrs['node_name'],'cell_name': df.attrs['cell_name'],
        'metrics_names': list(metrics_from_file('ZTE/' + df.attrs['zte_type'] + '/requirements/' + 'formula.txt').keys()),'metrics_formulas': metrics_from_file('ZTE/' + df.attrs['zte_type'] + '/requirements/' + 'formula.txt'),
        'primary_keys': df.attrs['primary_keys'],'counters': df.attrs['counters'],}
        # date(start_date[0], start_date[1], start_date[2])
        return df, keys_names, date(int(start_date[0]), int(start_date[1]), int(start_date[2])), date(int(end_date[0]), int(end_date[1]), int(end_date[2])), date(int(start_date[0]), int(start_date[1]), int(start_date[2])), date(int(end_date[0]), int(end_date[1]), int(end_date[2])), date(int(start_date[0]), int(start_date[1]), int(start_date[2])), date(int(end_date[0]), int(end_date[1]), int(end_date[2]))


    # Function that save settings values to store
    @app.callback(Output('settings_values_store', 'data'),[Input('settings_datarange', 'start_date'),
     Input('settings_datarange', 'end_date'),Input('settings_cluster', 'value'), Input('settings_timetype', 'value')])
    def save_settings_values(start_date, end_date, cluster_value, timegroup_type):
        return {'start_date': start_date, 'end_date' : end_date, "cluster_value": cluster_value, "timegroup_type": timegroup_type}



    # Function for change df by settings
    @app.callback(ServersideOutput('processed_df_store', 'data'),
        Input('main_df_store', 'data'),Input('keynames_store', 'data'),
        Input('submit_settings_btn', 'n_clicks'),State('settings_values_store', 'data'))
    def dataframe_settings(input_df, keys_dict, btn_action, settings_dict):
        if not btn_action is None :
            df = interval_aggregation(input_df, keys_dict['data_time_field_name'], settings_dict['start_date'], settings_dict['end_date'])
            df = time_aggregation(df, keys_dict['primary_keys'], keys_dict['data_time_field_name'], settings_dict['timegroup_type'], keys_dict['metrics_names'], keys_dict['counters'])
            if settings_dict['cluster_value']:
                f = open('ZTE/' + keys_dict['zte_type'] + '/requirements/cluster.txt', 'r')
                print(f)
                cluster_file = [nodes_temp.strip() for nodes_temp in f.readlines() if not nodes_temp.isspace()]
                f.close()
                df = claster_aggregation(df, settings_dict['cluster_value'][0], cluster_file[0], cluster_file[1:])
            return df


    # Function for creating Cell dataframe
    @app.callback(ServersideOutput('processed_df_store_cell', 'data'), Input('processed_df_store', 'data'), State('keynames_store', 'data'))
    def create_cell_df(df, keys_dict):
        try:
            processed_cell_df = count_metrics(df, keys_dict, keys_dict['counters'])
            return processed_cell_df.sort_values(keys_dict['data_time_field_name'])
        except: pass



    # Function for creating Node dataframe
    @app.callback(ServersideOutput('processed_df_store_node', 'data'), Input('processed_df_store', 'data'), State('keynames_store', 'data'))
    def create_node_df(df, keys_dict):
        try:
            node_df = node_aggregation(df, keys_dict['data_time_field_name'], keys_dict['node_name'], keys_dict['counters'])
            processed_node_df = count_metrics(node_df, keys_dict, keys_dict['counters'])
            return processed_node_df.sort_values(keys_dict['data_time_field_name'])
        except: pass

    #---------------------------------------AGREGATION BLOCK----------------------------------------------

    def interval_aggregation(input_df, data_time_field_name, start_date, end_date):
        # return input_df[(input_df[data_time_field_name] >= start_date) & (input_df[data_time_field_name] < end_date)]
        return input_df[(input_df[data_time_field_name] >= start_date) & (input_df[data_time_field_name]-timedelta(days=1) < end_date)]

    def remove_collecttime_from_primary_keys(primary_keys,data_time_field_name):
        copy_list = primary_keys[:]
        copy_list.remove(data_time_field_name)
        return copy_list

    def time_aggregation(df,primary_keys,data_time_field_name,frequency,metrics,counters):
        if not frequency == 'Hour':
            cutted_primary_keys = remove_collecttime_from_primary_keys(primary_keys,data_time_field_name)
            df = df.groupby([pd.Grouper(key = data_time_field_name, freq = 'D')] + cutted_primary_keys).sum()
            df.reset_index(inplace = True)
            return df
        return df

    def claster_aggregation(df,claster_check,claster_name,claster_values):
        if claster_check == 'only_cluster':
            return df[df[claster_name].astype(str).isin(claster_values)]
        return df

    def node_aggregation(df, data_time_field_name, node_name, counters):
        df_fields = [data_time_field_name,node_name] + counters
        return df.groupby([data_time_field_name,node_name],as_index = False).sum()[df_fields]


    def count_metrics(df, keys_dict, counters):
        metrics_formulas = metrics_from_file('ZTE/' + keys_dict['zte_type'] + '/requirements/' + 'formula.txt')
        df_columns = df.columns.tolist()
        primary_keys = [key for key in df_columns if key not in counters]

        for key,value in metrics_formulas.items():
            df[key] = np.around(df.eval(value),2)
        final_table = df[primary_keys + list(metrics_formulas.keys())]
        return final_table


# ----------------------------------------------------------------------------------
    #-----------------------------------------Line chart for CELL------------------------------------------

    # Function for creating graph "Line chart for CELL by METRICS"
    @app.callback(
        Output("line_chart_for_cell_by_metrics", "figure"),
        [Input("metrics_chklst_by_metrics_cellg","value"),Input("cell_chklst_by_metrics_cellg","value"), Input('processed_df_store_cell', 'data'), State('keynames_store', 'data')])
    def create_graph_by_metrics_cellgr(metric_value,cell_value, df, keys_dict):
        if not df is None:
            fig = px.line(df.loc[df[keys_dict['cell_name']].isin(list(cell_value))], y=metric_value, x=keys_dict['data_time_field_name'], color=keys_dict['cell_name'], markers=True)
            fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height = 400
            )
            return fig
        else: return {}

    # Function for updating cells list when nodes is choosed
    @app.callback(
        Output("cell_chklst_by_metrics_cellg","options"),
        Output("cell_chklst_by_metrics_cellg","value"),
        [Input("node_chklst_by_metrics_cellg","value"), Input('processed_df_store_cell', 'data'), State('keynames_store', 'data')])
    def set_nodes_by_metrics_cellgr(node_value, df, keys_dict):
        if not df is None:
            if node_value:
                cell_values_list = [{"label": x, "value": x} for x in set(df.loc[df[keys_dict['node_name']].isin(node_value)][keys_dict['cell_name']])]
                return cell_values_list, [item['value'] for item in cell_values_list]
            else:
                return [{"label": x, "value": x} for x in sorted(list(set(df[keys_dict['cell_name']].tolist())))], []
        else:
            return [], []

    # Function for creating graph "Line chart for CELL by OBJECT"
    @app.callback(
        Output("line_chart_for_cell_by_objects", "figure"),
        [Input("cell_chklst_by_object_cellg","value"),Input("metrics_chklst_by_object_cellg","value"), Input('processed_df_store_cell', 'data'), State('keynames_store', 'data')])
    def create_graph_by_object_cellgr(cell_value, metric_value, df, keys_dict):
        if not df is None:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            temp_df = df.loc[df[keys_dict['cell_name']] == cell_value]
            if metric_value:
                for item in metric_value:
                    fig.add_traces(go.Scatter(y=temp_df[item], x=temp_df[keys_dict['data_time_field_name']], name=item, mode = "markers+lines"))
            fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height = 400,
            xaxis_title="COLLECTTIME",
            yaxis_title="metric value",
            )       
            return fig
        else: return {}

    # Options block
    @app.callback(Output("node_chklst_by_metrics_cellg", 'options'), Output("cell_chklst_by_object_cellg", 'options'),
        [Input('keynames_store', 'data'), Input('processed_df_store_cell', 'data')])
    def get_options_cellg(keys_dict, df):
        if not df is None:
            return [{"label": x, "value": x} for x in sorted(list(set(df[keys_dict['node_name']].tolist())))], [{"label": x, "value": x} for x in sorted(list(set(df[keys_dict['cell_name']].tolist())))]
        else: return [], []
    @app.callback(Output("metrics_chklst_by_object_cellg","options"),Output("metrics_chklst_by_metrics_cellg","options"),
        Input('keynames_store', 'data'))
    def get_metrics_cellg(keys_dict):
        return [{"label": x, "value": x} for x in keys_dict['metrics_names']], [{"label": x, "value": x} for x in keys_dict['metrics_names']]


    #-----------------------------------------Line chart for NODE------------------------------------------

    # Function for creating graph "Line chart for NODE by METRICS"
    @app.callback(
        Output("line_chart_for_node_by_metrics", "figure"),
        [Input("metrics_chklst_by_metrics_nodeg","value"),Input("node_chklst_by_metrics_nodeg","value"),
        Input('keynames_store', 'data'), Input('processed_df_store_node', 'data')])
    def create_graph_by_metrics_nodegr(metric_value,node_value, keys_dict, df):
        if not df is None:
            fig = px.line(df.loc[df[keys_dict['node_name']].isin(list(node_value))], y=metric_value, x=keys_dict['data_time_field_name'], color=keys_dict['node_name'], markers=True)
            fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height = 400
            )
            return fig
        else: return {}


    # Function for creating graph "Line chart for NODE by OBJECT"
    @app.callback(
        Output("line_chart_for_node_by_objects", "figure"),
        [Input("node_chklst_by_object_nodeg","value"),Input("metrics_chklst_by_object_nodeg","value"),
        Input('keynames_store', 'data'), Input('processed_df_store_node', 'data')])
    def create_graph_by_object_nodegr(node_value, metric_value, keys_dict, df):
        if not df is None:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            temp_df = df.loc[df[keys_dict['node_name']] == node_value]
            if metric_value:
                for item in metric_value:
                    fig.add_traces(go.Scatter(y=temp_df[item], x=temp_df[keys_dict['data_time_field_name']], name=item, mode = "markers+lines")) 
            fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height = 400,
            xaxis_title="COLLECTTIME",
            yaxis_title="metric value",
            )       
            return fig
        else: return {}

    @app.callback(Output("metrics_chklst_by_object_nodeg","options"),Output("metrics_chklst_by_metrics_nodeg","options"),
        Input('keynames_store', 'data'))
    def get_metrics_nodeg(keys_dict):
        return [{"label": x, "value": x} for x in keys_dict['metrics_names']], [{"label": x, "value": x} for x in keys_dict['metrics_names']]


    @app.callback(Output("node_chklst_by_metrics_nodeg", 'options'), Output("node_chklst_by_object_nodeg", 'options'),
        [Input('keynames_store', 'data'), Input('processed_df_store_node', 'data')])
    def get_options_nodeg(keys_dict, df):
        if not df is None:
            return [{"label": x, "value": x} for x in sorted(list(set(df[keys_dict['node_name']].tolist())))], [{"label": x, "value": x} for x in sorted(list(set(df[keys_dict['node_name']].tolist())))]  
        else: return [], []
    #--------------------------------------Line chart for CLUSTER---------------------------------------------

    # Function for creating graph "Line chart for CLUSTER by METRICS"
    @app.callback(
        Output("line_chart_for_cluster_by_metrics", "figure"),
        [Input("metrics_chklst_by_metrics_clusterg","value"), Input('keynames_store', 'data'), Input('processed_df_store_node', 'data')])
    def create_graph_by_metrics_clustergr(metric_value, keys_dict, df):
        if not df is None:
            df_grouped_by_cluster = df.groupby([keys_dict['data_time_field_name']], as_index = False).sum()
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            if metric_value:
                for item in metric_value:
                    fig.add_traces(go.Scatter(y=df_grouped_by_cluster[item], x=df_grouped_by_cluster[keys_dict['data_time_field_name']], name=item, mode = "markers+lines")) 
            fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height = 400,
            xaxis_title="COLLECTTIME",
            yaxis_title="metric value",
            )       
            return fig
        else: return {}

    @app.callback(Output("metrics_chklst_by_metrics_clusterg","options"),
        Input('keynames_store', 'data'))
    def get_metrics_clusterg(keys_dict):
        return [{"label": x, "value": x} for x in keys_dict['metrics_names']]
    #----------------------------------------Line for TIME OVERLAY-------------------------------------------

    # Function for updating object list in TIME OVERLAY
    @app.callback(
        Output("object_chklst_timeov", "options"),
        [Input("object_type_chklst_timeov","value"), Input('keynames_store', 'data'), Input('processed_df_store_cell', 'data')])
    def update_object_list_timeov(object_type, keys_dict, df):
        if not object_type is None:
            if object_type == "Cell":
                return [{"label": x, "value": x} for x in sorted(list(set(df[keys_dict['cell_name']].tolist())))]
            elif object_type == "Node":
                return [{"label": x, "value": x} for x in sorted(list(set(df[keys_dict['node_name']].tolist())))]
            elif object_type == 'Cluster':
                return [{"label": 'Cluster', "value": 'cluster'}]
        else: return []

    # Function for updating metrics list in TIME OVERLAY
    @app.callback(Output("metrics_chklst_timeov","options"),
        Input('keynames_store', 'data'))
    def get_metrics_timeoverl(keys_dict):
        return [{"label": x, "value": x} for x in keys_dict['metrics_names']]

    # Function for creating graph list in TIME OVERLAY
    @app.callback(Output('time_overlay_graph', 'figure'),
        [Input('submit_timeov_btn', 'n_clicks'),
        State('interval_1_timeov', 'start_date'), State('interval_1_timeov', 'end_date'),
        State('interval_2_timeov', 'start_date'), State('interval_2_timeov', 'end_date'),
        State('object_type_chklst_timeov', 'value'), State('object_chklst_timeov', 'value'),
        State('metrics_chklst_timeov', 'value'), State('keynames_store', 'data'),
        State('processed_df_store_cell', 'data'), State('processed_df_store_node', 'data')])
    def create_graph_time_overlay(n_clicks, int1_start, int1_end, int2_start, int2_end, object_type, selected_object, selected_metric, keys_dict, cell_df, node_df):
        if not n_clicks is None:
            if object_type == 'Cell':
                df1 = interval_aggregation(cell_df, keys_dict['data_time_field_name'], int1_start, int1_end)
                df2 = interval_aggregation(cell_df, keys_dict['data_time_field_name'], int2_start, int2_end)
                df1 = df1.loc[df1[keys_dict['cell_name']] == selected_object]
                df2 = df2.loc[df2[keys_dict['cell_name']] == selected_object]

            if object_type == 'Node':
                df1 = interval_aggregation(node_df, keys_dict['data_time_field_name'], int1_start, int1_end)
                df2 = interval_aggregation(node_df, keys_dict['data_time_field_name'], int2_start, int2_end)
                df1 = df1.loc[df1[keys_dict['node_name']] == selected_object]
                df2 = df2.loc[df2[keys_dict['node_name']] == selected_object]

            if object_type == 'Cluster':
                cluster_df = cell_df.groupby([keys_dict['data_time_field_name']], as_index = False).sum()
                df1 = interval_aggregation(cluster_df, keys_dict['data_time_field_name'], int1_start, int1_end)
                df2 = interval_aggregation(cluster_df, keys_dict['data_time_field_name'], int2_start, int2_end)

            df1['day_numeration'] = range(1, len(df1)+1)
            df2['day_numeration'] = range(1, len(df2)+1)
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_traces(go.Scatter(y=df1[selected_metric], x=df1['day_numeration'], name='1 interval', text = df1[keys_dict['data_time_field_name']],  hovertemplate = '<br><b>Date</b> %{text}' + '<br><b>Value</b> %{y}',mode = "markers+lines"))
            fig.add_traces(go.Scatter(y=df2[selected_metric], x=df2['day_numeration'], name='2 interval', text = df2[keys_dict['data_time_field_name']],  hovertemplate = '<br><b>Date</b> %{text}' + '<br><b>Value</b> %{y}', mode = "markers+lines"))
            fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height = 400,
            xaxis_title="COLLECTTIME",
            yaxis_title="metric value",
            hovermode='x unified')
            return fig
        else: return {}


    #----------------------------------------Line for BOLLINGER LINES-------------------------------------------

    # Function for updating metrics list in BOLLINGER LINES
    @app.callback(Output("metrics_chklst_bollinger","options"),
        Input('keynames_store', 'data'))
    def get_metrics_bollinger(keys_dict):
        return [{"label": x, "value": x} for x in keys_dict['metrics_names']]


    # Function for updating object list in BOLLINGER LINES
    @app.callback(
        Output("object_chklst_bollinger", "options"),
        [Input("object_type_chklst_bollinger","value"), Input('keynames_store', 'data'), Input('processed_df_store_cell', 'data')])
    def update_object_list_bollinger(object_type, keys_dict, df):
        if not object_type is None:
            if object_type == "Cell":
                return [{"label": x, "value": x} for x in sorted(list(set(df[keys_dict['cell_name']].tolist())))]
            elif object_type == "Node":
                return [{"label": x, "value": x} for x in sorted(list(set(df[keys_dict['node_name']].tolist())))]
            elif object_type == 'Cluster':
                return [{"label": 'Cluster', "value": 'cluster'}]
        else: return []


    # Function for creating graph for BOLLINGER LINES
    @app.callback(Output('bollinger_graph', 'figure'),
        [Input('object_type_chklst_bollinger', 'value'), Input('object_chklst_bollinger', 'value'),
        Input('metrics_chklst_bollinger', 'value'), Input('keynames_store', 'data'),
        Input('processed_df_store_cell', 'data'), Input('processed_df_store_node', 'data')])
    def create_graph_bollinger(object_type, selected_object, selected_metric, keys_dict, cell_df, node_df):
        if not selected_object is None and not selected_metric is None:
            if object_type == 'Cell':
                df = cell_df.loc[cell_df[keys_dict['cell_name']] == selected_object]
            if object_type == 'Node':
                df = node_df.loc[node_df[keys_dict['node_name']] == selected_object]
            if object_type == 'Cluster':
                df = cell_df.groupby([keys_dict['data_time_field_name']], as_index = False).sum()
            print(df)

            window = 7
            no_of_std = 2
            rolling_mean = df[selected_metric].rolling(window).mean()
            rolling_std = df[selected_metric].rolling(window).std()
            df['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
            df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)
            print(df)
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_traces(go.Scatter(y=df[selected_metric], x=df[keys_dict['data_time_field_name']], name= selected_metric, mode = "markers+lines"))
            fig.add_traces(go.Scatter(y=df['Bollinger High'], x=df[keys_dict['data_time_field_name']], name= 'Bollinger High', mode = "markers+lines"))
            fig.add_traces(go.Scatter(y=df['Bollinger Low'], x=df[keys_dict['data_time_field_name']], name= 'Bollinger Low', mode = "markers+lines"))
            fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height = 400,
            xaxis_title="COLLECTTIME",
            yaxis_title="metric value",
            hovermode='x unified')
            return fig
        else: return {}

    #-----------------------------------------LAYOUT--------------------------------------------------------
    app.layout = html.Div(children=[

        dcc.ConfirmDialog(
            id='alert'
        ),

        dcc.Store(id='main_df_store'),
        dcc.Store(id='keynames_store'),
        dcc.Store(id='settings_values_store'),
        dcc.Store(id='processed_df_store'),
        dcc.Store(id='processed_df_store_cell'),
        dcc.Store(id='processed_df_store_node'),

        # Hidden Div
        html.Div(id='onload', style={'display':'none'}),

    # Settings--------------------------------------------------------
        html.Div(children=[
            html.Div(children='Settings', style={"color":"white","font-size":"30px","font-weight":"600","padding":"15px 0 0 0 ","text-shadow":"1px 1px 2px black", "text-align": "center"}),
            
            html.Div(children=[
                html.Div(children='Select date range', style={"display":"inline-block", "color":"white", "font-size":"20px","font-weight":"600","padding":"5px 0 5px 20px","text-shadow":"1px 1px 2px black"}),
                dcc.DatePickerRange(
                    id='settings_datarange',
                    calendar_orientation='vertical',
                    display_format='DD/MM/YYYY',
                    start_date = date(2021, 8, 10),
                    style={"display":"inline-block", "padding":"0 0 0 20px"},
                ), 
            ], style={"padding":"5px 10px 20px 20px", "display":"inline-block"}),

            html.Div(children=[
                html.Div(children='Use cluster', style={"display":"inline-block", "color":"white", "font-size":"20px","font-weight":"600","padding":"5px 0 5px 50px","text-shadow":"1px 1px 2px black"}),
                dcc.Checklist(
                    id='settings_cluster',
                    options=[{'label':'', 'value':'only_cluster'}],
                    style={"display":"inline-block", "padding":"0 0 0 20px", 'width':'20px'},
                ), 
            ], style={"padding":"5px 10px 20px 20px", "display":"inline-block"}),

            html.Div(children=[
                html.Div(children='Select time grouping type', style={"display":"inline-block", "color":"white", "font-size":"20px","font-weight":"600","padding":"5px 20px 5px 50px","text-shadow":"1px 1px 2px black"}),
                html.Div(children=[dcc.Dropdown(
                    id='settings_timetype',
                    options=[{"label": x, "value": x} for x in ['Hour', 'Day']],
                    value='Day',
                    style={'width':'140px'},
                )], style={'display':'inline-block', 'float':'right'}), 
            ], style={"padding":"5px 40px 20px 20px", "display":"inline-block"}),

            dbc.Button('Submit', id='submit_settings_btn', style={"display":"inline-block", 'background-color': 'white', 'height': '40px', 'width': '100px', "border-radius":"10px"}),


        ], style={"border":"1px grey","background":"#949EBC", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "border-radius":"10px", "margin":"1%"}),

    # Line chart for CELL-----------------------------------------------
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
                            # value=metrics[1]
                        ),
                        html.Div(children='''Select nodes:''', style={"padding":"5px 0 5px 0"}),
                        dcc.Dropdown(
                            id="node_chklst_by_metrics_cellg",
                            # value=[node[0]],
                            multi=True
                        ),
                        html.Div(children='''Select cells:''', style={"padding":"5px 0 5px 0"}),
                        dcc.Dropdown(
                            id="cell_chklst_by_metrics_cellg",
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
                            # value=cell[0]
                        ),
                        html.Div(children='''Select mertrics:''', style={"padding":"5px 0 5px 0"}),
                        dcc.Dropdown(
                            id="metrics_chklst_by_object_cellg",
                            # value=[metrics[0]],
                            multi=True
                        ),  
                    ]),
                    html.Div(style = {"height":"64px"}),
                    dcc.Graph(id="line_chart_for_cell_by_objects")
                ],style={"width":"45%", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)","background":"white","position":"absolute", "display":"inline-block", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"})
            ])
        ], style={"border":"1px grey","background":"#949EBC", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "border-radius":"10px", "margin":"1%"}),



    # Line chart for NODE-----------------------------------------------
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
                            # value=[]
                        ),
                        html.Div(children='''Select nodes:''', style={"padding":"5px 0 5px 0"}),
                        dcc.Dropdown(
                            id="node_chklst_by_metrics_nodeg",
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
                            # value=cell[0]
                        ),
                        html.Div(children='''Select mertrics:''', style={"padding":"5px 0 5px 0"}),
                        dcc.Dropdown(
                            id="metrics_chklst_by_object_nodeg",
                            # value=[metrics[0]],
                            multi=True
                        ),  
                    ]),
                    dcc.Graph(id="line_chart_for_node_by_objects")
                ],style={"width":"45%","background":"white","position":"absolute", "display":"inline-block", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"})
            ])
        ], style={"border":"1px grey","background":"#949EBC", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "border-radius":"10px", "margin":"1%"}),


    # Line chart for CLUSTER-----------------------------------------------
        html.Div(children=[
            html.Div(children='Line chart for CLUSTER', style={"color":"white","font-size":"30px","font-weight":"600","padding":"15px 0 0 0 ","text-shadow":"1px 1px 2px black", "text-align": "center"}),
            html.Div(children=[

                # Graph Line chart for CLUSTER by METRICS
                html.Div(children=[
                    # html.Div(children='Line chart for CLUSTER by OBJECT', style={"color":"#191970", "font-size":"20px","font-weight":"600","padding":"5px 0 5px 0"}),
                    html.Div(children='''Select mertrics:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="metrics_chklst_by_metrics_clusterg",
                        multi=True
                        # value=[]
                    )
                ]),
                dcc.Graph(id="line_chart_for_cluster_by_metrics"),
                html.Div(children=[
                    html.Div(children='''Time grouping:''', style={"padding":"5px 10px 5px 0", "display":"inline-block"}),
                    dcc.Checklist(
                        id="time_chklst_timeov",
                        options=[{"label": x, "value": x} for x in ['Hour', 'Day']],
                        labelStyle = {"display":"inline-block", "padding":"0 5px 0 0"},
                        style = {"display":"inline-block"}
                    )
                ], style={"display":"block"}),
            ],style={"background":"white", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"})

        ], style={"border":"1px grey","display":"inline-block", "width":"98%","background":"#949EBC", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "border-radius":"10px", "margin":"1%"}),

    # Line chart for TIME OVERLAY-----------------------------------------------
        html.Div(children=[
            html.Div(children='Line chart for TIME OVERLAY', style={"color":"white","font-size":"30px","font-weight":"600","padding":"15px 0 0 0 ","text-shadow":"1px 1px 2px black", "text-align": "center"}),
            html.Div(children=[

                # Graph Line chart for TIME OVERLAY
                html.Div(children=[
                    html.Div(children='''Select time intervals:''', style={"padding":"5px 0 5px 0"}),

                    dcc.DatePickerRange(
                        id='interval_1_timeov',
                        calendar_orientation='vertical',
                        display_format='DD/MM/YYYY',
                        style={"display":"inline-block", "padding":"0 0 0 0px"},
                    ), 
                    dcc.DatePickerRange(
                        id='interval_2_timeov',
                        calendar_orientation='vertical',
                        display_format='DD/MM/YYYY',
                        style={"display":"inline-block", "padding":"0 40px 0 40px"},
                    ),
                    dbc.Button('Submit', outline=True, color="#D8BFD8", id='submit_timeov_btn',className="me-1", style={"display":"inline-block", 'background-color': '#D8BFD8', 'height': '40px', 'width': '100px', "border-radius":"10px"}),
                ]), 
                html.Div(children=[
                    html.Div(children='''Select object type:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="object_type_chklst_timeov",
                        options=[{"label": x, "value": x} for x in ['Node', 'Cell', 'Cluster']],
                    )
                ]),
                html.Div(children=[
                    html.Div(children='''Select object:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="object_chklst_timeov",
                    )
                ]),
                html.Div(children=[
                    html.Div(children='''Select mertrics:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="metrics_chklst_timeov",
                    )
                ]),
                
                dcc.Graph(id="time_overlay_graph")
            ],style={"background":"white", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"})

        ], style={"border":"1px grey","display":"inline-block", "width":"98%","background":"#D8BFD8", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "border-radius":"10px", "margin":"1%"}),

    # Line chart for TIME OVERLAY-----------------------------------------------
        html.Div(children=[
            html.Div(children='Line chart for BOLLINGER LINES', style={"color":"white","font-size":"30px","font-weight":"600","padding":"15px 0 0 0 ","text-shadow":"1px 1px 2px black", "text-align": "center"}),      
            html.Div(children=[
                html.Div(children=[
                    html.Div(children='''Select object type:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="object_type_chklst_bollinger",
                        options=[{"label": x, "value": x} for x in ['Node', 'Cell', 'Cluster']],
                    )
                ]),
                html.Div(children=[
                    html.Div(children='''Select object:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="object_chklst_bollinger",
                    )
                ]),
                html.Div(children=[
                    html.Div(children='''Select mertrics:''', style={"padding":"5px 0 5px 0"}),
                    dcc.Dropdown(
                        id="metrics_chklst_bollinger",
                    )
                ]),
                
                dcc.Graph(id="bollinger_graph") 
            ],style={"background":"white", "margin":"1%", "padding":"1%","border": "1px grey", "border-radius":"10px"})
        ], style={"border":"1px grey","display":"inline-block", "width":"98%","background":"#D8BFD8", "box-shadow":"1px 4px 26px -9px rgba(155, 127, 156, 1)", "border-radius":"10px", "margin":"1%"})
    ], style={"font-family":"verdana"})


    return app.server



