#Ianto Cannon 2025 Dec 1. Plot the profile of a levitating spinning drop, photographed in Fauzia Wardani's gallery of fluid motion at APS DFD.
import numpy as np

def spinning_drop_profile_solver(capillary_len, rad_tip, height, fname=None):
  rad_tip/=capillary_len
  height/=capillary_len
  capillary_len=1
  ds = 1e-3
  psi=0
  r=0
  z=height
  Volume=0
  centroid=0
  if fname: adams_txt = open(fname, "w") 
  for i in range(int(5/ds)):
    dr = ds * np.cos(psi)
    dz = ds * np.sin(psi)
    r += dr
    z -= dz
    dPsi = ds * (2/rad_tip + z**2/2/capillary_len**3 - np.sin(psi)/r)
    psi += dPsi
    Volume += np.pi*r**2*dz
    centroid += z*np.pi*r**2*dz
    if fname and not i%int(.01/ds):
      print(r, z, psi, dPsi, capillary_len, file=adams_txt)
    if psi>np.pi:break
  if fname: print('saved',fname,'iterations',i)
  centroid /= Volume
  return Volume, r, z, z-centroid, np.pi-psi

def plot_drop_profile(name, capillary_len): 
  import matplotlib.pyplot as plt
  fig, ax = plt.subplots(1)
  with open('data/spin.txt', encoding = 'utf-8') as f:
    df = np.loadtxt(f)
  ax.plot(df[0,0]*capillary_len*1e3, df[0,1]*capillary_len*1e3, '+', c='b')
  ax.plot(df[:,0]*capillary_len*1e3, df[:,1]*capillary_len*1e3, c='b')
  ax.tick_params(which='both', direction='in', top=True, right=True)
  ax.set_xlabel('r [mm]')
  ax.set_ylabel('z [mm]')
  ax.set_ylim([-1,1])
  ax.set_xlim([0,.4])
  ax.set_aspect('equal', adjustable='box')
  print('savin ',name)
  fig.savefig(name, bbox_inches='tight', transparent=True, format='pdf')
  return

#Parameters
surf_tens = 72e-3 #N/m, surface tension
density = 1e3 #kg*m**-3 density difference between the drop and the surrounding air
rotation_speed = 759 #rad/s rotation speed of the drop
capillary_len = (surf_tens / density / rotation_speed**2 ) **(1/3)
print('capillary_len',capillary_len,'m')

#Lengthscales of the drop
rad_tip = 5e-4 #m radius of curvature at the tip
height = 9.5e-4 #m distance of the tip from the axis of rotation

vol, height, centroid, *_ = spinning_drop_profile_solver(capillary_len, rad_tip, height, fname=f'data/spin.txt')
plot_drop_profile('data/spin.pdf', capillary_len)
