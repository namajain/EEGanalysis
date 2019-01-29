import pandas
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
from pandas import Series
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import seaborn as sns
sns.set_style('white')
import pprint as pp
import scipy as sp
from scipy import signal
from scipy import interpolate

CLIPDOWN = -600
CLIPUP = 600

THINKING_CSV = 'Data/thinking.csv'
READING_CSV = 'Data/reading.csv'
MEDITATING_CSV = 'Data/meditating.csv'
MEDITATING2_CSV = 'Data/1002.csv'

FREQ = 256


def doFFTcsv(csv,show,save):
    df = prepEEGdata(csv)
    yf = scipy.fft(df.fp2.values)
    x = scipy.fftpack.fftfreq(yf.size, 1 / FREQ)

    fig, axes = plt.subplots()
    fig.set_size_inches(19.3, 10.91)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    fig.tight_layout()

    xmin = 0
    xmax = 80
    axes.set_xlim([xmin,xmax])
    ymin = 0
    ymax = 500000
    axes.set_ylim([ymin,ymax])
    axes.plot(np.abs(x), np.abs(yf))

    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.title("FFT")



    if save:
        plt.savefig(genImgLoc(csv), bbox_inches='tight',dpi = 100)
    if show:
        plt.show()

def doFFTdf(df):
    yf = scipy.fft(df.fp2.values)
    x = scipy.fftpack.fftfreq(yf.size, 1 / FREQ)

    fig, axes = plt.subplots()

    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.title("FFT")

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    fig.tight_layout()
    plt.show()

def prepEEGdata(csv):
    df = pandas.read_csv(csv)
    df = df.dropna(how='all', axis=1)
    df = df.rename(index=str, columns={'FP2-F4': 'fp2'})
    try:
        df = df[~df.fp2.str.contains("FP")]
    except AttributeError:
        pass
    df = df.astype(float)

    df.fp2 = df.fp2.clip(lower=CLIPDOWN, upper=CLIPUP)

    df['diff1'] = df.fp2.diff()
    df['diff2'] = df.diff1.diff()
    df = df[15*FREQ:(9*60+15)*FREQ]

    df = convertToDateIndexFromNum(df)

    return df

def convertToDateIndexFromNum(df):
    df = df.reset_index(drop=True)
    df['id'] = df.index
    df.index = df.index / FREQ
    df.index = pandas.to_datetime(df.index, unit='s')
    return df

def showHist(df):
    df.hist(column='fp2', bins=1000)
    plt.show()

# rd=resampleData(dfMed,'4ms', False)
def resampleData(df, timeFrame, show):
    resampledData = df.resample(timeFrame).mean()
    if show:
        plt.plot(df.index, df.fp2)
        plt.plot(resampledData.index, resampledData.fp2)
        plt.show()
    return resampledData

def resampleDataMax(df, timeFrame='16ms', show=False):
    resampledData = df.resample(timeFrame).max()
    if show:
        plt.plot(df.index, df.fp2)
        plt.plot(resampledData.index, resampledData.fp2)
        plt.show()
    return resampledData

def generateAcfPlots(df, ts = '20ms'):
    if ts is None:
        dfRes = df
    else:
        dfRes = resampleData(df, ts, False)
    # plot_pacf(dfMed.fp2,lags=40)
    # plot_pacf(dfMed2.fp2,lags=40)
    fig, ax = plt.subplots()
    plot_acf(df.fp2, lags=100, use_vlines=False, ax=ax, ls='solid')
    plot_acf(dfRes.fp2, lags=100, use_vlines=False, ax=ax, ls='solid')
    ax.legend(('4ms  - Original',ts+' - Downsampled'))
    pyplot.show()

def generateAcfPlotsDiff(df, ts = '20ms'):
    fig, ax = plt.subplots()
    plot_acf(df.diff1, lags=100, use_vlines=False, ax=ax, ls='solid')
    if ts is not None:
        dfRes = resampleData(df, ts, False)
        plot_acf(dfRes.diff1, lags=100, use_vlines=False, ax=ax, ls='solid')
        ax.legend(('4ms  - Original', ts + ' - Downsampled'))
    else:
        ax.legend(('4ms  - Original'))

    # plot_pacf(dfMed.fp2,lags=40)
    # plot_pacf(dfMed2.fp2,lags=40)

    pyplot.show()

    
