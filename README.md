# TMS016 - Project 3 - Iris Recognition
By: Jack Sandberg, Sara Arnesen, David Nordström.

## Summary
A project in the course TMS016 Spatial statics and image analysis exploring the applicability of the iris recognition algorithms proposed by John Daugman. The methods are able to successfully locate 77% of the inner and outer boundaries of the iris in the MMU Iris dataset. Among the individuals with successfully located iris, we are able to classify 95% of the iris when comparing against all located iris. When restricting the comparison to only one ground-truth sample, we are able to classify 78% of the iris.  

More details of the methods and results can be found in final report PDF.

## Setup
```
conda create --name tms016_project3 --file requirements.txt
```

## File descriptions
Note that we are not allowed to further distribute the MMU Iris dataset. The dataset is required to run most of the code.

**loadData.py** - File that provides functions for easy access to the dataset and the output from CalculateIris.py. Requires the dataset to be in the directory /MMU-Iris-Database/ and output from CalculateIris.py to be in the directory /OutputData/ if no other directory is specified.

**findIris.py** - Functions performing Daugmans algorithm.

**irisNormalization.py** - Functions for converting a circular region from x,y-coordinates to non-concentric polar coordinates.

**gaborWavelets.py** - Functions defining the Gabor wavelet and for performing convolutions with a 2D Gabor wavelet.

**CalculateIris.py** - Iterates over the dataset to find the iris and pupils of all images. Also normalizes all extracted iris' and calculates the binary encoding of the iris'. Saves all generated data to /OutputData/.

**checkDataQuality.py** - Iterates over the data generated by CalculateIris.py and lets the user inspect and rate the quality of the iris' found. The ratings are saved to *dataRatings.txt*. Note that you may need to change the path to your browser of choice.

**compareHammington.py** - Loads all the data calculated in *CalculateIris.py*, calculates the binary encodings, all Hamming distances and finally classifies the all iris.

**visualizedFeatureExtraction.py** - Visualizes the found iris and its corresponding binary encoding.

**testIndividualImage.py** - Tests the effect of applying a Gaussian blur to one of the images.
