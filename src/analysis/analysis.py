from eegLib import *








csv = genDataName(2,1,2)
dfMed = prepEEGdata(csv)

dfMed=dfMed.abs()
x = dfMed.fp2.values[:1000]
t = dfMed.index[:1000]
imfs = emd(x, nIMF = 5)


fig, axes = plt.subplots()
fig.set_size_inches(19.3, 10.91)
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
fig.tight_layout()

for i in range(len(imfs)):
    plt.subplot(len(imfs),1,i+1)
    plt.plot(t,x,color='0.6')
    plt.plot(t,imfs[i],'k')
    plt.ylim([-1000,1000])
    plt.ylabel('IMF '+np.str(i+1))
    if i == len(imfs)-1:
        plt.xlabel('Time (s)')
plt.show()
# generateAcfPlots(dfMed)
# showHist(dfMed)
# rd=resampleData(dfMed,'4ms', False)
# # doFFTcsv(csv,1,1)
# plotFFT(MEDITATING_CSV)
# plotFFT(THINKING_CSV)
# plotFFT(READING_CSV)


