**Tabla de contenidos**

.. contents::
   :local:

Descripción
===========

Con este módulo podrá vender certificaciones a través del portal web que instala el módulo de eventos.

Instalación
===========

El sistema usa `Blockcert <http://www.blockcerts.org/>`__

Deberá tener los siguientes repositorios clonados y accesibles por Odoo:

* `cert-tools <https://github.com/blockchain-certificates/cert-tools/>`__ rama master
* `cert-issuer <https://github.com/blockchain-certificates/cert-issuer>`__ rama v2

Se recomienda instalar ambas librerías en un entorno virtual distinto al de Odoo. Existen dependencias que presentan conflicto.

Para instalar 'cert-issuer' se procederá con el clonado del código fuente. Posteriormente se ejecutará el comando:

`python setup.py experimental --blockchain=ethereum`

Si el sistema presenta error en las dependencias edite el fichero <virtualenv>/site-packages/merkletools-1.0.2.dist-info/METADATA

Deberá localizar la definición de las dependencias y sustituir la existente por esta otra

`Requires-Dist: pysha3 (>=1.0.1)`

Configuración
=============

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

Peticiones / Errores conocidos
==============================

* Envío automático del certificado en formato json. Actualmente se envía la insignia de forma estándar. Por tanto, se deberá enviar de forma manual en dicho formato. El destino de los certificados es 'work_dir'
* Crear una página de acceso público para la validación de los certificados y así asegurar la veracidad del fichero
* Y mucho más . . .

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/aeodoo/blockchain/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/aeodoo/blockchain/issues/new?body=module:%20{{ addon_name }}%0Aversion:%20{{ branch }}%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======
* `Guadaltech <https://guadaltech.es/>`__

  * Fernando La Chica <fernandolachica@gmail.com>
