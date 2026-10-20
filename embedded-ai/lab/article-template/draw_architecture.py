"""Recreate the vector architecture illustration; not executable model code."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
root=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'serif','font.size':10})
fig,ax=plt.subplots(figsize=(6.5,1.65));ax.axis('off')
labels=['Window\n16 × 3','Temporal mix\n16 → 8 → 16','Feature mix\n3 → 8 → 3','Linear head\n48 → 1']
for i,label in enumerate(labels):
    x=.01+i*.255
    ax.add_patch(FancyBboxPatch((x,.3),.21,.47,boxstyle='round,pad=0.012',facecolor='#eef2f4',edgecolor='#677a86',linewidth=.8))
    ax.text(x+.105,.535,label,ha='center',va='center',fontsize=9)
    if i<3:ax.annotate('',xy=(x+.247,.535),xytext=(x+.22,.535),arrowprops={'arrowstyle':'->','color':'#677a86'})
ax.text(.5,.08,'Residual additions in both mixing stages; train on PC, infer on the board.',ha='center',fontsize=8)
fig.savefig(root/'figures'/'architecture.pdf',bbox_inches='tight')
