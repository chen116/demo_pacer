from pyxs import Client
import subprocess





domU_mac = 0
with Client() as c:
	domU_mac = (c[b"/local/domain/23/device/vif/0/mac"]).decode()
# ip n | grep '00:16:3e:6b:67:2e' | cut -d" " -f1

p1 = subprocess.Popen(["ip","n"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", domU_mac], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
domU_ip = p2.communicate()[0].decode().split()[0]
print(domU_ip)


domu_ids=[]
keys=['vid']
with Client(xen_bus_path="/dev/xen/xenbus") as c:
	if domu_ids==[]:
		for x in c.list('/local/domain'.encode()):
			domu_ids.append(x.decode())
		domu_ids.pop(0)
	for domuid in self.domu_ids:
		permissions = []
		permissions.append(('b'+'0').encode())
		permissions.append(('b'+domuid).encode())
		for key in keys:
			tmp_key_path = ('/local/domain'+'/'+domuid+'/'+key).encode()
			tmp_val = ('xenstore entry init').encode()
			c.write(tmp_key_path,tmp_val)
			c.set_perms(tmp_key_path,permissions)
			print('created',key,'for dom',domuid)



