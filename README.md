# Introducción a los Sistemas Distribuidos (75.43) - TP N◦2: Software-Defined Networks

## Grupo B4 - Integrantes:

| Alumno                                                      | Padrón |
| ----------------------------------------------------------- | ------ |
| [Camila Fernández Marchitelli](https://github.com/camifezz) | 102515 |
| [Lucas Aldazabal](https://github.com/LucasAlda)             | 107705 |
| [Bautista Boselli](https://github.com/BautistaBoselli)      | 107490 |
| [Alejo Fábregas](https://github.com/alejofabregas)          | 106160 |
| [Camilo Fábregas](https://github.com/camilofabregas)        | 103740 |

## Resumen

El objetivo del trabajo práctico es la construcción de una topología dinámica y parametrizable, utilizando el protocolo OpenFlow para poder implementar un Firewall a nivel de capa de enlace. Para poder plantear este escenario se emulará el comportamiento de la topología a través de mininet.

## Iniciar POX
Ejecutar los siguientes comandos antes de iniciar mininet:
```
> cp firewall.py [PATH_POX]/pox/misc/firewall.py

En una terminal en el directorio del proyecto
```

```
> ./pox/pox.py log.level forwarding.l2_learning misc.firewall

En una terminal en el directorio del proyecto
```


## Iniciar Mininet

```
> sudo python3 scripts.py [cli|test1|test2|test3|test4]

En una terminal en el directorio del proyecto
```



## Configuración Topología

La topologia consiste en una hilera de N switches con dos hosts conectados al de mas a la derecha (lh1 y lh2) y dos hosts al de mas a la izquierda (rh1 y rh2)

- LH1: IP 10.10.10.1
- LH2: IP 10.10.10.2
- RH1: IP 10.10.11.1
- RH2: IP 10.10.11.2

Los N switches se configuran con el parametro `cant_switches` en el archivo `config.json`. Cada switch tiene como dpid el numero de switch que es, por ejemplo el switch 1 tiene como dpid 1.

Con el parametro `switch_firewall` se configura el switch que va a tener el firewall, por ejemplo si se configura con 3, el switch 3 va a ser el firewall.

Ejemplo:

```json
{
  "cant_switches": 10,
  "switch_firewall": 3
}
```

## Reglas

Las reglas se configuran en el archivo reglas.json, hay dos tipos de reglas: comunicaciones entre hosts y tipos de paquetes.

### Comunicaciones entre hosts

Se configuran con una lista de tuplas de hosts que no pueden comunicarse entre sí. Por ejemplo:

```json
{
  "block_communications": [["10.10.10.1", "10.10.11.2"]],
  "block_messages": []
}
```

### Comunicaciones de paquetes

Se configuran con una lista de reglas con los siguientes campos:

| Nombre    | Descripción                     | Requerido |
| --------- | ------------------------------- | --------- |
| protocol  | protocolo del mensaje (UDP/TCP) | Si        |
| src_ip    | IP de origen                    | No        |
| dest_ip   | IP de destino                   | No        |
| src_port  | Puerto de origen                | No        |
| dest_port | Puerto de destino               | No        |

Por ejemplo:

```json
{
  "block_communications": [],
  "block_messages": [
    {
      "protocol": "UDP", // requerido
      "src_ip": "10.10.10.1",
      "dest_ip": "10.10.11.2",
      "src_port": 4000,
      "dest_port": 80
    }
  ]
}
```

## Scripts

### Acceder a CLI (Default)
Hace un pingall y luego se accede a la CLI de mininet.
```
> sudo python3 scripts.py cli
```
### Test regla 1
Ejecutar un iperf entre lh1 y rh2 en el puerto 80 para validar que se descartan todos los mensajes con puerto destino 80.
```
> sudo python3 scripts.py test1
```
### Test regla 2
Ejecutar un iperf desde lh1 en puerto 5001 y UDP para validar que se descartan todos los mensajes que provengan del host 1, tengan como puerto destino el 5001, y esten utilizando el protocolo UDP.
```
> sudo python3 scripts.py test2
```
### Test regla 3
Ejecutar iperf entre lh2 y rh1 para validar que dados dos hosts cualquiera (configurables via reglas) no se puedan comunicar de ninguna forma.
```
> sudo python3 scripts.py test3
```
### Test hosts mismo lado
Ejecutar iperf entre lh1 y lh2 para ver que dos hosts del mismo lado pueden comunicarse entre sí por puerto 80 (prohibido por regla 1) dependiendo del switch_firewall del config.json:
- si el switch_firewall es el 1 (switch del extremo donde conectan estos hosts): La regla 1 prohíbe la comunicación
- si el switch_firewall es cualquier otro: Se pueden comunicar por no pasar por el firewall
```
> sudo python3 scripts.py test4
```


