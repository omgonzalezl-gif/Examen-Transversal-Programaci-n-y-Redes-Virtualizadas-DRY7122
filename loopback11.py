from ncclient import manager

config = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">

  <interface>

   <Loopback>

    <name>11</name>

    <ip>

     <address>

      <primary>

       <address>11.11.11.11</address>

       <mask>255.255.255.255</mask>

      </primary>

     </address>

    </ip>

   </Loopback>

  </interface>

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

    router.edit_config(target="running", config=config)

    print("Loopback11 creada correctamente.")
