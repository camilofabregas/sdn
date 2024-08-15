from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.addresses import IPAddr
import json
import pox.lib.packet as pkt

REGLAS_PATH = "./reglas.json"
# Descomentar para la demo sin reglas
# REGLAS_PATH = "./sin_reglas.json"


rules_file = open(REGLAS_PATH)
rules = json.load(rules_file)

config_file = open("./config.json")
config = json.load(config_file)
SWITCH_FIREWALL = config['switch_firewall']

log = core.getLogger()


def launch():
    log.info("Iniciando controlador POX")
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    # Para loguear los paquetes OpenFlow que llegan al controlador    
    # core.openflow.addListenerByName("PacketIn", _handle_PacketIn)


def _handle_ConnectionUp(event):
    log.info("[SWITCH dpid: %s] Conectado con exito al controlador", event.dpid)    

    # Solo configuramos el switch firewall seleccionado
    if event.dpid != SWITCH_FIREWALL:
        return

    log.info("[SWITCH dpid: %s] Configurando las reglas para este switch", event.dpid)

    block_communications = rules['block_communications'] or []
    block_messages = rules['block_messages'] or []

    for block_communication in block_communications:
        # Bloqueamos la ida
        block = of.ofp_match()
        block.nw_src = IPAddr(block_communication[0])
        block.nw_dst = IPAddr(block_communication[1])
        block.dl_type = 0x800

        flow_mod = of.ofp_flow_mod()
        flow_mod.match = block
        event.connection.send(flow_mod)

        # Bloqueamos la vuelta
        block = of.ofp_match()
        block.nw_src = IPAddr(block_communication[1])
        block.nw_dst = IPAddr(block_communication[0])
        block.dl_type = 0x800

        flow_mod = of.ofp_flow_mod()
        flow_mod.match = block
        event.connection.send(flow_mod)

    # Regla 1 y regla 2.
    for block_message in block_messages:
        block = of.ofp_match()
        block.dl_type = 0x800

        # configurar protocolo    
        if "protocol" in block_message.keys():
            if block_message['protocol'] == 'TCP':
                block.nw_proto = pkt.ipv4.TCP_PROTOCOL
            elif block_message['protocol'] == 'UDP':
                block.nw_proto = pkt.ipv4.UDP_PROTOCOL

        # configurar IPs            
        if "src_ip" in block_message.keys():
            block.nw_src = IPAddr(block_message['src_ip'])
        if "dest_ip" in block_message.keys():
            block.nw_dest = IPAddr(block_message['dest_ip'])

        # configurar puertos            
        if "src_port" in block_message.keys():
            block.tp_src = block_message['src_port']
        if "dest_port" in block_message.keys():
            block.tp_dst = block_message['dest_port']

        # agregar regla al switch            
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = block
        event.connection.send(flow_mod)

def _handle_PacketIn(event):
    log.info("[CONTROLADOR] Recibido paquete OpenFlow del switch con dpid %s", event.dpid)
