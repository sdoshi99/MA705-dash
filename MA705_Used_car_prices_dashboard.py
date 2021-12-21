

import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from dash import dcc as dcc
from dash import html as html
import plotly.express as px
from dash import dash_table as dt


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

df = pd.read_csv('./Used Car Clean Data.csv')

app.layout = html.Div([html.H1('Price of Used Cars',
                      style={'fontSize': 50, 'textAlign' : 'center', 'background-color': 'MidnightBlue','color' : 'white'}),
                       
                     
            html.Div([
                html.P("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"),
                ]),
   
    html.Div([
    html.H2('-> Description:',
            style={'fontSize':30, 'textAlign':'left', 'color': 'MidnightBlue'}),
    html.Div([
        html.P("The dashboard summarizes the information of 7,632 used cars obtained from www.kaggle.com. It will allow the user to see the price of the used car based on the following categories:"),
        html.P("⦿ Brand: List of the car companies name."),
        html.P("⦿ Model: List of the model name of particular car company."),
        html.P("⦿ Miles Driven: Total number of miles driven by the car. "),
        html.P("⦿ MPG(Miles Per Gallon): Average given by the car ")
    ])
]),
    
                     
    html.Label("-> Select Brand:", style={'fontSize':30, 'textAlign':'left', 'color':'MidnightBlue'}),
    dcc.Dropdown(
        id='brandname',
        options=[{'label': b, 'value': b} for b in sorted(df.Brand.unique())],
        value='Audi',
        clearable=False
    ),
             html.Br(),
     html.Label("-> Select Model:", style={'fontSize':30, 'textAlign':'left',  'color': 'MidnightBlue'}),
    dcc.Dropdown(id='modelname',
                 options=[],
                 value=[],
                 multi=True),
    dcc.Graph(id='displayscatter', figure={}),
    dcc.Graph(id='display', figure={}),
             html.Br(),
    
    html.Div([
        html.H3('-> Search Results',
                style={'fontSize':30, 'textAlign':'left',  'color': 'MidnightBlue'}),
        
        dt.DataTable(id = 'my_datatable',
                     columns =[{'id': c, 'name':c} for c in df.columns.values],
                     virtualization = True,
                     page_action = 'native',
                     page_size=15,
                     style_table={'height': '300px', 'overflowY': 'auto'},
                     style_header={'backgroundColor': 'SlateBlue'},
                     style_cell={
                         'backgroundColor': 'Lavender',
                         'color': 'black'
                    }
    
                     )]),
             
        html.H4('-> Interpretation',
                style={'fontSize':30, 'textAlign':'left', 'color': 'MidnightBlue'}),
        html.Div([
        html.P("⦿ With an increase in Total Miles Driven and decrease in Miles per Gallon, the price of the car decreases."),
        html.P("⦿ There is an inverse relation between the price of car and total miles driven"),
       
    ]),
        html.H5('-> References -- Data Sources.',
                style={'fontSize':30, 'textAlign':'left', 'color': 'MidnightBlue'}),
        html.Div([
        html.A("⦿ Used car data.",
               href = 'https://www.kaggle.com/kukuroo3/used-car-price-dataset-competition-format/activity'),
        html.Br(),
        html.A("⦿ Scatter Plot.",
               href = 'https://plotly.com/python/line-and-scatter/'),
        html.Br(), 
        html.A("⦿ Pie Chart.",
               href = "https://plotly.com/python/pie-charts/"),
        html.Br(),
        html.A("⦿ Data Table.",
               href = "https://dash.plotly.com/datatable"),
        html.Br(),
        html.A("⦿ Color.",
               href = "https://htmlcolorcodes.com/color-names/")
       ])
    
])

server = app.server

@app.callback(
    Output('my_datatable', 'data'),
    Input('brandname', 'value'),
    Input('modelname', 'value')

)
def display_table(select_brand, select_model):
    table = df[(df.Brand == select_brand) & (df.Model.isin(select_model))]
    return table.to_dict('records')


@app.callback(
    Output('modelname', 'options'),
    Input('brandname', 'value')
)
def set_car_options(chosen_brand):
    dff = df[df.Brand==chosen_brand]
    return [{'label': c, 'value': c} for c in sorted(dff.Model.unique())]

@app.callback(
    Output('modelname', 'value'),
    Input('modelname', 'options')
)

def set_car_value(car_names):
    print(car_names)
    return [x['value'] for x in car_names]

@app.callback(
    Output('displayscatter', 'figure'),
    Input('modelname', 'value'),
    Input('brandname', 'value')
)
def update_grpah(selected_model, selected_brand):
    if len(selected_model) == 0:
        return dash.no_update
    else:
        dff = df[(df.Brand==selected_brand) & (df.Model.isin(selected_model))]
        
        fig = px.scatter(dff, x='Mileage', y='Price',
                         color='MPG',
                         trendline='ols',
                         hover_name='Model',
                         title = 'Scatter Plot of Price and Total Miles Driven of Used Cars', 
                         labels={'MPG':'Miles per Gallon',
                                 'Mileage':'Total Miles Driven',
                                 'Price':'Prices of Car'}
                         )
        return fig

@app.callback(
    Output('display', 'figure'),
    Input('modelname', 'value'),
    Input('brandname', 'value')
)
def pie_chart(choose_model, choose_brand):
   
        dfff = df[(df.Brand==choose_brand) & (df.Model.isin(choose_model))]
        
        fig1 = px.pie(dfff, values='Mileage', names='Model')
            
        return fig1



if __name__ == '__main__':
    app.run_server(debug=True)
