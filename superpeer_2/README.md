Cuando se inician las instancias que soportan los super peer Systemd busca todos los servicios habilitados y arranca el servicio llamado `flaskapp.service` automaticamente.

Esto se hace porque los nodos hacen todas las peticiones a la siguiente URL:
`http://internet-facing-1575917799.us-east-1.elb.amazonaws.com:8080/`

Esto es el DNS del balanceador de cargas con el que cuenta la red. Allí se distribuye el registro de peers entre los super peers disponibles.

Como los super peers estan dentro de una VPC y no cuentan con una dirección IP pública, se automatizó la ejecución del programa dentro de cada instancia con este script.

Si llegase a fallar se puede entrar a una de las instancias de super peer que actua como bastión la cual posee una dirección IP pública asignada mediante una IP elastica de AWS y se ejecutan los siguientes comandos:

Para recargar Systemd: `sudo systemctl daemon-reload`

Para iniciar el servicio de nuevo: `sudo systemctl start flaskapp.service`

Para comprobar el estado del servicio: `sudo systemctl status flaskapp.service`