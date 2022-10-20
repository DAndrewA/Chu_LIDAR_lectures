import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec as GS

t = np.array(range(400))
r = np.sin(t/50)

fig = plt.figure(figsize=(18,8))

gs = GS.GridSpec(1,2, width_ratios=[1,3])

ax = fig.add_subplot(gs[0])
ax.plot(t,r)
ax = fig.add_subplot(gs[1])
ax.plot(t,r)


plt.show()

# also consider subplot_mosaic?