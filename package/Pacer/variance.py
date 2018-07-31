import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-hr", "--heavy", type=float, default=300, help="heavy-workload-frame-size")
ap.add_argument("-lr", "--light", type=float, default=150, help="light-workload-frame-size")
ap.add_argument("-p", "--period",type=float,default=300,help="video sequences")
ap.add_argument("-x", "--util",type=float,default=300,help="video sequences")
args = vars(ap.parse_args())


h=args["heavy"]
l=args["light"]
p=args["period"]
x=args["util"]
print('high')
print("best case fps:",1/ ((h-2*(p*x))/x+2*(p*x)))
print("worst case fps:",x/h)

print('low')
print("best case fps:",1/ ((l-2*(p*x))/x+2*(p*x)))
print("worst case fps:",x/l)


x=0.5
p=0.01
h=0.05
l=0.025

print("50%")
print('high')
print("best case fps:",1/ ((h-2*(p*x))/x+2*(p*x)))
print("worst case fps:",x/h)

print('low')
print("best case fps:",1/ ((l-2*(p*x))/x+2*(p*x)))
print("worst case fps:",x/l)



x=0.4
p=0.01
h=0.05
l=0.025


print("40%")
print('high')
print("best case fps:",1/ ((h-2*(p*x))/x+2*(p*x)))
print("worst case fps:",x/h)

print('low')
print("best case fps:",1/ ((l-2*(p*x))/x+2*(p*x)))
print("worst case fps:",x/l)

x=0.4
p=10
h=50
l=25

print("50%")
print('high')
print("best case fps:",((h-2*(p*x))/x+2*(p*x)))
print("worst case fps:",h/x)

print('low')
print("best case fps:", ((l-2*(p*x))/x+2*(p*x)))
print("worst case fps:",l/x)



