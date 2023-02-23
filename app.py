# from dash import Dash, dcc, html, Input, Output, State  
# import plotly.graph_objs as go
# import pickle
# import pandas as pd

# app = Dash()  

# app.layout = html.Div(children=[  
#     html.H1(children='Linear Regresion Predictive Model', style={'textAlign': 'center', "color":"#9fd3c7"}),  
#     html.H2(children='Boston Houses Example', style={'textAlign': 'center','color':'#9fd3c7'}), 
#     html.Div(children=[  
#         html.P([  
#           html.Label('Percentage of lower status of the population (lstat): '),  
#           dcc.Input(id='lstat', placeholder='Percentage of lower status', type='text') 
#         ]),
#         html.P([  
#           html.Label('Average number of rooms per dwelling (rm): '),  
#           dcc.Input(id='rm', placeholder='Average number of rooms', type='text')  
#         ]),
#         html.Button(id='submit-button', n_clicks=0, children='Predict Price'), 
#         html.P([  
#            html.Label('Predicted Price: $'),  
#            dcc.Input(value='0', type='text', id='pred', placeholder='Predicted Price')  
#         ]),
#         html.Div(id='result') 
#     ], style={'textAlign': 'center', "color":"#ececec"})  

# ], style={"backgroundColor":"#142d4c"}) 


# @app.callback(
#     Output(component_id='pred', component_property='value'),  
#     [Input('submit-button', 'n_clicks'),  
#     State(component_id='lstat', component_property='value'),  
#     State(component_id='rm', component_property='value')] 
#     )
# def prediction(n_clicks,lstat,rm):  
#     if lstat != None and lstat != '' and rm != None and rm != '':  
#         try:  
#             # X = pd.read_csv("testdf.csv")
#             prediccion = model.predict(X)  
#             return prediccion 
#         except ValueError:
#             return 'Value error in lstat or rm'


# if __name__ == '__main__': 
#     nombre_archivo='modelo.pkl'  
#     archivo_entrada=open(nombre_archivo,'rb') 
#     model=pickle.load(archivo_entrada) 
#     archivo_entrada.close() 
#     app.run_server(debug=True) 

import base64
import datetime
import io
import pickle

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children='Modelo de clasificación para predicción de defectos', style={'textAlign': 'center', "color":"#9fd3c7"}),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastra un archivo o ',
            html.A('selecciona uno')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            "color":"#ececec"
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
], style={"backgroundColor":"#142d4c"})

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    print(content_string)

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        X = df
        prediccion = model.predict(X)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    df.reset_index(inplace=True)
    return html.Div([
        html.Label('Nombre del archivo: ', style={"color":"#ececec"}),
        html.H5(filename, style={"color":"#ececec"}),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),
        
        html.P([  
           html.Label('Predicciones: ', style={"color":"#ececec"}),  
           #dcc.Input(value=repr(prediccion), type='text', readOnly=True),  
           
        ]),
        html.Table(
            
                [html.Tr([html.Td(i), html.Td(c)], style={"color":"#ececec"}) for i, c in enumerate(prediccion)]
                #html.Tr([html.Td(c) for c in data]),
                #[html.Tr(c) for c in prediccion]
            
        # dash_table.DataTable(
        #     [{'index': list(range(len(prediccion))), 'prediccion': list(prediccion.astype(str))}],
        ),
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    nombre_archivo='d:/Descargas/HOLA/modelo.pkl'  
    archivo_entrada=open(nombre_archivo,'rb') 
    model=pickle.load(archivo_entrada) 
    archivo_entrada.close() 
    app.run_server(debug=True)