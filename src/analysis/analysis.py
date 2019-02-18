if __name__ == '__main__':
    from src.lib.eegLib import *
    print('meow')
    csv = genDataName(2, 1, 2)
    dfMed = prepEEGdata(csv)
    # with open('imf.pkl', 'rb') as input:
    #     imfs = pickle.load(input)
    # dfMed=dfMed.abs()
    # dfMed=dfMed[:20000]
    # import time
    #
    # start = time.time()
    # eemd = EEMD(trials=8)
    # imfs = eemd.eemd(dfMed.fp2.values, max_imf=5)
    imfs,res = emd(dfMed.fp2.values, nIMF=5)
    rdiff = dfMed.sub(res, axis=0)
    # rdiff=rdiff.sub(imfs[3], axis=0)
    # rdiff=rdiff.sub(imfs[2], axis=0)
    # rdiff=rdiff.sub(imfs[1], axis=0)
    # rdiff=rdiff.sub(imfs[0], axis=0)
    # end = time.time()
    # print(end - start)
    plt.style.use('seaborn-whitegrid')
    doFFTcompare(dfMed,rdiff)
    # # imfs = emd(x, nIMF = 5)
    #
    # ceemdan = CEEMDAN(trials=8)
    #
    # imfs = ceemdan(x, max_imf=5)
    # with open('imf.pkl', 'wb') as output:
    #     pickle.dump(imfs, output, pickle.HIGHEST_PROTOCOL)
    # print('pickle 1')
    #
    # # dfMed=dfMed.abs()
    # x = dfMed.fp2.values
    # # imfs = emd(x, nIMF = 5)
    #
    # ceemdan = CEEMDAN(trials=8)
    #
    # imfs = ceemdan(x, max_imf=5)
    # with open('imf.pkl', 'wb') as output:
    #     pickle.dump(imfs, output, pickle.HIGHEST_PROTOCOL)
    # print('pickle 2')
    # fig, axes = plt.subplots()
    # fig.set_size_inches(19.3, 10.91)
    # mng = plt.get_current_fig_manager()
    # mng.window.showMaximized()
    # fig.tight_layout()
    # for i in range(len(imfs)):
    #     plt.subplot(len(imfs),1,i+1)
    #     plt.plot(t,x,color='0.6')
    #     plt.plot(t,imfs[i],'k')
    #     plt.ylim([-1000,1000])
    #     plt.ylabel('IMF '+np.str(i+1))
    #     if i == len(imfs)-1:
    #         plt.xlabel('Time (s)')
    # plt.show()
# generateAcfPlots(dfMed)
# showHist(dfMed)
# rd=resampleData(dfMed,'4ms', False)
# # doFFTcsv(csv,1,1)
# plotFFT(MEDITATING_CSV)
# plotFFT(THINKING_CSV)
# plotFFT(READING_CSV)


