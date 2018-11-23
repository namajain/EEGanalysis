
# EEG Data Analysis #
Monitoring brain waves in Meditative and Non-Meditative states using EEG with the goal of building a classification model to predict the state (Meditative vs Non-Meditative)

## ToDo: ## 

### 1. Collection: ###
- [x] Collection of EEG amplitude data in 3 states: Meditative, Casually Thinking and Reading a fiction novel (One test subject)
- [ ] Collection in Meditative state of second test subject

### 2. Cleaning: ###
- [x] Resampling the  time-series data into intervels of 16 miliseconds 
- [ ] Smoothening the data and removing EEG artifacts

### 3. Analysis: ###
- [x] Performing Fast Fourier Transformation to produce Frequency-Amplitude data 
- [ ] Performing Wavelet transformation
- [ ] Using stock-market indicators for inference 
- [ ] Identifying the smallest quantum to determine a meditative state
- [ ] Building a classification tool to predict the brain states


## Observation Log
### 23rd November 2018
For now, I'm able to identify meditative states by looking at the FFT transformation for 10 min long recordings, I think the next step should be to identify the smallest quantum of signal which can be used to reliably predict meditative states
