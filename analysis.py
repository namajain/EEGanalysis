import eegLib as el








csv = el.genDataName(2,1,1)
dfMed = el.prepEEGdata(csv)
# showHist(dfMed)
rd=el.resampleData(dfMed,'4ms', False)
el.doFFTcsv(csv,1,1)
# plotFFT(MEDITATING_CSV)
# plotFFT(THINKING_CSV)
# plotFFT(READING_CSV)
