import pandas
import matplotlib.animation
import matplotlib.pyplot as plt


class emdVizBlit():

    def __init__(self, rd=None, csv=None, ncomp=5, fplot=20, xran=128, fa=.8):
        self.rd = [1] * 10000
        self.nComp = ncomp
        self.nPoints = fplot
        self.xRange = xran
        self.cMap = plt.get_cmap('inferno').colors
        self.freqAdjust = fa

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

        lines = [getLine(axe) for axe in ax]
        anim_running = True

        def absanimate(i):
            nonlocal ax

            # if isRedrawIter(i):
            # redrawPlotOutline(i)

            # plotBaseSignal(i)
            # plotImfSignal(i)
            # plotResidueSignal(i)
            return lines

        anim = matplotlib.animation.FuncAnimation(fig, absanimate, frames=len(self.rd) // self.nPoints,
                                                  interval=self.nPoints / 256 * self.freqAdjust,
                                                  repeat=False, blit=True)
        plt.show()


if __name__ == '__main__':
    ev = emdVizBlit()
    ev.emdPlot()
