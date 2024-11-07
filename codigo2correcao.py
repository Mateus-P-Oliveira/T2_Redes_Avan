import sys
#import MySQLdb
import pymysql
pymysql.install_as_MySQLdb()  # Faz a substituição do MySQLdb pelo pymysql
import netifaces  # Para verificar as interfaces de rede
from scapy.all import sniff  # Para capturar pacotes de rede
from pysnmp.hlapi import *

import logging
import threading

# Configurando o logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RMONProbe:
    def __init__(self, interfaces):
        self.interfaces = interfaces
        self.BBDD = self.connect_db()
        logging.info(f"Monitoring interfaces: {', '.join(self.interfaces)}")

    def connect_db(self):
        try:
            return MySQLdb.connect(host="localhost", user="user", passwd="password", db="comunidades")
        except MySQLdb.Error as e:
            logging.error(f"Database connection error: {e}")
            sys.exit(1)

    def monitor_interfaces(self):
        threads = []
        for interface in self.interfaces:
            t = threading.Thread(target=self.sniff_interface, args=(interface,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def sniff_interface(self, interface):
        sniff(iface=interface, prn=self.process_packet, store=0)

    def process_packet(self, packet):
        # Extração e registro de detalhes do pacote
        logging.info(f"Packet captured on {packet.sniffed_on if hasattr(packet, 'sniffed_on') else 'unknown interface'}")
        # Armazena no banco de dados as informações de interesse
        cursor = self.BBDD.cursor()
        # Exemplificando com IP de origem e destino
        cursor.execute(
            "INSERT INTO packet_data (src_ip, dst_ip, protocol) VALUES (%s, %s, %s)",
            (packet[0][1].src, packet[0][1].dst, packet[0].proto if hasattr(packet[0], 'proto') else None)
        )
        self.BBDD.commit()

    def handle_snmp_request(self, oid, operation, value=None):
        logging.info(f"Handling SNMP request: {oid} with operation {operation}")
        if operation == 'get':
            return self.get_statistics() if oid == "1.3.6.1.2.1.16.1" else self.get_history()
        elif operation == 'set' and oid == "1.3.6.1.2.1.16.1":
            self.update_statistics(value)

    def get_statistics(self):
        logging.info("Fetching statistics data...")
        cursor = self.BBDD.cursor()
        cursor.execute("SELECT * FROM statistics")
        return cursor.fetchall()

    def get_history(self):
        logging.info("Fetching history data...")
        cursor = self.BBDD.cursor()
        cursor.execute("SELECT * FROM history")
        return cursor.fetchall()

    def update_statistics(self, value):
        logging.info(f"Updating statistics with value: {value}")
        cursor = self.BBDD.cursor()
        cursor.execute("UPDATE statistics SET value=%s WHERE id=1", (value,))
        self.BBDD.commit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: probe <interface1> <interface2> ...")
        sys.exit(1)

    interfaces = sys.argv[1:]
    rmon_probe = RMONProbe(interfaces)

    # Iniciar monitoramento das interfaces em threads
    rmon_probe.monitor_interfaces()
