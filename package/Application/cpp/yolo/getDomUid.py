from pyxs import Client
with Client(xen_bus_path="/dev/xen/xenbus") as c:
	domu_id = c.read("domid".encode())
print(domu_id)