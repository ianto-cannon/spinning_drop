#Ianto Cannon 2025 Dec 1. Plot the profile of a levitating spinning drop, photographed in Fauzia Wardani's gallery of fluid motion at APS DFD.
import numpy as np

def spinning_drop_profile_solver(capillary_len, rad_tip, z_tip, fname=None):
  #rad_tip/=capillary_len
  #z_tip/=capillary_len
  #capillary_len=1
  ds = 1e-5*capillary_len
  psi=0
  r=0
  z=z_tip
  Volume=0
  centroid=0
  if fname: adams_txt = open(fname, "w") 
  for i in range(int(1e6)):
    dr = ds * np.cos(psi)
    dz = ds * np.sin(psi)
    r += dr
    z -= dz
    dPsi = ds * (2/rad_tip + (z**2 -z_tip**2)/2/capillary_len**3 - np.sin(psi)/r)
    psi += dPsi
    Volume += np.pi*r**2*dz
    centroid += z*np.pi*r**2*dz
    if fname and not i%int(1e3):
      print(r, z, psi, dPsi, np.sin(psi)/r, file=adams_txt)
    #if psi>np.pi:break
    if dPsi<0 and psi<np.pi/2:break
  if fname: print('saved',fname,'iterations',i)
  centroid /= Volume
  return Volume, r, z, centroid, psi

def plot_drop_profile(folder, fname): 
  import matplotlib.pyplot as plt
  import os
  fig, ax = plt.subplots(1)
  for file in sorted(os.listdir(folder)):
    if 'txt' not in file: continue
    if fname not in file: continue
    with open(folder+file, encoding = 'utf-8') as f:
      df = np.loadtxt(f)
    if df.ndim<2: continue
  ax.plot(df[:,0]*1e3, df[:,1]*1e3, c='b')
  ax.plot(df[-1,0]*1e3, df[-1,1]*1e3, '+', c='b')
  ax.tick_params(which='both', direction='in', top=True, right=True)
  ax.set_xlabel('r [mm]')
  ax.set_ylabel('z [mm]')
  #ax.set_ylim([-1,1])
  #ax.set_xlim([0,.4])
  ax.set_aspect('equal', adjustable='box')
  print('savin ',fname+'.pdf')
  fig.savefig(fname+'.pdf', bbox_inches='tight', transparent=True, format='pdf')
  return

#Parameters
surf_tens = 72e-3 #N/m, surface tension
density = 1e3 #kg*m**-3 density difference between the drop and the surrounding air
rotation_speed = 2548 #rad/s rotation speed of the drop
capillary_len = (surf_tens / density / rotation_speed**2 ) **(1/3)
print('capillary_len',capillary_len,'m')

#Lengthscales of the drop
z_tip = 2*1.915e-4 #m distance of the tip from the axis of rotation
rad_tip = z_tip/10 #m radius of curvature at the tip
for r in range(10):
  Volume, r, z, centroid, psi = spinning_drop_profile_solver(capillary_len, rad_tip, z_tip, fname=f'data/spin{r:05}.txt')
  rad_tip += z/2
print('rad_tip',rad_tip)
plot_drop_profile('data/','spin')
