# importamos la libreria
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel,Field 
# Basemodel = para declarar tipos clases, #Field herramienta para las validaciones
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
#8, 9
class Ventas(BaseModel):
    #id: Optional[int]=None  #En caso que no se tenga validacion en el objeto
    id: int =Field(ge=0,le=200)
    fecha:str
    #tienda:str = Field(default="tienda01",min_length=4, max_length=20)
    tienda:str = Field(min_length=4, max_length=20)
    #tienda:str
    importe:float
    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "fecha":'2023-12-01',
                'tienda':'tienda01',
                'importe': 10
            }
        }        
#8
@app.post('/venta_ob',tags=['venta_obj'])
def venta_obt(venta:Ventas):
    List_venta.append(venta)
    return List_venta
#9
@app.put('/venta_ob/{id}',tags=['venta_obt'])
def venta_act(id:int, ventas:Ventas):
    for element in List_venta:
        if element['id']==id:
            element['fecha']=ventas.fecha
            element['tienda'] = ventas.tienda
            element['importe'] = ventas.importe
    return List_venta

#creamos punto de entrada o end point #1
@app.get('/',tags=['Inicio'])#cambio de etiqueta en documentacion
def mensaje():
    #return 'Holamundo2'
    return HTMLResponse('<h2> Titulo de fast api</h2> ') #salida de fast api

#2
@app.get('/ventas',tags=['ventas'])
def mensaje_ventas():
    return List_venta

#3 #10 agregamos path
@app.get('/ventas/{id}',tags=['ventas'])
def buscar_ventas(id:int = Path(ge=1,le=100)):
    for x in List_venta:
        if x['id'] == id:
            print(x)
            return x
        else:
            continue
#4  # 11 Se agrega Query
@app.get('/ventas/',tags=['ventas'])
def buscar_ventas_x_tienda(tienda: str =Query(min_length=4,max_length=20),id: int =Query(ge=1 ,le=100)):
    return [elemento for elemento in List_venta if elemento['tienda'] == tienda]

#5          
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
#6
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
#7 
@app.delete('/ventas/{id}',tags=['Ventas'])
def eliminar_ventas(id:int):
    for element in List_venta:
        if element['id'] == id:
            List_venta.remove(element)
        return List_venta

#uvicorn main:app --reload
#uvicorn main:app --reload --port 5000
#uvicorn main:app --reload --port 5000 --host 0.0.0.0