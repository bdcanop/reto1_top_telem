Funcionamiento:

Primero se suben los super peers (en consola se ejecuta y el único argumento que recibe por ahora para testear en local es el puerto en donde se va a ejecutar) luego en AWS no recibirá ningun argumento ya que correrá en maquinas diferentes con una IP diferente.

Cuando los super peer esten en linea se deben registrar con los otros super peer para que se conozcan, esto se puede hacer mediante un script pero por ahora se hace manualmente de la siguiente manera:

En Postman se hace la siguiente solicitud:

GET http://127.0.0.1:8080/register-superpeer
Body 
{
    "address":"127.0.0.1:8081"
}

Esto registra el super peer 8081 en el super peer 8080, se debe hacer una solicitud nuevamente para registrar el super peer 8082 por ejemplo.

Y esto se debe hacer nuevamente para los peer 8081 y 8082 con el fin de que se conozcan entre ellos.

Una vez esto realizado se puede hacer la conexión de cada peer en donde se va especificar lo siguiente al momento de subirlos:

python app.py [nombre del nodo] [numero de archivos a compartir] [host] [port]

por ejemplo

python app.py Diego 2 127.0.0.1:8080 8085

Aqui podriamos mapear el host a un nombre para que no sea tan dificl de estar copiando una direccion IP como argumento.

Podria quedar asi:

python app.py Diego 2 Colombia 8085

Esto conectaria el nodo Diego al super peer Colombia en donde Diego compartiria 2 archivos a traves del puerto 8085 (el puerto tampoco seria necesario si solo lanzo un super peer por maquina como usualmente ocurre).