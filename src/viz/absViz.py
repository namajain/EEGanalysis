from src.lib.eegLib import *
import seaborn as sns
import matplotlib.animation
# csv = genDataName(2,1,2)
csv = '../../'+MEDITATING_CSV
dfM = prepEEGdata(csv)
# rd = dfM
rd = dfM.abs()

# global rd, rdres




rrd = upEnvelope(rd)
rdres = upEnvelope(upEnvelope(rrd))
FPLOT = 10
XRAN = 1280


def absanimate(i):
    if i*FPLOT%XRAN ==0:
        for xes in plt.gcf().get_axes():
            xes.clear()
        plt.xlim(rd.index[i*FPLOT], rd.index[i*FPLOT+XRAN-1])
        plt.ylim(-100, 600)
    plt.plot(rd.index[i*FPLOT:i*FPLOT+FPLOT+1],rd.fp2[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='red')
    plt.plot(rdres.index[i*FPLOT:i*FPLOT+FPLOT+1],rdres.fp2[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='blue')
    # plt.plot(rd.index[i*FPLOT:i*FPLOT+FPLOT+1],rd.diff1[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='blue')

def dynamicDataPlot():
    fig, ax = plt.subplots()
    fig.set_size_inches(19.3, 10.91)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    fig.tight_layout()
    ani = matplotlib.animation.FuncAnimation(fig, absanimate, frames=len(rd) // FPLOT, interval=FPLOT / 256, repeat=False)
    plt.show()



dynamicDataPlot()