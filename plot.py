# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import plotly as py
import common as holo

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

abs = pd.read_csv('data/fusion/absolute_error.csv')  # df
print(abs.head())
# print(df.iloc[5]['trans_error']) # 1.601726
base_timestamp = abs.iloc[0]['time']
print(base_timestamp)
print(len(abs.index))

seq = pd.read_csv('data/fusion/sequence_error.csv')  # df2
print(seq.head())
print(len(seq.index))

traj = pd.read_csv('data/fusion/trajectories.csv')  # df3
print(traj.head())
print(len(traj.index))

df4 = pd.read_csv('data/fusion/sequence_covariance_error.csv')  # df4
print(df4.head())
print(len(df4))

lon_trans = abs['x_error'].to_numpy()
# print(np.mean(lon_trans))
# print(np.std(lon_trans))
# print(np.median(lon_trans))
# print(np.max(lon_trans))
# print(np.min(lon_trans))

lat_trans = abs['y_error'].to_numpy()
trans = abs['trans_error'].to_numpy()
yaw = abs['yaw_error'].to_numpy()
rot = abs['rot_error'].to_numpy()
sequence_trans = seq['trans_error'].to_numpy()
sequence_rot = seq['rot_error'].to_numpy()

df = abs
df2 = seq
df3 = traj

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Holo MLC Evaluation'),
    html.H2(children='Absolute Evaluation'),

    dcc.RangeSlider(
        id='overall_slider',
        marks={i : '{:f}'.format(i) for i in np.arange(0.0, 1.0, 0.1)},
        min=0.0,
        max=1.0,
        step=0.1,
        value=[0.0, 0.5],
    ),

    html.Br(children=[
    ]),
    html.Br(children=[
    ]),

    html.Div(children=[
        html.Div(id='dummy', style={'display': 'none'}),
    ]),

    dcc.Checklist(
        id='overall_checkbox',
        options=[
            {'label': 'Trajectory', 'value': 'T'},
            {'label': 'Absolute error', 'value': 'A'},
            {'label': 'Absolute box error', 'value': 'AB'},
            {'label': 'Velocity error', 'value': 'V'},
            {'label': 'Velocity box error', 'value': 'VB'},
        ],
        values=[],
        labelStyle={'display': 'inline-block'}
    ),

    html.Div(children=[
        html.Div(id='trajectory_container'),
    ]),

    html.Div(children=[
        html.Div(id='absolute_container'),
    ]),

    html.Div(children=[
        html.Div(id='absolute_box_container'),
    ]),

    html.Div(children=[
        html.Div(id='velocity_container'),
    ]),

    html.Div(children=[
        html.Div(id='velocity_box_container'),
    ]),

    html.H2(children='Sequence Evaluation'),

    dcc.Checklist(
        id='sequence_checkbox',
        options=[
            {'label': 'Sequence translation error', 'value': 'ST'},
            {'label': 'Sequence rotation error', 'value': 'SR'},
            {'label': 'Sequence box error', 'value': 'SB'},
        ],
        values=[''],
        labelStyle={'display': 'inline-block'}
    ),

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
        value=[]
    ),

    html.Div(children=[
        html.Div(id='sequence_translation_graph_container'),
        html.Div(id='sequence_rotation_graph_container'),
    ]),

    html.Div(children=[
        html.Div(id='sequence_box_container'),
    ]),

    html.Div(children=[
        html.H2('Result Table', style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='table',
            columns=[{'name': '', 'id': ''}, {'name': 'Lon Trans', 'id': 'lon_trans'}, {'name': 'Lat Trans', 'id': 'lat_trans'}, {'name': 'Trans', 'id': 'trans'},
                     {'name': 'Yaw', 'id': 'yaw'}, {'name': 'Rot', 'id': 'rot'}, {'name': 'Sequence Trans', 'id': 'sequence_trans'}, {'name': 'Sequence Rot', 'id': 'sequence_rot'}],
            data=[
                {'': 'Min', 'lon_trans': np.min(lon_trans), 'lat_trans': np.min(lat_trans), 'trans': np.min(trans), 'yaw': np.min(
                    yaw), 'rot': np.min(rot), 'sequence_trans': np.min(sequence_trans), 'sequence_rot': np.min(sequence_rot)},
                {'': 'Max', 'lon_trans': np.max(lon_trans), 'lat_trans': np.max(lat_trans), 'trans': np.max(trans), 'yaw': np.max(
                    yaw), 'rot': np.max(rot), 'sequence_trans': np.max(sequence_trans), 'sequence_rot': np.max(sequence_rot)},
                {'': 'Mean', 'lon_trans': np.mean(lon_trans), 'lat_trans': np.mean(lat_trans), 'trans': np.mean(trans), 'yaw': np.mean(
                    yaw), 'rot': np.mean(rot), 'sequence_trans': np.mean(sequence_trans), 'sequence_rot': np.mean(sequence_rot)},
                {'': 'Median', 'lon_trans': np.median(lon_trans), 'lat_trans': np.median(lat_trans), 'trans': np.median(trans), 'yaw': np.median(
                    yaw), 'rot': np.median(rot), 'sequence_trans': np.median(sequence_trans), 'sequence_rot': np.median(sequence_rot)},
                {'': 'Std', 'lon_trans': np.std(lon_trans), 'lat_trans': np.std(lat_trans), 'trans': np.std(trans), 'yaw': np.std(
                    yaw), 'rot': np.std(rot), 'sequence_trans': np.std(sequence_trans), 'sequence_rot': np.std(sequence_rot)},
                {'': 'Rms', 'lon_trans': np.sqrt(np.mean(lon_trans**2)), 'lat_trans': np.sqrt(np.mean(lat_trans**2)), 'trans': np.sqrt(np.mean(trans**2)), 'yaw': np.sqrt(
                    np.mean(yaw**2)), 'rot': np.sqrt(np.mean(rot**2)), 'sequence_trans': np.sqrt(np.mean(sequence_trans**2)), 'sequence_rot': np.sqrt(np.mean(sequence_rot**2))},
            ],
            style_header={
                # 'backgroundColor': 'green',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': ''},
                    # 'backgroundColor': 'red',
                    'fontWeight': 'bold'
                }
            ],
        ),
    ]),
])


