
                '''
                go.Scatter(
                    x=df.iloc[i]['time']-base_time),
                    y=df.iloc[i]['horizon_trans_error'],
                    text=[df.iloc[i]['time'], i],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in range(5)
                '''

        dcc.Graph(
            id='horizon_error_figure',
            figure=go.Figure(
                data=[
                    go.Scattergl(
                        x=df['time']-base_time,
                        y=df['horizon_trans_error'],
                        text=df['time'],
                        mode='lines+markers',
                        name='horizon_trans_error',
                        hoverinfo='y+text+name',
                        textposition='top left',
                        hoverlabel={'namelength': -1},
                        opacity=0.7
                    )
                ],

                layout=go.Layout(
                    title='Horizon Error Figure',
                    showlegend=True
                )
            )
        )