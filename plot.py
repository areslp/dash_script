# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy
import plotly as py
import common as holo

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('data/fusion/absolute_error.csv')
print(df.head())
# print(df.iloc[5]['trans_error']) # 1.601726
base_timestamp = df.iloc[0]['time']
print(base_timestamp)
print(len(df))

df2 = pd.read_csv('data/fusion/sequence_error.csv')
print(df2.head())
print(len(df2))

df3 = pd.read_csv('data/fusion/trajectories.csv')
print(df3.head())
print(len(df3))

df4 = pd.read_csv('data/fusion/sequence_covariance_error.csv')
print(df4.head())
print(len(df4))

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Holo MLC Evaluation'),

    html.Div(children=[
        html.H2('Trajectory', style={'textAlign': 'center'}),
        holo.CreateTrajectory(df3, ['gt_x', 'gt_y'], 'GroundTruth Trajectory(UTM)'),
        holo.CreateTrajectory(df3, ['es_x', 'es_y'], 'Estimate Trajectory(UTM)'),
    ]),

    html.Div(children=[
        html.H2('Absolute Error', style={'textAlign': 'center'}),
        holo.CreateScatterGraph(df, ['trans_error', 'horizon_trans_error', 'z_error'],
                                'Translation Error', ['time(s)', 'error(m)'], base_timestamp),
        holo.CreateScatterGraph(df, ['x_error', 'y_error'], 'Longitudinal & Laterl Error', [
            'time(s)', 'error(m)'], base_timestamp),
        holo.CreateScatterGraph(df, ['rot_error', 'roll_error', 'pitch_error', 'yaw_error'], 'Rotation Error', [
            'time(s)', 'error(deg)'], base_timestamp)
    ]),

    html.Div(children=[
        html.H2('Absolute Box Error', style={'textAlign': 'center'}),
        holo.CreateBoxGraph(df, ['rot_error', 'roll_error', 'pitch_error',
                                 'yaw_error'], 'Rotation Box Error', 'error(deg)'),
        holo.CreateBoxGraph(df, ['trans_error', 'horizon_trans_error', 'z_error',
                                 'x_error', 'y_error'], 'Translation Box Error', 'error(m)')
    ]),

    html.Div(children=[
        html.H2('Velocity Error', style={'textAlign': 'center'}),
        holo.CreateScatterGraph(df, ['velx_enu_error', 'vely_enu_error', 'velz_enu_error'],
                                'ENU Velocity Error', ['time(s)', 'error(m/s)'], base_timestamp),
        holo.CreateScatterGraph(df, ['velx_body_error', 'vely_body_error', 'velz_body_error'],
                                'Body Velocity Error', ['time(s)', 'error(m/s)'], base_timestamp),
        holo.CreateScatterGraph(df, ['roll_vel_error', 'pitch_vel_error', 'yaw_vel_error'],
                                'Angular Velocity Error', ['time(s)', 'error(deg/s)'], base_timestamp),
    ]),

    html.Div(children=[
        html.H2('Velocity Box Error', style={'textAlign': 'center'}),
        holo.CreateBoxGraph(df, ['velx_enu_error', 'vely_enu_error',
                                 'velz_enu_error'], 'ENU Velocity Box Error', 'error(m/s)'),
        holo.CreateBoxGraph(df, ['velx_body_error', 'vely_body_error',
                                 'velz_body_error'], 'Body Velocity Box Error', 'error(m/s)'),
        holo.CreateBoxGraph(df, ['roll_vel_error', 'pitch_vel_error',
                                 'yaw_vel_error'], 'Angular Velocity Box Error', 'error(deg/s)'),
    ]),

    html.Div(children=[
        html.H2('Sequence Error', style={'textAlign': 'center'}),
        html.P('Please select segment length : '),
        dcc.Dropdown(
            id='segment_dropdown',
            options=[
                {'label': '100', 'value': 100},
                {'label': '200', 'value': 200},
                {'label': '300', 'value': 300},
                {'label': '400', 'value': 400},
                {'label': '500', 'value': 500},
                {'label': '600', 'value': 600},
                {'label': '700', 'value': 700},
                {'label': '800', 'value': 800},
            ],
            multi=True,
            value=[100]
        ),
        html.Div(id='sequence_translation_graph_container'),
        html.Div(id='sequence_rotation_graph_container'),
    ]),
])


@app.callback(
    dash.dependencies.Output(
        'sequence_translation_graph_container', 'children'),
    [dash.dependencies.Input('segment_dropdown', 'value')])
def update_translation_graph(value):
    return holo.CreateSequenceScatterGraph(df2, ['trans_error', 'pure_x_error', 'pure_y_error', 'pure_z_error'],
                                           value, 'Sequence Translation Error', ['time(s)', 'error(m/m)'], base_timestamp),


@app.callback(
    dash.dependencies.Output('sequence_rotation_graph_container', 'children'),
    [dash.dependencies.Input('segment_dropdown', 'value')])
def update_rotation_graph(value):
    return holo.CreateSequenceScatterGraph(df2, ['rot_error', 'roll_error', 'pitch_error', 'yaw_error'],
                                           value, 'Sequence Rotation Error', ['time(s)', 'error(deg/m)'], base_timestamp),


if __name__ == '__main__':
    app.run_server(debug=False)
