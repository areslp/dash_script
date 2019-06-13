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

lon_trans = df['x_error'].to_numpy()
# print(np.mean(lon_trans))
# print(np.std(lon_trans))
# print(np.median(lon_trans))
# print(np.max(lon_trans))
# print(np.min(lon_trans))

lat_trans = df['y_error'].to_numpy()
trans = df['trans_error'].to_numpy()
yaw = df['yaw_error'].to_numpy()
rot = df['rot_error'].to_numpy()
sequence_trans = df2['trans_error'].to_numpy()
sequence_rot = df2['rot_error'].to_numpy()

test = pd.read_csv('solar.csv')
data = test.to_dict('records')
print(data)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Holo MLC Evaluation'),

    html.Div(children=[
        html.H2('Trajectory', style={'textAlign': 'center'}),
        holo.CreateTrajectory(
            df3, [['gt_x', 'gt_y'], ['es_x', 'es_y']], 'Trajectory(UTM)'),
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
        holo.CreateSequenceScatterGraph(df2, ['trans_error', 'pure_x_error', 'pure_y_error', 'pure_z_error'],
                                        [100], 'Sequence Translation Error', ['time(s)', 'error(m/m)'], base_timestamp),
        holo.CreateSequenceScatterGraph(df2, ['rot_error', 'roll_error', 'pitch_error', 'yaw_error'],
                                        [100], 'Sequence Rotation Error', ['time(s)', 'error(deg/m)'], base_timestamp),
    ]),

    html.Div(children=[
        html.H2('Sequence Box Error', style={'textAlign': 'center'}),
        holo.CreateSequenceBoxGraph(df2, ['trans_error', 'pure_x_error', 'pure_y_error', 'pure_z_error'],
                                    [100, 200, 300, 400, 500, 600, 700, 800], 'Sequence Translation Box Error', 'error(m/m)'),
        holo.CreateSequenceBoxGraph(df2, ['rot_error', 'roll_error', 'pitch_error', 'yaw_error'],
                                    [100, 200, 300, 400, 500, 600, 700, 800], 'Sequence Rotation Box Error', 'error(deg/m)'),
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
                #'backgroundColor': 'green',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': ''},
                    #'backgroundColor': 'red',
                    'fontWeight': 'bold'
                }
            ],
        ),
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=False)
