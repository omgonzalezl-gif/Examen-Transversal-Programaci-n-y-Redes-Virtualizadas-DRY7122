from ncclient import manager

hostname = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>OMAR-MISAEL</hostname>
    </native>
</config>
"""

with manager.connect(
    host="192.168.56.108",
    port=830,
    username="cisco",
    password="cisco",
    hostkey_verify=False
) as router:

    router.edit_config(target="running", config=hostname)

    print("Hostname cambiado correctamente.")
