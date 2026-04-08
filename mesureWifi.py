import sys
import os
import threading
import snmpgetwifi
import affichageWifi

#

sleep_input = input("Intervalle de mesure en secondes (défaut 5) : ").strip()
sleep_time = int(sleep_input) if sleep_input else 5

print("Unité de débit : o (octets/s)  |  ko (kilo-octets/s)  |  mo (méga-octets/s)")
unite_input = input("Unité (défaut ko) : ").strip().lower()
unite = unite_input if unite_input in ("o", "ko", "mo") else "ko"

print("Type de trafic : download  |  upload  |  both")
type_input = input("Type (défaut both) : ").strip().lower()
traffic_type = type_input if type_input in ("download", "upload", "both") else "both"

#

snmpgetwifi.SLEEP   = affichageWifi.SLEEP   = sleep_time
snmpgetwifi.UNITE   = affichageWifi.UNITE   = unite
snmpgetwifi.TRAFFIC = affichageWifi.TRAFFIC = traffic_type

t = threading.Thread(target=snmpgetwifi.run)
t.daemon = True
t.start()

affichageWifi.run() 