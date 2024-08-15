import sys
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.cli import CLI
import json
from topologia import Topologia


config_file = open('./config.json')
config = json.load(config_file)

CANT_SWITCHES = config['cant_switches']
SWITCH_FIREWALL = config['switch_firewall']


def create_mininet():
    print("\nCreando Topologia")
    topo = Topologia(CANT_SWITCHES)
    net = Mininet(topo, controller=RemoteController, switch=OVSSwitch)

    input("\nEnter para Iniciar Mininet")

    net.start()
    dumpNodeConnections(net.hosts)

    return net


def test_cli():
    print("\n[Iniciando TEST CLI]")
    net = create_mininet()

    input("\nEnter para Ejecutar pingall")
    net.pingAll()

    print("\nIniciando CLI")    
    CLI(net)
    net.stop()


def test_regla_1():
    print("\n[Iniciando TEST1]")
    net = create_mininet()

    input("\nEnter para Ejecutar iperf entre lh1 y rh2 en puerto 80")
    lh1, rh2 = net.get('lh1', 'rh2')
    net.iperf((lh1, rh2), port=80)
    
    print("\nIniciando CLI")
    CLI(net)

    net.stop()


def test_regla_2():
    print("\n[Iniciando TEST2]")
    net = create_mininet()

    input("\nEnter para Ejecutar iperf desde el lh1 en puerto 5001 y UDP")
    lh1, rh1 = net.get('lh1', 'rh1')
    net.iperf((lh1, rh1), l4Type='UDP', port=5001)

    print("\nIniciando CLI")    
    CLI(net)

    net.stop()


def test_regla_3():
    print("\n[Iniciando TEST3]")
    net = create_mininet()

    lh2, rh1 = net.get('lh2', 'rh1')

    input("\nEnter para Ejecutar PingAll")
    net.pingAll()

    input("\nEnter para Ejecutar iperf entre lh2 y rh1")
    net.iperf((lh2, rh1))

    print("\nIniciando CLI")    
    CLI(net)

    net.stop()

def test_regla_4():
    print("\n[Iniciando TEST1]")
    net = create_mininet()

    input("\nEnter para Ejecutar iperf entre lh1 y lh2 en puerto 80")
    lh1, lh2 = net.get('lh1', 'lh2')
    net.iperf((lh1, lh2), port=80)

    print("\nIniciando CLI")    
    CLI(net)

    net.stop()


def main():
    if SWITCH_FIREWALL > CANT_SWITCHES:
        print("ERROR: La cantidad de Switches no puede ser menor al numero de Switch Firewall")
        return
    elif CANT_SWITCHES < 1:
        print("ERROR: La cantidad de Switches no puede ser menor a 1")
        return
        
    if len(sys.argv) == 1:
        test_cli()
        return
    if sys.argv[1] == 'test1':
        test_regla_1()
    elif sys.argv[1] == 'test2':
        test_regla_2()
    elif sys.argv[1] == 'test3':
        test_regla_3()
    elif sys.argv[1] == 'test4':
        test_regla_4()
    else:
        test_cli()


if __name__ == '__main__':
    setLogLevel('info')
    main()
