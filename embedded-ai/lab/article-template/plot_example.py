"""Recreate the article's separate illustrative plot; no TD model is implemented."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
a=np.loadtxt(root/'data'/'illustrative_trace.csv',delimiter=',',skiprows=1)
t,y=a[:,0],a[:,1]
error=y[:-1]-y[1:]
print('N =',len(error),'MSE =',np.mean(error**2),'MAE =',np.mean(abs(error)))
plt.rcParams.update({'font.family':'serif','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(6.2,2.3))
ax.plot(t,y,label='Observed illustrative signal',color='#203f59')
ax.plot(t[1:],y[:-1],'--',label='Persistence (previous observation)',color='#a56536')
ax.set(xlabel='Sample index',ylabel='Signal (arbitrary units)')
ax.legend(frameon=False,fontsize=8,loc='upper right');ax.grid(alpha=.15)
fig.savefig(root/'figures'/'illustrative_signal.pdf',bbox_inches='tight')
