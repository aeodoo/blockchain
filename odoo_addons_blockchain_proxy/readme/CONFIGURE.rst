Vaya a Ajustes -> Blockchain. Se indican las siguientes variables:

* Entorno: Elija entre Test o Producción
* Path para Blockcert: Directorio base. Dentro encontraremos los repositorios 'cert-tools' y 'cert-issuer'. Esta ruta debe ser accesible por Odoo. Se ejecutarán comandos python sobre ella.
* Carpeta datos: Destino de las plantillas de insignias en formato Open badges
    * A tener en cuenta. En el subdirectorio 'work_dir' se encontrarán los certificados firmados y enviados a la red Ethereum
* ID Emisor: Emisor del certificado en formato open badges
* Clave privada emisor
* Clave pública emisor
* URL Emisor: Se publicará un json que identifica a la agencia emisora de certificados. Este fichero será usado por la librería 'cert-verification' para comprobar la validez del mismo
* Límite gas: Blockcert recomienda un valor mayor a 25000
* Token para Etherscan: La librería puede usar muchas peticiones a este software de terceros y requerirá de un token para el correcto funcionamiento
