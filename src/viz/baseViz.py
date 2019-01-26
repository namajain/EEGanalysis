from src.lib.eegLib import *
import seaborn as sns
import matplotlib.animation
# csv = genDataName(2,1,2)
csv = '../../'+MEDITATING_CSV
dfM = prepEEGdata(csv)
rd = dfM
rdres2 = upEnvelope(upEnvelope(rd))
rdres = loEnvelope(loEnvelope(rd))
rdiff=rdres2.sub(rdres.fp2,axis=0)
FPLOT = 10
XRAN = 1280




def dynamicDataPlot():
    fig, ax = plt.subplots()
    ax.set_facecolor('xkcd:light blue')
    fig.set_size_inches(19.3, 10.91)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    fig.tight_layout()
    plt.style.use('seaborn-darkgrid')

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
        if i*FPLOT%XRAN ==0:
            for xes in plt.gcf().get_axes():
                xes.clear()
            plt.axhline(0, color='white')
            plt.xlim(rd.index[i*FPLOT], rd.index[i*FPLOT+XRAN-1])
            plt.ylim(-600, 600)
        plt.plot(rdiff.index[i*FPLOT:i*FPLOT+FPLOT+1],rdiff.fp2[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='yellow',label='envelope difference')
        plt.plot(rd.index[i*FPLOT:i*FPLOT+FPLOT+1],rd.fp2[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='xkcd:dark gray',label='fp2 signal')
        plt.plot(rdres.index[i*FPLOT:i*FPLOT+FPLOT+1],rdres.fp2[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='blue',label='lower envelope')
        plt.plot(rdres2.index[i*FPLOT:i*FPLOT+FPLOT+1],rdres2.fp2[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='red',label='upper envelope')
        # plt.plot(rd.index[i*FPLOT:i*FPLOT+FPLOT+1],rd.diff1[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='blue')
        if i*FPLOT%XRAN ==0:
            plt.legend(loc='upper right')
    fig.canvas.mpl_connect('key_press_event', onClick)
    anim = matplotlib.animation.FuncAnimation(fig, absanimate, frames=len(rd) // FPLOT, interval=FPLOT / 256,
                                             repeat=False)
    plt.show()

dynamicDataPlot()
