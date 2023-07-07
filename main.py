from fastapi import FastAPI # importamos la libreria
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = 'aplicacion mensaje'
app.version = '1.0.1'

#vamos usarlo para mostrar nada mas
ventas =[
    {
        'id':1,
        'fecha':'20230706',
        'importe':2500,
        'tienda':'tienda01'
    },
    {
        'id':2,
        'fecha':20230606,
        'importe':1222,
        'tienda': 'tienda02'
    }
]

#creamos punto de entrada o end point
@app.get('/',tags=['Inicio'])#cambio de etiqueta en documentacion
def mensaje():
    #return 'Holamundo2'
    return HTMLResponse('<h2> Titulo de fast api</h2> ') #salida de fast api

@app.get('/ventas',tags=['ventas'])
def mensaje_ventas():
    return ventas


#uvicorn main:app --reload
#uvicorn main:app --reload --port 5000
#uvicorn main:app --reload --port 5000 --host 0.0.0.0