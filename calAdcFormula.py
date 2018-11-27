
def get_vr(v1, v2, r1, r2):
   return (v2 + (r2/(r1+r2)) * (v1-v2)) * 1024/1.8 - 1

def get_v1(vr, v2, r1, r2):
    return ((1.8/1024) * ((r1+r2)/r2) * (vr+1)) - ((r1/r2)*v2)

par1 = [3.3, 0, 12, 8.25]
vr = get_vr(*par1)
par2 = [vr, par1[1], par1[2], par1[3]]
v1 = get_v1(*par2)

print(vr, v1)
