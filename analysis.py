from eegLib import *








csv = genDataName(2,1,2)
dfMed = prepEEGdata(csv)





generateAcfPlots(dfMed)
# showHist(dfMed)
# rd=resampleData(dfMed,'4ms', False)
# # doFFTcsv(csv,1,1)
# plotFFT(MEDITATING_CSV)
# plotFFT(THINKING_CSV)
# plotFFT(READING_CSV)


