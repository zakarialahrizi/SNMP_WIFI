from pysnmp.hlapi import *
import time

#
SLEEP = 5
UNITE = "ko"
TRAFFIC = "both"

def run():

    # OID 1.10 = ifInOctets (download), 1.16 = ifOutOctets (upload)
    IFACE = 33
    OID_DOWN = f'.1.3.6.1.2.1.2.2.1.10.{IFACE}'
    OID_UP   = f'.1.3.6.1.2.1.2.2.1.16.{IFACE}'

    DIVISEUR = {"o": 1, "ko": 1024, "mo": 1024 * 1024}[UNITE]

    def get_value(oid):
        g = getCmd(
            SnmpEngine(),
            CommunityData('com', mpModel=1),
            UdpTransportTarget(('127.0.0.1', 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        errorIndication, errorStatus, errorIndex, varBinds = next(g)
        if errorIndication or errorStatus:
            return None
        return int(varBinds[0][1])

    #
    files = {}
    if TRAFFIC in ("download", "both"):
        files["down"] = open("debit_down.txt", "a")
    if TRAFFIC in ("upload", "both"):
        files["up"]   = open("debit_up.txt",   "a")

    ancienne_down = ancienne_up = None
    first = True

    while True:
        actuelle_down = get_value(OID_DOWN) if TRAFFIC in ("download", "both") else None
        actuelle_up   = get_value(OID_UP)   if TRAFFIC in ("upload",   "both") else None

        if not first:
            if actuelle_down is not None and ancienne_down is not None:
                debit = (actuelle_down - ancienne_down) / DIVISEUR / SLEEP
                print(f"Download : {debit:.2f} {UNITE}/s")
                files["down"].write(f"{debit}\n")
                files["down"].flush()

            if actuelle_up is not None and ancienne_up is not None:
                debit = (actuelle_up - ancienne_up) / DIVISEUR / SLEEP
                print(f"Upload   : {debit:.2f} {UNITE}/s")
                files["up"].write(f"{debit}\n")
                files["up"].flush()
        else:
            first = False
            print(f"(Première mesure - attente de {SLEEP}s pour calculer le débit)")

        ancienne_down = actuelle_down
        ancienne_up   = actuelle_up
        time.sleep(SLEEP)