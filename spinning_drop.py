#Ianto Cannon 2025 Dec 1. Plot the profile of a levitating spinning drop, photographed in Fauzia Wardani's gallery of fluid motion at APS DFD.
import numpy as np

def spinning_drop_profile_solver(capillary_len, rad_tip, z_tip, nodes, fname=None):
  ds = 1e-4*z_tip
  psi=0
  r=0
  z=z_tip
  Volume=0
  centroid=0
  if fname: adams_txt = open(fname, "w") 
  for i in range(int(1e5)):
    dr = ds * np.cos(psi)
    dz = ds * np.sin(psi)
    r += dr
    z -= dz
    dPsi = ds * (2/rad_tip + (z**2 -z_tip**2)/2/capillary_len**3 - np.sin(psi)/r)
    if psi < 0: break
    if psi > np.pi: break
    if (psi-np.pi/2)*(psi+dPsi-np.pi/2) < 0:
      nodes-=1
      if nodes==0: break
    psi += dPsi
    Volume += np.pi*r**2*dz
    centroid += z*np.pi*r**2*dz
    if fname and not i%int(1e2):
      print(r, z, psi, dPsi, np.sin(psi)/r, file=adams_txt)
  if fname: print('saved',fname,'iterations',i)
  centroid /= Volume
  return Volume, r, z, centroid, psi

def plot_drop_profile(folder, fname): 
  import matplotlib.pyplot as plt
  import os
  fig, ax = plt.subplots(1)
  for i, file in enumerate(reversed(sorted(os.listdir(folder)))):
    #if i > 1: break
    if 'txt' not in file: continue
    if fname not in file: continue
    with open(folder+file, encoding = 'utf-8') as f:
      df = np.loadtxt(f)
    if df.ndim<2: continue
    ax.plot(df[:,0], df[:,1], c='b')
    ax.plot(df[-1,0], df[-1,1], '+', c='b')
  ax.tick_params(which='both', direction='in', top=True, right=True)
  ax.set_xlabel('r [m]')
  ax.set_ylabel('z [m]')
  ax.set_aspect('equal', adjustable='box')
  print('savin ',fname+'.pdf')
  plt.show()
  fig.savefig(fname+'.pdf', bbox_inches='tight', transparent=True, format='pdf')
  return

surf_tens = 23.2e-3 #N/m, surface tension
density = 801 #kg*m**-3 density difference between the drop and the surrounding air
#brown_txt = open('data/brown.txt', "w") 
if True:#for om in range(1):
  rotation_speed = 13.48#om+1 #rad/s rotation speed of the drop
  capillary_len = ( surf_tens / density / rotation_speed**2 ) ** (1/3)
  z_tip = 1.18e-2 #m distance of the tip from the axis of rotation
  #rad_tip = z_tip/10 #m radius of curvature at the tip
  rad_min = z_tip/10 #m radius of curvature at the tip
  rad_max = z_tip/2 #m radius of curvature at the tip
  for t in range(50):
    #rad_tip = rad_min + (rad_max-rad_min)*t/100
    rad_tip = (rad_max + rad_min)/2
    Volume, rad_neck, z, centroid, psi = spinning_drop_profile_solver(capillary_len, rad_tip, z_tip, 1)
    if psi < 0: rad_max = rad_tip
    elif psi > np.pi: rad_max = rad_tip
    elif z>0: rad_min = rad_tip
    else: rad_max = rad_tip
    #rad_tip += z/50
  Volume, rad_neck, z, centroid, psi = spinning_drop_profile_solver(capillary_len, rad_min, z_tip, 1, fname=f'data/spin_min.txt')
  Volume, rad_neck, z, centroid, psi = spinning_drop_profile_solver(capillary_len, rad_max, z_tip, 1, fname=f'data/spin_max.txt')
  plot_drop_profile('data/','spin')
  print('rotation_speed',rotation_speed,'capillary_len',capillary_len,'rad_tip',rad_tip)
  #Volume, rad_neck, z, centroid, psi = spinning_drop_profile_solver(capillary_len, rad_tip, z_tip, fname=f'data/spin{om:03}.txt')
  #size = (2*3*Volume/4/np.pi)**(1/3) #m radius of drop if it were spherical
  #print( rotation_speed*(density*size**3/8/surf_tens)**.5, 2*z_tip/size, file=brown_txt)
