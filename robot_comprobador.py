"""
Buscar en el comprobador de derechos de la SDS las identificaciones listadas en "comprobar.csv"
"""

# Cargar librerías
import rpa as r

# Carar archivo
print('Cargar archivo comprobar.csv')
Comprobar = r.load('comprobar.csv').replace('""','').splitlines()[1:]
print(len(Comprobar), ' filas cargadas')

# Iniciar robot
print('Iniciar robot')
r.init(turbo_mode=True)
r.timeout(10)

# Validar si tiene credenciales
if r.load('credenciales.txt'):
    # Cargar credenciales
    Credenciales = r.load('credenciales.txt').splitlines()

    # Arbrir INICIAR SESION
    r.url('https://appb.saludcapital.gov.co/comprobadorDeDerechos/Login.aspx?ReturnUrl=%2fComprobadordederechos%2fConsulta')
    
    # Iniciar sesion
    r.type('//*[@id="MainContent_Login_UserName"]', '[clear]' + Credenciales[0])
    r.type('//*[@id="MainContent_Login_Password"]', '[clear]' + Credenciales[1])
    r.click('//*[@id="MainContent_Login_LoginButton"]')

# Consultar cada registro de dfComprobar
for n, registro in enumerate(Comprobar, start=1):
    print('Registro', n, 'de', len(Comprobar), ':', registro)
    # Abrir comprobador
    r.url('https://appb.saludcapital.gov.co/Comprobadordederechos/Consulta.aspx')

    # Buscar identificación
    r.type('//*[@id="MainContent_txtNoId"]', '[clear]' + registro.split(',')[0])
    r.click('//*[@id="MainContent_cmdConsultar"]')

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

    # Verifica si inició sesión
    if r.present('//*[@id="LoginName"]'):
        # Verifica si se encontró
        if r.present('//*[@id="MainContent_grdSubsidiado"]/tbody/tr[1]/th[15]'):
            # Leer EPS-S
            epss = r.read('//*[@id="MainContent_grdSubsidiado"]/tbody/tr[2]/td[15]')

            # Leer Estado
            estado = r.read('//*[@id="MainContent_grdSubsidiado"]/tbody/tr[2]/td[18]')
            print('-', epss, estado)
            resultado = registro + ',' + epss + ',' + estado + '\n'
            r.write(resultado, 'comprobados_sds.csv')
        else:
            # Validar si existe el registro en el comprobador por nombres

            # Abrir comprobador
            r.url('https://appb.saludcapital.gov.co/Comprobadordederechos/Consulta.aspx')

            # Buscar por nombres
            r.type('//*[@id="MainContent_txtPriApellido"]', '[clear]' + registro.split(',')[3])
            r.type('//*[@id="MainContent_txtSegApellido"]', '[clear]' + registro.split(',')[4])
            r.type('//*[@id="MainContent_txtPriNombre"]', '[clear]' + registro.split(',')[1])
            r.type('//*[@id="MainContent_txtSegNombre"]', '[clear]' + registro.split(',')[2])
            r.click('//*[@id="MainContent_cmdConsultar"]')
            
            # Verifica si se encontró
            if r.present('//*[@id="MainContent_grdSubsidiado"]/tbody/tr[1]/th[15]'):
                # Leer EPS-S
                epss = r.read('//*[@id="MainContent_grdSubsidiado"]/tbody/tr[2]/td[15]')

                # Leer Estado
                estado = r.read('//*[@id="MainContent_grdSubsidiado"]/tbody/tr[2]/td[18]')
                print('-', epss, estado)
                resultado = registro + ',' + epss + ',' + estado + '\n'
                r.write(resultado, 'comprobados_sds_nombres.csv')
            else:
                print('- Sin información')
                resultado = registro  + '\n'
                r.write(resultado, 'no_comprobados.csv')
    else:
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