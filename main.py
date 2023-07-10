# importamos la libreria
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse,JSONResponse #agregamos JsnResponse para poder mandar respuestas
from pydantic import BaseModel,Field 
# Basemodel = para declarar tipos clases, #Field herramienta para las validaciones
from typing import Optional,List #list para poder enviar el tipo que deseamos obtener

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

######## Tipo Clase ################3
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
#8 #12 JSONResponse #12.1 devolver tipo objeto
@app.post('/venta_ob',tags=['venta_obj'],response_model=dict,status_code=200) 
                                        #indicamos que vamos a devolver un modelo tipo ventas
def venta_obt(venta:Ventas)->List[Ventas]:
    venta = dict(venta)
    List_venta.append(venta)
    #return List_venta #8
    return JSONResponse(content=List_venta,status_code=200)

#9  #12 JSONResponse
@app.put('/venta_ob/{id}',tags=['venta_obt'],response_model=dict,status_code=201)
def venta_act(id:int, ventas:Ventas)->Ventas:
    for element in List_venta:
        if element['id']==id:
            element['fecha']=ventas.fecha
            element['tienda'] = ventas.tienda
            element['importe'] = ventas.importe
    #return List_venta
    return JSONResponse(content={'mensaje':'Actualizada venta'},status_code=201)

######## Tipo Clase ################3

#creamos punto de entrada o end point #1 
@app.get('/',tags=['Inicio'])#cambio de etiqueta en documentacion
def mensaje():
    #return 'Holamundo2'
    return HTMLResponse('<h2> Titulo de fast api</h2> ') #salida de fast api

#2 #12 vamos a devolver por jsonResponse
@app.get('/ventas',tags=['ventas'],response_model=List[Ventas],status_code=200)
def mensaje_ventas()->List[Ventas]:
    #return List_venta #2
    return JSONResponse(content=List_venta,status_code=200)

#3 #10 agregamos path #12 devolvermos JSONResponse el dato x
@app.get('/ventas/{id}',tags=['ventas'],response_model=List[Ventas], status_code=200)
def buscar_ventas(id:int = Path(ge=1,le=100))->Ventas:
    for x in List_venta:
        if x['id'] == id:
            print(x)
            #return x
            return JSONResponse(content=x,status_code=200)
        else:
            continue
    return JSONResponse(content=[],status_code=404)

#4  # 11 Se agrega Query #JSONResponse
@app.get('/ventas/',tags=['ventas'],response_model=List[Ventas])
def buscar_ventas_x_tienda(tienda: str =Query(min_length=4,max_length=20),id: int =Query(ge=1 ,le=100))->List[Ventas]:
    datos =[elemento for elemento in List_venta if elemento['tienda'] == tienda] #12
    print(datos)
    #return [elemento for elemento in List_venta if elemento['tienda'] == tienda] #4
    return JSONResponse(content=datos) #12

#5          #12 JSONResponse
@app.post('/ventas',tags=['Ventas'],response_model=List[Ventas],status_code=201)
def crea_venta(id:int = Body(),fecha:str =Body(),tienda:str = Body(), importe:float =Body())->dict:
    List_venta.append(
        {
            "id":id,
            "fecha":fecha,
            "tienda":tienda,
            "importe":importe
        }
    )
    #return List_venta #5
    return JSONResponse(content={'Mensaje':'Venta Registrada'},status_code=201) #12 JSONResponse

#6
@app.put('/ventas/{id}',tags=['Ventas'],response_model=dict,status_code=201)
def actualizamos_venta(id:int,fecha:str=Body(),tienda:str=Body(),importe:float=Body())->dict:
    #recorremos los elementos de la lista.
    for elemen in List_venta:
        if  elemen['id'] == id:
            elemen['fecha'] = fecha
            elemen['tienda'] = tienda
            elemen['importe'] = importe
    #ventas = elemen    

   # return List_venta #6
    return JSONResponse(content={'mensaje':'Registro Actualizado'},status_code=201)
#7   #12 JSONResponse
@app.delete('/ventas/{id}',tags=['Ventas'],response_model=dict,status_code=200)
def eliminar_ventas(id:int)->dict:
    for element in List_venta:
        if element['id'] == id:
            List_venta.remove(element)
            return JSONResponse(content={'mensaje':'Se elimino sin inconvenientes'})
        #return List_venta
    return JSONResponse(content={'mensaje':'No se encontro'},status_code=200)

#uvicorn main:app --reload
#uvicorn main:app --reload --port 5000
#uvicorn main:app --reload --port 5000 --host 0.0.0.0