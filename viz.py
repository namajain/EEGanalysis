from eegLib import *
import seaborn as sns
import matplotlib.animation
# csv = genDataName(2,1,2)
csv = MEDITATING_CSV
dfM = prepEEGdata(csv)
rd = dfM
# rd = dfM.abs()
# rd=resampleDataMax(dfM.abs(),'32ms', False)
FPLOT = 10
XRAN = 1280
def animate(i):
    # print(rd.index[int(i):int(i+2)].tolist())
    if i*FPLOT%XRAN ==0:
        plt.gcf().clear()
        plt.xlim(rd.index[0], rd.index[XRAN])
        plt.ylim(-600, 600)
        print("CLEEEER")
    # print(i)
    plt.plot(rd.index[i*FPLOT%XRAN:i*FPLOT%XRAN+FPLOT+1],rd.fp2[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='red')
    # plt.plot(rd.index[i*FPLOT%XRAN:i*FPLOT%XRAN+FPLOT+1],rd.diff1[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='blue')

def absanimate(i):
    # print(rd.index[int(i):int(i+2)].tolist())
    if i*FPLOT%XRAN ==0:
        plt.gcf().clear()
        plt.xlim(rd.index[0], rd.index[XRAN])
        plt.ylim(-600, 600)
        print("CLEEEER")
    # print(i)
    plt.plot(rd.index[i*FPLOT%XRAN:i*FPLOT%XRAN+FPLOT+1],rd.fp2[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='red')
    # plt.plot(rd.index[i*FPLOT%XRAN:i*FPLOT%XRAN+FPLOT+1],rd.diff1[int(i)*FPLOT:int(i+1)*FPLOT+1].tolist(),color='blue')


def dynamicDataPlot():
    fig, ax = plt.subplots()
    fig.set_size_inches(19.3, 10.91)
    fig.tight_layout()
    plt.xlim(rd.index[0], rd.index[XRAN])
    plt.ylim(-100, 600)
    ani = matplotlib.animation.FuncAnimation(fig, animate, frames=len(rd) // FPLOT, interval=FPLOT / 256, repeat=False)
    plt.show()


dynamicDataPlot()
#
# generateAcfPlotsDiff(rd,ts= None)