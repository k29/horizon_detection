## Horizon Detection

Horizon detection or sky segmentation is the problem of finding a boundary between sky and non sky regions in a given image. This can have many applications especially in navigation of UAV. This problem has been tackeled by many and there are cheifly two ways of solving this:

* Edge detection
* Modelling sky and non sky regions using machine learning

In most of the early attempts of this problem, there is an underlying assumption that the horizon boundary is linear. This post also discusses one such method by Ettinger which uses latter of the two ways discussed above. 

The basic algorithm in that the sky and ground are modelled as two different gaussian distributions in RGB space, and then horizon line is a line segment seperating the two, which can found by maximising an optimisation criterion. Thus sky and ground regions are represented as two set of points each distributed about a seperate mean point in the RGB space. We then perform a search through potential set of lines (m,b), to find the line with highest likelihood of being the best fit horizon line. Now we just need to find the scalar term for the optimisation criterion. 
Intuitevely, given the pixel groupings, we need to quantify the assumption that a sky pixel will look similar to other sky pixels and likewise for the ground ones. Thus we are definitely looking for a degree of variance in each distribution. Now we want to obtain a single measure of variance from a three dimensional data. We know that the three eignevalues of the covariance matrix represent the degree of variance from the mean along the three principal axes, thus a product of these eigenvalues is a good scalar value. Since product of eigenvalues is the det. of the matrix, we can say we need to minimise the followign function, 

![](assets/min.png)
or rather maximise the following function:

![](assrts/max.png)
where, 

![](assets/sky cov.png)

![](assets/ground cov.png)

The above function needs some adjustments in case the covariance matrix is singular, but this function perfoms pretty well as can be seen in the images below. The code for the implementation is linked below. 





