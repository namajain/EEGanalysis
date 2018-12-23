
# EEG Data Analysis #
Monitoring brain waves in Meditative and Non-Meditative states using EEG with the goal of building a classification model to predict the state (Meditative vs Non-Meditative)

## ToDo: ## 

### 1. Collection: ###
- [x] Collection of EEG amplitude data in 3 states: Meditative, Casually Thinking and Reading a fiction novel (One test subject)
- [x] Collection in Meditative state of second test subject

### 2. Cleaning: ###
- [x] Resampling the  time-series data into intervals of 16 miliseconds 
- [ ] Smoothening the data
- [ ] Removing EEG artifacts

### 3. Analysis: ###
- [x] Performing Fast Fourier Transformation to produce Frequency-Amplitude data 
- [x] Generating the autocorrelation plots
- [ ] Performing Wavelet transformation
- [ ] Using stock-market indicators for inference 
- [ ] Identifying the smallest quantum to determine a meditative state
- [ ] Building a classification tool to predict the brain states

## Guidelines for data acquisition
* Impedence should be less than 20 kilo ohms
* Records should be saved in format **XYZZ** where X is the patient id, Y is the activity id and ZZ is the trial id
* Pyplots for FFT should follow this uniform config - tight fit, frequency 0 - 80 and amplitude 0 - 500000
* Duration should be around 10 mins and should use the data from 0:15 - 9:15


