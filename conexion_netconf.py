from ncclient import manager

router = manager.connect(
    host='192.168.56.108',
    port=830,
    username='cisco',
    password='cisco',
    hostkey_verify=False,
    look_for_keys=False,
    allow_agent=False
)

print(router.connected)
