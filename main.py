from fastapi import FastAPI,Body # importamos la libreria
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
        'tienda':'c'
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

@app.get('/ventas/{id}',tags=['ventas'])
def buscar_ventas(id:int):
    for x in ventas:
        if x['id'] == id:
            print(x)
            return x
        else:
            continue
        
@app.get('/ventas/',tags=['ventas'])
def buscar_ventas_x_tienda(tienda: str,id: int):
    return [elemento for elemento in ventas if elemento['tienda'] == tienda]
          
@app.post('/ventas',tags=['Ventas'])
def crea_venta(id:int = Body(),fecha:str =Body(),tienda:str = Body(), importe:float =Body()):
    ventas.append(
        {
            "id":id,
            "fecha":fecha,
            "tienda":tienda,
            "importe":importe
        }
    )
    return ventas

#uvicorn main:app --reload
#uvicorn main:app --reload --port 5000
#uvicorn main:app --reload --port 5000 --host 0.0.0.0