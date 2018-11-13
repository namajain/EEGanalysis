import pandas
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt

CLIPDOWN = -600
CLIPUP = 600

THINKING_CSV = 'thinking.csv'
READING_CSV = 'reading.csv'
MEDITATING_CSV = 'meditating.csv'

FREQ = 256

def plotFFT(csv):
    df =prepareEEGdata(csv)
    # df.plot()
    # remove outliers
    # df=df[np.abs(df.fp2-df.fp2.mean()) <= (100*df.fp2.std())]
    # df.plot()
    yf = scipy.fft(df.fp2.values)
    x = scipy.fftpack.fftfreq(yf.size, 1 / FREQ)
    # yf = yf/1000
    fig, axes = plt.subplots()
    axes.plot(np.abs(x), np.abs(yf))
    # axes.plot(x[:x.size//2], np.abs(yf)[:yf.size//2])
    # axes.set_aspect('equal')
    # axes.set_xlim([xmin,xmax])
    # ymin = 0
    # ymax = 20000
    # axes.set_ylim([ymin,ymax])
    plt.show()

def prepareEEGdata(csv):
    df = pandas.read_csv(csv)
    df = df.dropna(how='all', axis=1)
    df = df.rename(index=str, columns={'FP2-F4': 'fp2'})
    df = df[~df.fp2.str.contains("FP")]
    df = df.astype(float)

    df.fp2 = df.fp2.clip(lower =CLIPDOWN, upper =CLIPUP)

    df['diff1'] = df.fp2.diff()
    df['diff2'] = df.diff1.diff()
    df = df.dropna()
    df = convertToDateIndexFromNum(df)

    return df

def plotRange(df,dfCol,start,end):

    df.iloc[:df.fp2.size // 10].fp2.plot()
    # df.tail(1000).fp2.plot()
    plt.show()


def convertToDateIndexFromNum(df):
    df = df.reset_index(drop=True)
    df['id']=df.index
    df.index = df.index / FREQ
    df.index = pandas.to_datetime(df.index, unit='s')
    return df


def showHist(csv):
    df = prepareEEGdata(csv)
    df.hist(column='fp2', bins=1000)
    plt.show()

showHist(MEDITATING_CSV)

# plotFFT(MEDITATING_CSV)
# plotFFT(THINKING_CSV)
# plotFFT(READING_CSV)