def genDataName(patient,activity,trial):
    return '../../Data/' + '{0:01d}'.format(patient) + '{0:01d}'.format(activity) + '{0:02d}'.format(trial) + '.csv'


def genImgLoc(csvLoc):
    return 'Plots/All' + csvLoc[4:-4] + '.png'


def split_list(df, wanted_parts):
    length = df.shape[0]
    return [ df.iloc[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]


def plotFFT_split(splitList):
    for x in splitList:
        doFFTdf(x)
        plt.show()

def upEnvelope(inFrame):
    inFrame['ldr'] = inFrame.fp2 - inFrame.fp2.shift(1)
    inFrame['rdr'] = inFrame.fp2 - inFrame.fp2.shift(-1)
    inFrame = inFrame.dropna()
    rd2 = inFrame.drop(inFrame[(inFrame.ldr < 0) | (inFrame.rdr < 0)].index)
    rd2 = rd2[['fp2']]
    outFrame = resampleData(rd2, "3.906ms", False)
    outFrame = outFrame.interpolate(method='quadratic')
    return outFrame

def loEnvelope(inFrame):
    inFrame['ldr'] = inFrame.fp2 - inFrame.fp2.shift(1)
    inFrame['rdr'] = inFrame.fp2 - inFrame.fp2.shift(-1)
    inFrame = inFrame.dropna()
    rd2 = inFrame.drop(inFrame[(inFrame.ldr > 0) | (inFrame.rdr > 0)].index)
    rd2 = rd2[['fp2']]
    outFrame = resampleData(rd2, "3.906ms", False)
    outFrame = outFrame.interpolate(method='quadratic')
    return outFrame
###############EMD####################

def emd(x, nIMF=3, stoplim=.001):
    """Perform empirical mode decomposition to extract 'niMF' components out of the signal 'x'."""

    r = x
    t = np.arange(len(r))
    imfs = np.zeros(nIMF, dtype=object)
    for i in range(nIMF):
        r_t = r
        is_imf = False

        while not is_imf :
            # Identify peaks and troughs
            pks = sp.signal.argrelmax(r_t)[0]
            trs = sp.signal.argrelmin(r_t)[0]

            # Interpolate extrema
            pks_r = r_t[pks]
            fip = sp.interpolate.InterpolatedUnivariateSpline(pks, pks_r, k=3)
            pks_t = fip(t)

            trs_r = r_t[trs]
            fitr = sp.interpolate.InterpolatedUnivariateSpline(trs, trs_r, k=3)
            trs_t = fitr(t)

            # Calculate mean
            mean_t = (pks_t + trs_t) / 2
            mean_t = _emd_complim(mean_t, pks, trs)

            # Assess if this is an IMF (only look in time between peaks and troughs)
            sdk = _emd_comperror(r_t, mean_t, pks, trs)

            # if not imf, update r_t and is_imf
            if sdk < stoplim:
                is_imf = True
            else:
                r_t = r_t - mean_t

        imfs[i] = r_t
        r = r - imfs[i]

    return imfs


def _emd_comperror(h, mean, pks, trs):
    """Calculate the normalized error of the current component"""
    samp_start = np.max((np.min(pks), np.min(trs)))
    samp_end = np.min((np.max(pks), np.max(trs))) + 1
    return np.sum(np.abs(mean[samp_start:samp_end] ** 2)) / np.sum(np.abs(h[samp_start:samp_end] ** 2))


def _emd_complim(mean_t, pks, trs):
    samp_start = np.max((np.min(pks), np.min(trs)))
    samp_end = np.min((np.max(pks), np.max(trs))) + 1
    mean_t[:samp_start] = mean_t[samp_start]
    mean_t[samp_end:] = mean_t[samp_end]
    return mean_t
