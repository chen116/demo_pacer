import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-hr", "--heavy", type=int, default=300, help="heavy-workload-frame-size")
ap.add_argument("-lr", "--light", type=int, default=150, help="light-workload-frame-size")
ap.add_argument("-p", "--period",type=int,help="video sequences")
ap.add_argument("-x", "--util",type=int,help="video sequences")
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
