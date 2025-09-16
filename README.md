# Sistema de Scouts Basado en Arquitectura MVC con API REST

para ejecutar el proyecto y evitar cualquier problema de compatibildad en futuros push se necesita crear un entorno virtual en python para django y otro para el vue

# Django API REST

para usar dijango como api rest usamos la libreria de API REST FRAMEWORK que nos permite convertir a django en una api que podemos consumir y hacer un CRUD en la base de datos.

# Vue como Cliente

para usar vue como cliente se tendra que usar consultar HTTP a la APi, para controlar la seguridad de estas solicitudes el API REST FRAMEWORK nos permite proteger ciertos comandos de HTTP para evitar usos mal debidos

# Como usarlo

1. Configura el Visual Studio Code para clonar el repositivo en una carpeta donde tengas el entorno virtual y cada vez que hagas un Fetch origin este se actualize a lo ultimo.
2. Ejecuta 'python -m ven [Nombre Del Entorno Virtual]'
3. Entra al entorno virtual
4. Ejecuta 'pip install -r requirements.txt'