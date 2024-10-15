"""
Buscar en el comprobador de derechos de la SDS las identificaciones listadas en "comprobar.csv"
"""

# Cargar librerías
import rpa as r

# Carar archivo
print('Cargar archivo comprobar.csv')
Comprobar = r.load('comprobar.csv').splitlines()[1:]
print(len(Comprobar), ' filas cargadas')

# Iniciar robot
print('Iniciar robot')
r.init()

# Consultar cada registro de dfComprobar
for n, registro in enumerate(Comprobar, start=1):
    print('Registro', n, 'de', len(Comprobar), ':', registro)
    # Abrir comprobador
    r.url('https://appb.saludcapital.gov.co/Comprobadordederechos/Consulta.aspx')

    # Buscar identificación
    r.type('//*[@id="MainContent_txtNoId"]', '[clear]' + registro + '[enter]')
    r.timeout(10)

    # Validar si existe el registro en el comprobador
    for i in range(1, 11):
        # Verifica si se encontró
        if r.present('//*[@id="MainContent_cmdNuevaConsulta"]'):
            break        # Verifica si se encontró

        # Verifica si no se encontró
        if r.present('//*[@id="MainContent_lblError"]'):
            break
        
        # Esperar 1 segundo
        r.wait(1)

    # Verifica si se encontró
    if r.present('//*[@id="MainContent_grdSubsidiado"]/tbody/tr[1]/th[14]'):
        # Leer EPS-S
        epss = r.read('//*[@id="MainContent_grdSubsidiado"]/tbody/tr[2]/td[14]')

        # Leer Estado
        estado = r.read('//*[@id="MainContent_grdSubsidiado"]/tbody/tr[2]/td[16]')
        print('-', epss, estado)
        resultado = registro + ',' + epss + ',' + estado + '\n'
        r.write(resultado, 'comprobados_sds.csv')
    else:
        print('- Sin información')
        resultado = registro  + '\n'
        r.write(resultado, 'no_comprobados.csv')

# Cerrar robot
print('Cerrar robot')
r.close()