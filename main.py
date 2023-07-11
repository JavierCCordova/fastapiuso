# importamos la libreria
from fastapi import FastAPI, Body, Path, Query, Request,HTTPException, Depends #14 Request,HTTPException,Depends
from fastapi.security import HTTPBearer # 14 para la seguridad aplicarlo
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials #agregamos JsnResponse para poder mandar respuestas
from fastapi.encoders import jsonable_encoder #16 para pasar listado json
from pydantic import BaseModel,Field 
# Basemodel = para declarar tipos clases, #Field herramienta para las validaciones
from typing import Optional,List

from config.BBDD import sesion,motor,base
from modelos.ventas import Ventas as Ventas_modelo

from starlette.requests import Request #list para poder enviar el tipo que deseamos obtener
from jwt_config import get_token,valide_token

app = FastAPI()
app.title = 'aplicacion mensaje'
app.version = '1.0.1'

base.metadata.create_all(bind=motor)

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
######## Portador de token ################14
class Portador(HTTPBearer):
    async def __call__(self, request: Request):
        autorizacion = await super().__call__(request)
        dato = valide_token(autorizacion.credentials)
        if dato['email']!= 'holamundo@gmail.com':
            raise HTTPException(status_code=403, detail='No autorizado')

######## Tipo Clase validacion ################3
class Usuario(BaseModel):
    email:str
    clave:str

    #creamos ruta para login #13 para haacer pruebas de token para usarlo
@app.post('/login',tags=['autenticacion'])    
def login(usuario:Usuario):
    if usuario.email == 'holamundo@gmail.com' and usuario.clave=='123':
        #obtener el token pasale 
        token = get_token(usuario.dict())
        return JSONResponse(content=token,status_code=200)
    return JSONResponse(content={"mensaje":'Error de acceso denegado'},status_code=400)

######## Tipo Clase ################3
#Vamos a crear un modelo.
#8, 9
class Ventas(BaseModel):
    #id: Optional[int]=None  #En caso que no se tenga validacion en el objeto
    #id: int =Field(ge=0,le=200)
    id: Optional[int]=None 
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
#8 #12 JSONResponse #12.1 devolver tipo objeto #16 sessiones
@app.post('/venta_ob',tags=['venta_obj'],response_model=List[Ventas],status_code=200) 
                                        #indicamos que vamos a devolver un modelo tipo ventas
def venta_obt(venta:Ventas)->dict:
    db = sesion() #16 
    #Traemos los atributos para el modelo.
    nueva_venta = Ventas_modelo(**venta.dict())
    #añadir bbdd y commit para actualizar
    db.add(nueva_venta)
    db.commit()

    ''' 
    venta = dict(venta)
    List_venta.append(venta)
    #return List_venta #8
    return JSONResponse(content=List_venta,status_code=200)
    '''
    return JSONResponse(content={'mensaje':'Venta registrada'},status_code=200)

#9  #12 JSONResponse
'''
    for element in List_venta:
        if element['id']==id:
            element['fecha']=ventas.fecha
            element['tienda'] = ventas.tienda
            element['importe'] = ventas.importe
    #return List_venta
    return JSONResponse(content={'mensaje':'Actualizada venta'},status_code=201)
'''
@app.put('/venta_ob/{id}',tags=['venta_obt'],response_model=dict,status_code=201)
def venta_act(id:int, ventas:Ventas)->dict:
  
    db =sesion()
    resultado = db.query(Ventas_modelo).filter(Ventas_modelo.id == id).first()
    if not resultado:
        return JSONResponse(status_code=404,content={'mensaje':'No se actualizo'})
    else:
        resultado.fecha  = ventas.fecha
        resultado.tienda = ventas.tienda
        resultado.importe = ventas.importe
        db.commit
        return JSONResponse(status_code=200,content={'mensaje':'registro actualizado'})
    

######## Tipo Clase ################3

#creamos punto de entrada o end point #1 
@app.get('/',tags=['Inicio'])#cambio de etiqueta en documentacion
def mensaje():
    #return 'Holamundo2'
    return HTMLResponse('<h2> Titulo de fast api</h2> ') #salida de fast api

#2 #12 vamos a devolver por jsonResponse
@app.get('/ventas',tags=['ventas'],response_model=List[Ventas],status_code=200,dependencies=[Depends(Portador())])
def mensaje_ventas()->List[Ventas]:
    #15 para obtener de la bbdd
    bd = sesion()    
    resultado = bd.query(Ventas_modelo).all()

    return JSONResponse(status_code=200,content=jsonable_encoder(resultado))
    #return List_venta #2
    #return JSONResponse(content=List_venta,status_code=200) 

#3 #10 agregamos path #12 devolvermos JSONResponse el dato x
    '''
    for x in List_venta:
        if x['id'] == id:
            print(x)
            #return x
            return JSONResponse(content=x,status_code=200)
        else:
            continue
    return JSONResponse(content=[],status_code=404)'''    
@app.get('/ventas/{id}',tags=['ventas'],response_model=List[Ventas], status_code=200)
def buscar_ventas(id:int = Path(ge=1,le=100))->Ventas:
    #15 consulta BBDD
    bd = sesion()
    resultado = bd.query(Ventas_modelo).filter(Ventas_modelo.id == id).all()

    if not resultado:
        return JSONResponse(status_code=404,content={'mensaje':'No se encontro el identificador'})
    else:
        return JSONResponse(status_code=200,content=jsonable_encoder(resultado))


#4  # 11 Se agrega Query #JSONResponse
@app.get('/ventas/',tags=['ventas'],response_model=List[Ventas])
def buscar_ventas_x_tienda(tienda: str =Query(min_length=4,max_length=20),id: int =Query(ge=1 ,le=100))->List[Ventas]:
    db=sesion()
    resultado = db.query(Ventas_modelo).filter(Ventas_modelo.tienda==tienda).all()
    if not resultado:
        return JSONResponse(status_code= 404,content={'mensaje':'No se encontro la tienda'})
    else:
        return JSONResponse(status_code=200,content=jsonable_encoder(resultado))
    '''
    datos =[elemento for elemento in List_venta if elemento['tienda'] == tienda] #12
    print(datos)
    #return [elemento for elemento in List_venta if elemento['tienda'] == tienda] #4
    return JSONResponse(content=datos) #12
    '''

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
    db= sesion()
    resultado = db.query(Ventas_modelo).filter(Ventas_modelo.id==id).first()
    if not resultado:
        return JSONResponse(status_code=200, content={'mensaje':'No se pudo borrar'})
    else:
        db.delete(resultado)
        db.commit()
        return JSONResponse(status_code=200,content={'mensaje':'Se Elimino'})
    '''
    for element in List_venta:
        if element['id'] == id:
            List_venta.remove(element)
            return JSONResponse(content={'mensaje':'Se elimino sin inconvenientes'})
        #return List_venta
    return JSONResponse(content={'mensaje':'No se encontro'},status_code=200)
    '''
#uvicorn main:app --reload
#uvicorn main:app --reload --port 5000
#uvicorn main:app --reload --port 5000 --host 0.0.0.0