@app.callback(
    dash.dependencies.Output(
        'dummy', 'children'),
    [dash.dependencies.Input('overall_slider', 'value')])
def update_df(value):
    global df
    global df2
    global df3
    df = abs.iloc[int(value[0] * len(abs.index)): int(value[1] * len(abs.index))]
    df2 = seq.iloc[int(value[0] * len(seq.index)): int(value[1] * len(seq.index))]
    df3 = traj.iloc[int(value[0] * len(traj.index)): int(value[1] * len(traj.index))]
    return value

@app.callback(
    dash.dependencies.Output(
        'sequence_translation_graph_container', 'children'),
    [dash.dependencies.Input('segment_dropdown', 'value'),
     dash.dependencies.Input('sequence_checkbox', 'values'),
     dash.dependencies.Input('dummy', 'children')])
def update_translation_graph(value, values, dummy):
    if 'ST' in values:
        return [
            html.H2('Sequence Translation Error',
                    style={'textAlign': 'center'}),
            holo.CreateSequenceScatterGraph(df2, ['trans_error', 'pure_x_error', 'pure_y_error', 'pure_z_error'],
                                            value, 'Sequence Translation Error', ['time(s)', 'error(m)'], base_timestamp),
        ]


@app.callback(
    dash.dependencies.Output('sequence_rotation_graph_container', 'children'),
    [dash.dependencies.Input('segment_dropdown', 'value'),
     dash.dependencies.Input('sequence_checkbox', 'values'),
     dash.dependencies.Input('dummy', 'children')])
def update_rotation_graph(value, values, dummy):
    if 'SR' in values:
        return [
            html.H2('Sequence Rotation Error',
                    style={'textAlign': 'center'}),
            holo.CreateSequenceScatterGraph(df2, ['rot_error', 'roll_error', 'pitch_error', 'yaw_error'],
                                            value, 'Sequence Rotation Error', ['time(s)', 'error(deg/m)'], base_timestamp),
        ]


@app.callback(
    dash.dependencies.Output('sequence_box_container', 'children'),
    [dash.dependencies.Input('segment_dropdown', 'value'),
     dash.dependencies.Input('sequence_checkbox', 'values'),
     dash.dependencies.Input('dummy', 'children')])
def update_sequence_box_graph(value, values, dummy):
    if 'SB' in values:
        return [
            html.H2('Sequence Box Error', style={'textAlign': 'center'}),
            holo.CreateSequenceBoxGraph(df2, ['trans_error', 'pure_x_error', 'pure_y_error', 'pure_z_error'],
                                        value, 'Sequence Translation Box Error', 'error(m/m)'),
            holo.CreateSequenceBoxGraph(df2, ['rot_error', 'roll_error', 'pitch_error', 'yaw_error'],
                                        value, 'Sequence Rotation Box Error', 'error(deg/m)'),
        ]


