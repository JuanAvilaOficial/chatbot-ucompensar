> [!NOTE]
Para poder ejecutar el proyecto es necesario tener instalado Node.js en su computadora y ejecutar los siguientes comandos: 

node --watch ./server/index.js
python Ubot.py

la aplicación se ejecutará en el puerto 3000 por defecto y para ver lo hay que poner en el navegador http://localhost:3000

> [!important]
# Para crear el .venv Importar el proyecto

# Para linux 

1. rm -rf .venv

2. python3 -m venv .venv

3. source .venv/bin/activate

# Para windows

1. Remove-Item -Recurse -Force .venv

2. python -m venv .venv

3. source .venv/bin/activate

ya debería estar listo para instalar las dependencias de python

con -> pip install {paquete}

`pip install Flask tensorflow pandas numpy scikit-learn keras keras_preprocessing`