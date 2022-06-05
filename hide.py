import os
import winreg

print("\nRUN AS ADMINISTRATOR")

HKLM = winreg.HKEY_LOCAL_MACHINE

BRAND = "Acer n4020"
DISK  = "KINGSTON SSD 500gb"
CPU   = "Intel i5-11400"
GRAPHICAL_ADAPTER = "Generic Graphics Adapter"


def reg_delete_key(hkey, reg):
    try:
        registry_key = winreg.OpenKey(hkey, reg, 0, winreg.KEY_ALL_ACCESS)
        if registry_key:
            winreg.DeleteKey(hkey, reg)
    except Exception as e:
        pass

def reg_write_value(hkey, reg, name, value, rtype):
    try:
        registry_key = winreg.OpenKey(hkey, reg, 0, winreg.KEY_ALL_ACCESS)
        if registry_key:
            winreg.SetValueEx(registry_key, name, 0, rtype, value)
    except Exception as e:
        pass

def reg_read_value(hkey, reg, name):
    try:
        registry_key = winreg.OpenKey(hkey, reg, 0, winreg.KEY_READ)
        if registry_key:
            value = winreg.QueryValueEx(registry_key, name)
            if value:
                winreg.CloseKey(registry_key)
                return value
            winreg.CloseKey(registry_key)
    except Exception as e:
        pass

def reg_enum_value(key, reg):
    hkey = winreg.OpenKeyEx(key, reg, 0, winreg.KEY_READ)
    values = []
    count = winreg.QueryInfoKey(hkey)[0]
    try:
        with hkey:
            for i in range(count):
                enum = winreg.EnumValue(hkey, i)
                values.append(enum)
    except Exception as e:
        pass
    return values

def reg_enum_key(key, reg):
    hkey = winreg.OpenKeyEx(key, reg, 0, winreg.KEY_READ)
    keys = []
    count = winreg.QueryInfoKey(hkey)[0]
    try:
        with hkey:
            for i in range(count):
                enum = winreg.EnumKey(hkey, i)
                keys.append(enum)
    except Exception as e:
        pass
    return keys

"""
    enumerate keys inside key, if key/name exists replace it
"""
def find_key_replace_value(hkey, key, name, old, new, rtype):
    try:
        val = reg_read_value(hkey, key, name)
        if val:
            if type(val) == tuple:
                if len(old) == 0 or str.__contains__(val[0], old):
                    reg_write_value(hkey, key, name, new, rtype)
            else:
                if len(old) == 0 or str.__contains__(val, old):      
                    reg_write_value(hkey, key, name, new, rtype)
        else:
            enum = reg_enum_key(hkey, key)
            for r in enum:
                key = f"{key}\\{r}"
                val = reg_read_value(hkey, key, name)
                if val:
                    if type(val) == tuple:
                        if len(old) == 0 or str.__contains__(val[0], old):
                            reg_write_value(hkey, key, name, new, rtype)
                    else:
                        if len(old) == 0 or str.__contains__(val, old):      
                            reg_write_value(hkey, key, name, new, rtype)
    except Exception as e:
        print(str(e))


find_key_replace_value(HKLM, "HARDWARE\\DESCRIPTION\\System", "SystemBiosVersion", "" ,[f'{BRAND}   - 1'], winreg.REG_MULTI_SZ)

find_key_replace_value(HKLM, "SYSTEM\\ControlSet001\\Enum\\SCSI\\Disk&Ven_VBOX&Prod_HARDDISK", "FriendlyName", "", DISK, winreg.REG_SZ)

find_key_replace_value(HKLM, "SYSTEM\\ControlSet001\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000", "DriverDesc", "VirtualBox Graphics Adapter (WDDM)", GRAPHICAL_ADAPTER, winreg.REG_SZ)

find_key_replace_value(HKLM, "SYSTEM\\ControlSet001\\Control\\Video\\{C42682FB-E508-11EC-B53B-806E6F6E6963}\\Video", "DeviceDesc", "VirtualBox Graphics Adapter (WDDM)", GRAPHICAL_ADAPTER, winreg.REG_SZ)

find_key_replace_value(HKLM, "SYSTEM\\ControlSet001\\Control\\Class\\{4d36e97d-e325-11ce-bfc1-08002be10318}\\0020", "DriverDesc", "VirtualBox Guest Device", "Generic Device", winreg.REG_SZ)

find_key_replace_value(HKLM, "SYSTEM\\ControlSet001\\Enum\\SCSI\\CdRom&Ven_VBOX&Prod_CD-ROM", "FriendlyName", "VBOX CD-ROM", "CD-ROM", winreg.REG_SZ)


path = "SYSTEM\\ControlSet001\\Enum\\PCI"
enum = reg_enum_key(HKLM, path)
for e in enum:
    find_key_replace_value(HKLM, f"{path}\\{e}", "Service",    "VirtualBox Guest Device", GRAPHICAL_ADAPTER, winreg.REG_SZ)
    find_key_replace_value(HKLM, f"{path}\\{e}", "DeviceDesc", "VirtualBox Graphics Adapter (WDDM)", GRAPHICAL_ADAPTER, winreg.REG_SZ)
    find_key_replace_value(HKLM, f"{path}\\{e}", "DeviceDesc", "VirtualBox Guest Device", GRAPHICAL_ADAPTER, winreg.REG_SZ)


path = "HARDWARE\\DESCRIPTION\\System\\CentralProcessor"
enum = reg_enum_key(HKLM, path)
for e in enum:
    p = f"{path}\\{e}"
    find_key_replace_value(HKLM, p, "ProcessorNameString", "", CPU, winreg.REG_SZ)


path = "SYSTEM\\ControlSet001\\Enum\\ACPI"
enum = reg_enum_key(HKLM, path)
for e in enum:
    p = f"{path}\\{e}"
    find_key_replace_value(HKLM, p, "FriendlyName", "", CPU, winreg.REG_SZ)

    _enum = reg_enum_key(HKLM, p)
    for _e in _enum:
        _p = f"{p}\\{_e}"
        find_key_replace_value(HKLM, _p, "FriendlyName", "", CPU, winreg.REG_SZ)


print("\nAfter you are done using vbox guest additions you should remove VirtualBox services and eject the CD drive")