@app.callback(
    dash.dependencies.Output(
        'absolute_container', 'children'),
    [dash.dependencies.Input('overall_checkbox', 'values'),
     dash.dependencies.Input('dummy', 'children')])
def update_absolute_graph(value, dummy):
    if 'A' in value:
        return [
            html.H2('Absolute Error', style={'textAlign': 'center'}),
            holo.CreateScatterGraph(df, ['trans_error', 'horizon_trans_error', 'z_error'],
                                    'Translation Error', ['time(s)', 'error(m)'], base_timestamp),
            holo.CreateScatterGraph(df, ['x_error', 'y_error'], 'Longitudinal & Laterl Error', [
                'time(s)', 'error(m)'], base_timestamp),
            holo.CreateScatterGraph(df, ['rot_error', 'roll_error', 'pitch_error', 'yaw_error'], 'Rotation Error', [
                'time(s)', 'error(deg)'], base_timestamp),
            holo.CreateSequenceScatterGraph(df2, ['trans_error', 'pure_x_error', 'pure_y_error', 'pure_z_error'],
                                            value, 'Sequence Translation Error', ['time(s)', 'error(m)'], base_timestamp),
        ]


@app.callback(
    dash.dependencies.Output(
        'trajectory_container', 'children'),
    [dash.dependencies.Input('overall_checkbox', 'values'),
     dash.dependencies.Input('dummy', 'children')])
def update_trajectory_graph(value, dummy):
    if 'T' in value:
        return [
            html.H2('Trajectory', style={'textAlign': 'center'}),
            holo.CreateTrajectory(
                df3, [['gt_x', 'gt_y'], ['es_x', 'es_y']], 'Trajectory(UTM)'),
        ]


@app.callback(
    dash.dependencies.Output(
        'absolute_box_container', 'children'),
    [dash.dependencies.Input('overall_checkbox', 'values'),
     dash.dependencies.Input('dummy', 'children')])
def update_absolute_box_graph(value, dummy):
    if 'AB' in value:
        return [
            html.H2('Absolute Box Error', style={'textAlign': 'center'}),
            holo.CreateBoxGraph(df, ['rot_error', 'roll_error', 'pitch_error',
                                     'yaw_error'], 'Rotation Box Error', 'error(deg)'),
            holo.CreateBoxGraph(df, ['trans_error', 'horizon_trans_error', 'z_error',
                                     'x_error', 'y_error'], 'Translation Box Error', 'error(m)')
        ]


@app.callback(
    dash.dependencies.Output(
        'velocity_container', 'children'),
    [dash.dependencies.Input('overall_checkbox', 'values'),
     dash.dependencies.Input('dummy', 'children')])
def update_velocity_graph(value, dummy):
    if 'V' in value:
        return [
            html.H2('Velocity Error', style={'textAlign': 'center'}),
            holo.CreateScatterGraph(df, ['velx_enu_error', 'vely_enu_error', 'velz_enu_error'],
                                    'ENU Velocity Error', ['time(s)', 'error(m/s)'], base_timestamp),
            holo.CreateScatterGraph(df, ['velx_body_error', 'vely_body_error', 'velz_body_error'],
                                    'Body Velocity Error', ['time(s)', 'error(m/s)'], base_timestamp),
            holo.CreateScatterGraph(df, ['roll_vel_error', 'pitch_vel_error', 'yaw_vel_error'],
                                    'Angular Velocity Error', ['time(s)', 'error(deg/s)'], base_timestamp),
        ]


@app.callback(
    dash.dependencies.Output(
        'velocity_box_container', 'children'),
    [dash.dependencies.Input('overall_checkbox', 'values'),
     dash.dependencies.Input('dummy', 'children')])
def update_velocity_box_graph(value, dummy):
    if 'VB' in value:
        return [
            html.H2('Velocity Box Error', style={'textAlign': 'center'}),
            holo.CreateBoxGraph(df, ['velx_enu_error', 'vely_enu_error',
                                     'velz_enu_error'], 'ENU Velocity Box Error', 'error(m/s)'),
            holo.CreateBoxGraph(df, ['velx_body_error', 'vely_body_error',
                                     'velz_body_error'], 'Body Velocity Box Error', 'error(m/s)'),
            holo.CreateBoxGraph(df, ['roll_vel_error', 'pitch_vel_error',
                                     'yaw_vel_error'], 'Angular Velocity Box Error', 'error(deg/s)'),
        ]


if __name__ == '__main__':
    app.run_server(debug=False)
