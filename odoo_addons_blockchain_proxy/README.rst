Las dependencias de cert-issuer no están bien

https://community.blockcerts.org/t/merkletools-pysha-dependency-conflict/1107/2

Modifico la línea de /home/admingst/.local/lib/python3.8/site-packages/merkletools-1.0.2.dist-info/METADATA

Requires-Dist: pysha3 (>=1.0.1)


No puedo poner

"external_dependencies": {"python": ["cert-issuer==2.0.27", "cert-tools==3.0.0a2"]},
