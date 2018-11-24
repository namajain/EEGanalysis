import pandas
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt

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

def resampleData(df, timeFrame, show):
    resampledData = pandas.DataFrame()
    resampledData['fp2'] = df.fp2.resample(timeFrame).mean()
    if show:
        resampledData.plot()
        plt.show()
    return resampledData

def genDataName(patient,activity,trial):
    return 'Data/' + '{0:01d}'.format(patient) + '{0:01d}'.format(activity) + '{0:02d}'.format(trial) + '.csv'

def genImgLoc(csvLoc):
    return 'Plots/All' + csvLoc[4:-4] + '.png'