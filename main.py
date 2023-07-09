from fastapi import FastAPI,Body # importamos la libreria
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.title = 'aplicacion mensaje'
app.version = '1.0.1'

#vamos usarlo para mostrar nada mas
List_venta =[
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

#Vamos a crear un modelo.
class Ventas(BaseModel):
    id: Optional[int]=None
    fecha:str
    tienda:str
    importe:float
        

@app.post('/venta_ob',tags=['venta_obj'])
def venta_obt(venta:Ventas):
    List_venta.append(venta)
    return List_venta
@app.put('/venta_ob/{id}',tags=['venta_obt'])
def venta_act(id:int, ventas:Ventas):
    for element in List_venta:
        if element['id']==id:
            element['fecha']=ventas.fecha
            element['tienda'] = ventas.tienda
            element['importe'] = ventas.importe
    return List_venta
#creamos punto de entrada o end point
@app.get('/',tags=['Inicio'])#cambio de etiqueta en documentacion
def mensaje():
    #return 'Holamundo2'
    return HTMLResponse('<h2> Titulo de fast api</h2> ') #salida de fast api

@app.get('/ventas',tags=['ventas'])
def mensaje_ventas():
    return List_venta

@app.get('/ventas/{id}',tags=['ventas'])
def buscar_ventas(id:int):
    for x in List_venta:
        if x['id'] == id:
            print(x)
            return x
        else:
            continue
        
@app.get('/ventas/',tags=['ventas'])
def buscar_ventas_x_tienda(tienda: str,id: int):
    return [elemento for elemento in List_venta if elemento['tienda'] == tienda]
          
@app.post('/ventas',tags=['Ventas'])
def crea_venta(id:int = Body(),fecha:str =Body(),tienda:str = Body(), importe:float =Body()):
    List_venta.append(
        {
            "id":id,
            "fecha":fecha,
            "tienda":tienda,
            "importe":importe
        }
    )
    return List_venta

@app.put('/ventas/{id}',tags=['Ventas'])
def actualizamos_venta(id:int,fecha:str=Body(),tienda:str=Body(),importe:float=Body()):
    #recorremos los elementos de la lista.
    for elemen in List_venta:
        if  elemen['id'] == id:
            elemen['fecha'] = fecha
            elemen['tienda'] = tienda
            elemen['importe'] = importe
    #ventas = elemen    

    return List_venta
 
@app.delete('/ventas/{id}',tags=['Ventas'])
def eliminar_ventas(id:int):
    for element in List_venta:
        if element['id'] == id:
            List_venta.remove(element)
        return List_venta

#uvicorn main:app --reload
#uvicorn main:app --reload --port 5000
#uvicorn main:app --reload --port 5000 --host 0.0.0.0