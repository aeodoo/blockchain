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
