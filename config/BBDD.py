import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



fichero = "../datos.sqllite"
#leemos el directorio actuaal del archivo de BD
direcctorio = os.path.dirname(os.path.realpath(__file__))
#direccion de la BBDD unido las 2 variables anteriores
ruta = f"sqlite:///{os.path.join(direcctorio,fichero)}"
#creamos el motor
motor = create_engine(ruta,echo=True)
#importamos una session pasandole el motor
sesion = sessionmaker(bind=motor)
#crear base para manejar tablas
base = declarative_base()
