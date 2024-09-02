Cuando se inician las instancias que soportan los super peer Systemd busca todos los servicios habilitados y arranca el servicio llamado `flaskapp.service` automaticamente.

Esto se hace porque los nodos hacen todas las peticiones a la siguiente URL:
`http://internet-facing-1575917799.us-east-1.elb.amazonaws.com:8080/`

Esto es el DNS del balanceador de cargas con el que cuenta la red. Allí se distribuye el registro de peers entre los super peers disponibles.

Como los super peers estan dentro de una VPC y no cuentan con una dirección IP pública, se automatizó la ejecución del programa dentro de cada instancia con este script.

Si llegase a fallar se puede entrar a una de las instancias de super peer que actua como bastión la cual posee una dirección IP pública asignada mediante una IP elastica de AWS y se ejecutan los siguientes comandos:

Para recargar Systemd: ` sudo systemctl daemon-reload `

Para iniciar el servicio de nuevo: ` sudo systemctl start flaskapp.service `

Para comprobar el estado del servicio: ` sudo systemctl status flaskapp.service `

Para ver los logs del servicio: ` journalctl -u flaskapp.service -f `

Superpeer1 - Direccion IP Privada: 10.0.1.225:8080 - Direccion IP Publica: 3.212.232.139
ssh -i "super-peer.pem" ubuntu@3.212.232.139

Superpeer2 - Direccion IP Privada: 10.0.1.174:8080 - Direccion IP Publica: 54.197.61.74
ssh -i "super-peer.pem" ubuntu@54.197.61.74

Superpeer3 - Direccion IP Privada: 10.0.1.165:8080 - Direccion IP Publica: 98.82.69.129
ssh -i "super-peer.pem" ubuntu@98.82.69.129

Superpeer4 - Direccion IP Privada: 10.0.1.216:8080 - Direccion IP Publica: 23.22.64.232
ssh -i "super-peer.pem" ubuntu@23.22.64.232
