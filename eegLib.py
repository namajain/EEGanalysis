import pandas
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
from pandas import Series
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf



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

    xmin = 0
    xmax = 80
    axes.set_xlim([xmin,xmax])
    ymin = 0
    ymax = 500000
    axes.set_ylim([ymin,ymax])
    axes.plot(np.abs(x), np.abs(yf))

    fig.set_size_inches(19.3, 10.91)

    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.title("FFT")

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    fig.tight_layout()
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
    df['diff1'] = df.fp2.diff()
    if show:
        plt.plot(df.index, df.fp2)
        plt.plot(resampledData.index, resampledData.fp2)
        plt.show()
    return resampledData
def resampleDataMax(df, timeFrame='16ms', show=False):
    resampledData = df.resample(timeFrame).max()
    df['diff1'] = df.fp2.diff()
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
    return 'Data/' + '{0:01d}'.format(patient) + '{0:01d}'.format(activity) + '{0:02d}'.format(trial) + '.csv'


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