
from src.lib.eegLib import *
import seaborn as sns
import matplotlib.animation
# csv = genDataName(2,1,2)
csv = '../../'+MEDITATING_CSV
dfM = prepEEGdata(csv)
rd = dfM
NCOMP = 3

imfs = emd(rd.fp2.values, nIMF = NCOMP)
FPLOT = 20
XRAN = 1280
CMAP=plt.get_cmap('inferno').colors



def dynamicDataPlot():
    fig, ax = plt.subplots(nrows=NCOMP+1, sharex=True, sharey=True)
    fig.set_facecolor('xkcd:light blue')
    fig.set_size_inches(19.3, 10.91)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    fig.tight_layout()
    plt.style.use('seaborn-whitegrid')

    anim_running = True

    def onClick(event):
        nonlocal anim_running
        if anim_running:
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True

    def absanimate(i):
        nonlocal ax
        if i*FPLOT%XRAN ==0:
            for xes in plt.gcf().get_axes():
                xes.clear()
            plt.axhline(0, color='white')
            plt.xlim(rd.index[i*FPLOT], rd.index[i*FPLOT+XRAN-1])
            plt.ylim(-600, 600)
        plt.sca(ax[0])
        plt.plot(rd.index[i*FPLOT:i*FPLOT+FPLOT+1],rd.fp2[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color=CMAP[0],label='fp2 signal')
        if i*FPLOT%XRAN ==0:
            plt.legend(loc='upper right')
        for j in range(0, NCOMP):
            plt.sca(ax[j + 1])
            plt.plot(rd.index[i * FPLOT:i * FPLOT + FPLOT + 1],
                     imfs[j][int(i) * FPLOT:int(i + 1) * FPLOT + 1].tolist(),c=CMAP[(len(CMAP)-1)//(NCOMP+1)*(j+1)] ,label = 'imf '+str(j))
            if i * FPLOT % XRAN == 0:
                plt.legend(loc='upper right')


    fig.canvas.mpl_connect('key_press_event', onClick)
    anim = matplotlib.animation.FuncAnimation(fig, absanimate, frames=len(rd) // FPLOT, interval=FPLOT / 256,
                                             repeat=False)
    plt.show()

dynamicDataPlot()




