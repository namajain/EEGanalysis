
# EEG Data Analysis #
Monitoring brain waves in Meditative and Non-Meditative states using EEG with the goal of building a classification model to predict the state (Meditative vs Non-Meditative)

## ToDo: ## 

### 1. Collection: ###

- [x] Collection of EEG amplitude data in 3 states: Meditative, Casually Thinking and Reading a fiction novel (One test subject)
- [x] Collection in Meditative state of second test subject
- [ ] Collection of Multi-Channel Data

### 2. Cleaning: ###
- [x] Resampling the  time-series data into intervals of 16 miliseconds 
- [x] Smoothening the data
- [ ] Removing EEG artifacts

### 3. Analysis: ###
- [x] Performing Fast Fourier Transformation to produce Frequency-Amplitude data 
- [x] Generating the autocorrelation plots
- [x] Realtime stream visualization support with play and pause and multiple subplots
- [x] Empirical mode decomposition support
- [x] Performing amplitude modulation analysis 
- [ ] Performing wavelet transformation
- [ ] Identifying the smallest quantum to determine a meditative state


## ChangeLog
#### 18 Feb 2019
* Restructured Visualization module with classes
* Added EMD difference analysis, for the tested usecase imfs seem to correspond with EEG bands like alpha and beta, need to confirm
* Added an experimental blit visualization which renders the plot 4X faster, need to fine tune it 
#### 29 Jan 2019
* Added EMD Realtime Visualization
![Image of emdViz](https://github.com/namajain/EEGanalysis/raw/master/Plots/Realtime/test.gif)
#### 26 Jan 2019
* Restructured the code with modules
* Significantly enhanced the visualization module
* Added basic support for Empirical Mode Decomposition
![Image of baseViz](https://github.com/namajain/EEGanalysis/raw/master/Plots/Realtime/test.png)

#### 9 Jan 2019
* Added a very basic AM envelope detector. Need to optimize and refactor.
#### 23 Dec 2018
* Started ChangeLog
* Added Dynamic Realtime Visualization of EEG Data
* Looking at the realtime viz, the EEG data seems like an Amplitude modulated signal, need to analyse
#### B4 Dec 2018
* Added support for partial and full Autocorrelation Plots
* Added support for resampling
* No significant ACR if data is resampled for 20ms i.e. combining 5 data points into 1
* Added support for time slicing and plotting each sliced component
* Added data collection guidelines and supporting interface
* Added datasets for another meditator
* Added Guidelines for FFT and support for saving it as an image
* Added FFT Plots
* Added base interface for cleaning and loading the data

![Image of ACF](https://github.com/namajain/EEGanalysis/raw/master/Plots/Autocorrelation/ACF_without_resampling.png)
![Image of FFT](https://github.com/namajain/EEGanalysis/raw/master/Plots/All/2101.png)

## Guidelines for data acquisition
* Impedence should be less than 20 kilo ohms
* Records should be saved in format **XYZZ** where X is the patient id, Y is the activity id and ZZ is the trial id
    * X -> [ (1 : Naman), (2 : Dhaniya) ]
    * Y -> [ (1 : Reading), (2 : Thinking), (3 : Meditating) ]
* Pyplots for FFT should follow this uniform config - tight fit, frequency 0 - 80 and amplitude 0 - 500000
* Duration should be around 10 mins and using the data from 0:15 - 9:15
