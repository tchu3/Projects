
<!-- OBJECTIVE -->
## OBJECTIVE

OBJECTIVE: Create an algorithm to objectively detect whether the Primary Separation Cell (PSC) in the extraction plant is upset based on the TracerCo (density meter) profile.

<!-- ABOUT THE PROJECT -->
## ABOUT THE PROJECT

The current process has a CRO (control room operator) visually inspect a TracerCo (density meter) profile on a computer screen in the control room. The CRO makes a determination of whether the process is upset by subjectively determining whether the interface of the profile is "blurred". 

The TracerCo tool measures the density of the fluid over 88 tubes. A tube that measures a reading of 1,000 kg/m3 indicatse water, while a density less than 1,000 kg/m3 indicates "froth" (the desired product), and a density greater than 1,000 kg/m3 indicates middlings (a sand slurry - the undesired product). A "blurred" interface indicates that the vessel is properly separating froth from middlings, while an interface that is sharp and distinct suggests the process is running appropriately. When the process is upset the throughput of the plant is affected, ultimately affecting production rates. Below is an example of "clean" separation interface.
![Example of a TracerCo Profile](https://lh3.googleusercontent.com/pw/ABLVV85-_6S-DA7p_fI4CDlgNgjLcpRMxsQ4U6q_Xv9dEnZJ5_-MO4ORh-kasXliXglFVUYSyRM1PAgxbTJ3XTrx15AbkYnY7ZIHSfqY9mOt4qcOxeTx5qy2fXFQNv-tGIRyVcaaFanwygJDBEPn114CEPey=w457-h634-s-no-gm)

**Feature Engineering**
The primary feature set of 88 density readings (from each tube in the TracerCo) is a large feature set, and is inappropriate to be used in a model. Feature engineering is used to manufacture a set of properties that can be fed into a model.

Dimensionality Reduction
1) Clustering - the 88 tubes are clustered using k-means - the algorithm initializes ‘k’ centroids and convergences to similar datasets based on a nth dimension space using Euclidean distance. In this case 3 clusters were chosen to identify gas, froth, and middlings
2) Cleaning - each cluster is sent through a cleaning algorithm to remove outliers (i.e. plugged tubes that have abnormally high readings)
![Clustered example](https://lh3.googleusercontent.com/pw/ABLVV86OeV308MARk1281mVrRYBgMg9makc9cdQ0UFpuUTbJoB2b1xbx6KnOAiOIeWkyP1lm55HxD27ASFM2yLhT7LSz9MAPJXoJDNQB1f8dHBwPsY-Qsg7qVLVsFyxYsTHlXDyTyZRDL6k5gQocq3uJ5bWP=w597-h631-s-no-gm)

The resulting the clusters are then fed into (2) models:
1) Slope Method Algorithm
This method utilizes the clusters and draws two lines. One for the froth phase and another for the middlings phase. The two lines are intersected, and depending on where the line intersections will suggest whether the interface is "blurred". A intersection that is large (or infinitely) far away from the middle tube (40) indicates that the vessel is separating properly. The features extracted from this method are:
- Slope of the froth phase
- Slope of the middlings phase
- Paired mean difference (bulk density differences of the froth and middlings)
- Intersect of the two lines
![Example of the slope method](https://lh3.googleusercontent.com/pw/ABLVV84cZIe4P1-SbPkGFcZSJO9Ho6AJ4AG7oD0ZTujHgG6pZhiBe9eQJ991xKe2DQ7FyTZQ8Nr9qwm2W0XinjWLTrBacIudVfRkKtqEAD5Ga_IIlLPQfmiV-0g-4_ymUBCOh0p53HDZ0vVwOKF5kKk9RHfg=w460-h630-s-no-gm)

2) Sigmoid Method
The TracerCo profile is fit to a sigmoid. Conventionally sigmoids are used in machine learning algorithms as an activiation function, in this case the raw shape of the function is used. 

![enter image description here](https://lh3.googleusercontent.com/pw/ABLVV87mq_zXMpWCDXuQCJA1MSapGZa6x2jXG0kSNN7JfIvT8IUHFBRXl_ObOEVSz4n2dHUOMbVgfIc4eN75ZS-1rGzFFRdUmUmjRFl8ioOtajI9kegzEy-_epQkSOPnFNYn0GkJGBav4n2FvodRukgfbtvD=w640-h193-s-no-gm)

The function is fit to the TracerCo profile and the properties of the function transformations are extracted.

- a
- b
- c
- slope
- trace (aka the residual of the fit)

**Validation Method**
K-Fold Cross Validation
1.Data set broken out into ‘k’ bags of data (i.e. 3 parts)
2.Model is trained on ‘k-1’ bags of data (i.e. 2 parts – 66% of data set)
3.Model is tested on 1 bag of data (i.e.  1 part – 33% of data set)
4.Process is repeated on all bags of data
5. Model is reset so model is not retrained on existing weights causing overfitting

**Evaluation Measures**
- Accuracy
- Recall
- Precision
- F1 Score

The properties extracted in the two methods above were evaluated using a rules-based approach and a neural network. A rules based approach used empirical/visual interpretation to determine the thresholds to identify upset/clean conditions.
![enter image description here](https://lh3.googleusercontent.com/pw/ABLVV862f0XayLoSq2gmLQUTOQp5r_vOVrso3ZfG1c5DKj0o2RuiCqxzvPXX5zQUdZhNECJBVCE403UGI8_KpoGft5K4jeaClEuD33W5PPthjQUO2ajucpnZrQ-0T5wV7iDz6V97kQ9cSD5q_O6EVCjHrYX7=w1041-h352-s-no-gm)
![enter image description here](https://lh3.googleusercontent.com/pw/ABLVV85HDOedLhUCpq6yIAFeMUlNGVPaYsuG0ko5rxVtT1GofaFFMtykfn7t5QGlO6mSUk1JijysrlEU6Lf4Ij9ADicS_BxtqxkzV9nrZWdV1eMVs1FCpM4TjB8SNfzvWY7Bv4ut9jK4vjghOa-DrAIlErlK=w950-h586-s-no-gm)

<!-- USAGE EXAMPLES -->
## Usage

The script is currently connected to Albian PI - an ODBC connection to a SQL server that contains plant data. The connection will not work without permissions. The script is run through Tkinter to provide a GUI for users to provide a visual aid while the algorithm is running.

<!-- CONTACT -->
## Contact

Tommy Chu - www.linkedin.com/in/ttchu - tommy.chu3@gmail.com

