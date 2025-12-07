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
    if fname and not i%int(1e2):
      print(r, z, psi, dPsi, np.sin(psi)/r, file=adams_txt)
    psi += dPsi
    if fname:
      if z < -z_tip: break
    else:
      if (psi-np.pi/2)*(psi-dPsi-np.pi/2) < 0:
        nodes-=1
        if nodes==0: break
    if psi < 0: break
    if psi > np.pi: break
    Volume += np.pi*r**2*dz
    centroid += z*np.pi*r**2*dz
  if fname: print('saved',fname,'iterations',i)
  centroid /= Volume
  return Volume, r, z, centroid, psi, dPsi

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
    ax.plot(df[:,0], df[:,1], c='b')
  ax.tick_params(which='both', direction='in', top=True, right=True)
  ax.set_xlabel('r [m]')
  ax.set_ylabel('z [m]')
  ax.set_aspect('equal', adjustable='box')
  print('savin ',fname+'.pdf')
  fig.savefig(fname+'.pdf', bbox_inches='tight', transparent=True, format='pdf')
  return

#Parameters
surf_tens = 23.2e-3 #N/m, surface tension
density = 801 #kg*m**-3, density difference between the drop and the surrounding air
z_tip = 1.18e-2 #m, distance of the tip from the axis of rotation
nodes = 1 # 1,2,3,4..., dimensionless, number of times the profile is parallel to the z axis for z>0

brown_txt = open('data/brown.txt', 'a') 
for r in range(20):
  rotation_speed = .10 + r #rad/s, rotation speed of the drop
  #rotation_speed = 20 + 2*r #rad/s, rotation speed of the drop
  #rotation_speed = 11.5 + .05*r #rad/s, rotation speed of the drop
  #Use bisection to find rad_tip that centres the drop at z=0
  capillary_len = ( surf_tens / density / rotation_speed**2 ) ** (1/3)
  rad_min = z_tip/10
  rad_max = z_tip*2
  for t in range(20):
    rad_tip = (rad_max + rad_min)/2
    Volume, rad_neck, z, centroid, psi, dPsi = spinning_drop_profile_solver(capillary_len, rad_tip, z_tip, nodes)
    if psi < 0: rad_max = rad_tip
    elif psi > np.pi: rad_max = rad_tip
    elif z > 0: rad_min = rad_tip
    else: rad_max = rad_tip
  #if (psi-np.pi/2)*(psi-dPsi-np.pi/2) > 0: break
  #if z**2 > capillary_len**2: break
  if z**2 > (.01*z_tip)**2: break
  #if z > 0: break
  #if psi < 0: break 
  #if psi > np.pi: break
  Volume, rad_neck, z, centroid, psi, dPsi = spinning_drop_profile_solver(capillary_len, rad_min, z_tip, nodes, fname=f'data/spin{r:03}.txt')
  size = (3*Volume/4/np.pi)**(1/3) #m radius of drop if it were spherical
  print( rotation_speed*(density*size**3/8/surf_tens)**.5, z_tip/size, file=brown_txt)
  print( r, rotation_speed*(density*size**3/8/surf_tens)**.5, z_tip/size)
plot_drop_profile('data/','spin')
