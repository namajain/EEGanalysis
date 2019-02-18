from src.lib.eegLib import *
import seaborn as sns
import matplotlib.animation


class emdVizBlit():

    def __init__(self, rd=None, csv=None, ncomp=5, fplot=20, xran=128,fa=.8):
        if rd is not None:
            self.rd = rd
        elif csv is not None:
            self.rd = prepEEGdata(csv)
        else:
            self.rd = prepEEGdata('../../' + MEDITATING_CSV)
        self.nComp = ncomp
        self.nPoints = fplot
        self.xRange = xran
        self.cMap = plt.get_cmap('inferno').colors
        self.imfs, self.residue = emd(self.rd.fp2.values, nIMF=ncomp)
        self.freqAdjust=fa

    def emdPlot(self):
        fig, ax = plt.subplots(nrows=self.nComp + 2, sharex=True, sharey=True)
        fig.set_facecolor('xkcd:light blue')
        fig.set_size_inches(19.3, 10.91)
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        fig.tight_layout()
        plt.style.use('seaborn-whitegrid')

        def getColor(j):
            return self.cMap[(len(self.cMap) - 1) // (self.nComp + 2) * (j)]
        def getLine(axe):

            ln, = axe.plot([], [], color=getColor(0), animated=True)
            return ln
        lines=[getLine(axe) for axe in ax]
        anim_running = True

        def absanimate(i):
            nonlocal ax

            if isRedrawIter(i):
                redrawPlotOutline(i)

            plotBaseSignal(i)
            plotImfSignal(i)
            plotResidueSignal(i)
            return lines

        def onClick(event):
            nonlocal anim_running
            if anim_running:
                anim.event_source.stop()
                anim_running = False
            else:
                anim.event_source.start()
                anim_running = True

        def isRedrawIter(i):
            return i % self.xRange == 0

        def plotBaseSignal(i):
            nonlocal ax

            # plt.sca(ax[0])
            lines[0].set_data(self.rd.index[0:i * self.nPoints + self.nPoints + 1],
                     self.rd.fp2[0:int(i + 1) * self.nPoints + 1].tolist())

            if isRedrawIter(i):
                ax[0].legend(['FP2 Signal'])
            # drawLegend(i)


        def drawLegend(i):
            if isRedrawIter(i):
                plt.legend(loc='upper right')



        def plotResidueSignal(i):
            nonlocal ax
            # plt.sca(ax[self.nComp + 1])
            lines[self.nComp + 1].set_data(self.rd.index[:i * self.nPoints + self.nPoints + 1],
                     self.residue[:int(i + 1) * self.nPoints + 1].tolist())
            if isRedrawIter(i):
                ax[self.nComp + 1].legend(['Residue'])

        def plotImfSignal(i):
            nonlocal ax
            for j in range(0, self.nComp):
                lines[j+1].set_data(self.rd.index[:i * self.nPoints + self.nPoints + 1],
                         self.imfs[j][:int(i + 1) * self.nPoints + 1].tolist())
                if isRedrawIter(i):
                    ax[j+1].legend(['IMF ' + str(j)])



        def redrawPlotOutline(i):
            for xes in plt.gcf().get_axes():
                xes.clear()
            plt.axhline(0, color='white')
            plt.xlim(self.rd.index[i * self.nPoints], self.rd.index[(i + self.xRange )* self.nPoints - 1])
            plt.ylim(-600, 600)

        fig.canvas.mpl_connect('key_press_event', onClick)
        anim = matplotlib.animation.FuncAnimation(fig, absanimate, frames=len(self.rd) // self.nPoints,
                                                  interval=self.nPoints / 256*self.freqAdjust,
                                                  repeat=False,blit=True)
        plt.show()


if __name__ == '__main__':
    ev = emdVizBlit()
    ev.emdPlot()
