"""O que preciso fazer?
criar um client GATT com o endereço random? Apenas conectar não parece dar certo, talvez seja preciso GATT client :(
Conectar a BSN. Tem como conectar com random!!!!! Talvez não precisa criar um client GATT !!!
Notoficar todos as caracteristicas relevantes
Salvar em um arquivo
"""

from gi.repository import GLib

import dbus
import sys
import bluetooth_utils
import bluetooth_constants
#import client_discover_devices
import time

sys.path.insert(0, '.')

# Variaveis globais?
bus = None  # por que isso??? La em baixo ele jogar o SystemBus aqui
device_interface = None  # e isso, o que faz?

# UUIDs da BSN
SERVICE_OF_CONFIGURATION = "e40f0300-1fbf-11e8-b467-0ed5f89f718b"
SERVICE_OF_DATA_UUID = "e40f0400-1fbf-11e8-b467-0ed5f89f718b"
EULER_ANGLES_UUID = "e40f0403-1fbf-11e8-b467-0ed5f89f718b"
PARAMETRO_CONEXAO = "e40f0303-1fbf-11e8-b467-0ed5f89f718b"
BUSSULA_UUID = "e40f0405-1fbf-11e8-b467-0ed5f89f718b"
MAC_DA_GATO = "CA:DB:17:8A:02:97"
PATH_DA_BSN = "/org/bluez/hci0/dev_CA_DB_17_8A_02_97"

# Constantes copiadas do tutorial. Colocando aqui para ajudar na compreensão

ADAPTER_NAME = "hci0"

BLUEZ_SERVICE_NAME = "org.bluez"
BLUEZ_NAMESPACE = "/org/bluez/"
DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'

ADAPTER_INTERFACE = BLUEZ_SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = BLUEZ_SERVICE_NAME + ".Device1"
GATT_MANAGER_INTERFACE = BLUEZ_SERVICE_NAME + ".GattManager1"
GATT_SERVICE_INTERFACE = BLUEZ_SERVICE_NAME + ".GattService1"
GATT_CHARACTERISTIC_INTERFACE = BLUEZ_SERVICE_NAME + ".GattCharacteristic1"
GATT_DESCRIPTOR_INTERFACE = BLUEZ_SERVICE_NAME + ".GattDescriptor1"
ADVERTISEMENT_INTERFACE = BLUEZ_SERVICE_NAME + ".LEAdvertisement1"
ADVERTISING_MANAGER_INTERFACE = BLUEZ_SERVICE_NAME + ".LEAdvertisingManager1"


# codigo

def connect():
    global bus
    global device_interface
    try:
        device_interface.Connect()
    except Exception as e:
        print("Failed to connect")
        print(e.get_dbus_name())
        print(e.get_dbus_message())
        if ("UnknownObject" in e.get_dbus_name()):
            print("Try scanning first to resolve this problem")
        return bluetooth_constants.RESULT_EXCEPTION
    else:
        print("Connected OK")
        return bluetooth_constants.RESULT_OK


def connect_profile(uuid):
    global bus
    global device_interface
    try:
        print(device_interface.ConnectProfile(uuid))
        # device_interface.ConnectProfile(uuid)
    except Exception as e:
        print("Deu errado")
        print(e.get_dbus_name())
        print(e.get_dbus_message())


# bdaddr = sys.argv[1] #pega o argumento da linha de comando. Usar o MAC_DA_GATO
bus = dbus.SystemBus()

gato_proxy = bus.get_object(BLUEZ_SERVICE_NAME, PATH_DA_BSN)  # criando um proxy object da bsn
device_interface = dbus.Interface(gato_proxy, DEVICE_INTERFACE)  # criando uma interface do Device1
device_properties_interface = dbus.Interface(gato_proxy, DBUS_PROPERTIES)  # criando uma interface do Properties

adapter_path = bluetooth_constants.BLUEZ_NAMESPACE + bluetooth_constants.ADAPTER_NAME

# acquire the adapter interface so we can call its methods
adapter_object = bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME, adapter_path)
adapter_interface = dbus.Interface(adapter_object, bluetooth_constants.ADAPTER_INTERFACE)

print("Connecting to " + PATH_DA_BSN)
connect()
what = bluetooth_utils.dbus_to_python(device_properties_interface.Get(DEVICE_INTERFACE, 'ManufacturerData'))
print("Printando o what")
print(what)
# time.sleep(30)
# connect_profile(SERVICE_OF_DATA_UUID)
