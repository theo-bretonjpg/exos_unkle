Hello !
 
To make this program work you will need a few commands in the terminal,

first off you need to activate the python environnement with :

exos_unkle\exos_unkle\exo-2\venv\Scripts\Activate.ps1

Then the uvicorn server :

uvicorn main:app --reload

Then load up the doc on a browser with :

http://localhost:8000/docs#/

WARNING(I was getting a bug with the create contract POST that even after a few days I wasn't able
to fix so the get client Contracts doesn t work as well)

