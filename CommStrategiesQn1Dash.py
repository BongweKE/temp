import dash
from dash import dcc, html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="Veronica's Health Dashboard"),

    html.Div(children='''
        Visualizations of Veronica's health data.
    '''),

    dcc.Graph(id='glucose-trend'),
    dcc.Graph(id='calorie-intake'),
    dcc.Graph(id='health-metrics'),
    dcc.Graph(id='daily-calorie-intake'),
])


@app.callback(
    Output('glucose-trend', 'figure'),
    Input('glucose-trend', 'id') # Dummy input
)
def update_glucose_trend(id):
    fig = go.Figure(data=go.Scatter(x=df['Date'], y=df['Blood Glucose'], mode='lines+markers'))
    fig.update_layout(title='Blood Glucose Trend', xaxis_title='Date', yaxis_title='Blood Glucose')
    return fig

@app.callback(
    Output('calorie-intake', 'figure'),
    Input('calorie-intake', 'id')
)
def update_calorie_intake(id):
    meal_types = ['Breakfast Calories', 'Lunch Calories', 'Dinner Calories', 'Desert Calories']
    fig = go.Figure(data=[go.Bar(name=meal, x=meal_types, y=df[meal].mean()) for meal in meal_types])
    fig.update_layout(title='Average Caloric Intake by Meal Type', xaxis_title='Meal Type', yaxis_title='Average Calories')
    return fig

@app.callback(
    Output('health-metrics', 'figure'),
    Input('health-metrics', 'id')
)
def update_health_metrics(id):
    fig = go.Figure(data=go.Scatter(x=df['Exercise (minutes)'], y=df['Heart Rate'], mode='markers', marker=dict(size=df['Blood Pressure'])))
    fig.update_layout(title='Blood Pressure and Heart Rate vs Exercise', xaxis_title='Exercise (minutes)', yaxis_title='Heart Rate',
                      xaxis=dict(range=[0,df['Exercise (minutes)'].max() + 10]), yaxis=dict(range=[0, df['Heart Rate'].max() + 10]))
    return fig


@app.callback(
    Output('daily-calorie-intake', 'figure'),
    Input('daily-calorie-intake', 'id')
)
def update_daily_calorie_intake(id):
    recommended_threshold = 2000 # Replace with the actual recommended threshold
    fig = go.Figure(data=[go.Bar(x=df['Date'], y=df['Total Calories'], name='Total Calories'),
                         go.Scatter(x=df['Date'], y=[recommended_threshold]*len(df), name='Recommended Threshold')])
    fig.update_layout(title='Total Daily Calorie Intake vs Threshold', xaxis_title='Date', yaxis_title='Calories')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
