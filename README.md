# RPA-TagUI-Comprobador-SDS
Robot para usar el comprobador de derechos de la Secretaría Distrital de Salud usando TagUI (rpa) en Python

Lee cada registro del archivo comprobar.csv y lo verifica en el comprobador https://appb.saludcapital.gov.co/Comprobadordederechos/Consulta generando los archivos comprobados_sds.csv y no_comprobados.csv

Opcional, si cuenta con credenciales del comprobador en el archivo credenciales.txt, realiza una busqueda adicional por nombres

En la carpeta test se cargan los archivos de ejemplo y el ejecutable del robot