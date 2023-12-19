


<!-- OBJECTIVE -->
## OBJECTIVE

OBJECTIVE: Create a computer vision algorithm that **OBJECTIVELY** detects whether the process in the plant is upset.
![Clean froth on the left and upset froth on the right](https://lh3.googleusercontent.com/pw/ABLVV85tcJncZYS1qNGb16j9f0hbv9fsoPz_nrYs3A0wkJZsOJDvOx98RG3HcU4GU_E28j66V604aQMh6R28DznAYrICczqIP7SFw5JxgO1fzyxIxoPWQybqysOWSTQklQQGAD55BcUUge9qV8zb9wN_G3FP=w1025-h360-s-no-gm)

<!-- ABOUT THE PROJECT -->
## ABOUT THE PROJECT

The current process has a CRO (control room operator) visually inspect cameras setup in the froth screen building, and make a determination of whether the process is upset by how "watery" the froth looks on the screen. Water content in the froth is an indication of poor processing and causes restrictions down stream in the process. When the process is upset the throughput of the plant is affected, ultimately affecting production rates.

**Data Collection**
Process engineering team kept a log of upset conditions in the plant. Over multiple months, I collected videos of upset and clean froth, tagging each video and pulling the frames for each instance. There are a couple known issues first when there is steam in the froth building obstructing the view of the froth box (the fix for this is to be determined), second, the CRO has control of the camera changing the location of the froth box in the frame (the dynamic cropping function handles this issue)

**Video and Image Processing**
1) Brighten and contrast - increase contrast and reduce brightness for optimum image processing
2) Greyscale - Convert image to greyscale for simplistic processing (no additional value is lost by converting to greyscale)
3) Canny Algorithm - Run the canny algorithm over image - blur is applied to reduce noise in the image, the Sobel filters are convolved in the x,y direction to determine gradients in the image and detect an edge
![Post-processed Canny Image](https://lh3.googleusercontent.com/pw/ABLVV85In3blyagpgjP1VMXZv19RMvYh7EMbCwLKyTkCkNPE2TC8JSEmLYsVc8ws5ld_yVgHLRahXAbe6RXLbOMHXXA33fVlTMIjIg4kmvsECXhsYmIyxvC93z3TZq0o9yd_JkqHQXn9C6x2KqL0O5XSCNCG=w352-h240-s-no-gm)
4) Houghs Transform - transforms (x,y) coordinates to polar coordinates (theta, r), intersections in the (theta, r) plane are indications of a line. Hyperparameters are minimum number of points, minimum line length, and line gap. Given a list of lines found in the image, use lines with "target" slopes to identify location of the 4 main edges of a box.
![Post-processed Hughes Transform](https://lh3.googleusercontent.com/pw/ABLVV86cWy2OgKYzXz1OQiaaCkx2AqfVZ5-L9NBkF_PC8AZYBHt0m8X5KhPR5-pF-Hbt8YBsb4N5rsFzEZE9UE_YRE6Q11h6dlwf_MkLt1I2N_G9BfWgniGyy263PlXv-40w27uJu6YGgePd6joG6x0-8Im7=w1118-h400-s-no-gm)
3) Dynamically Crop Image - getCroppedBox function - after identifying the top of the box, draw an (100,85) dimension rectangle in the bottom left corner for evaluation in the model
![Detection of Cropped Box](https://lh3.googleusercontent.com/pw/ABLVV85bnUiYZn82CV-LbmCVisHn4wW_6_UMY97_vZfRJrUbKu31wXYHJO1Uv5-OYmtQ01VKdzTY4HP735YbHxmGEdymE5jj-VyllJeJTE1D_GCYPkd-WUFh6fIip38SgZvf84ZH7elCCA397othq4XCrtRQ=w583-h358-s-no-gm)

**Crossing Frequency Algorithm**
The simplest method, used to determine upset conditions. 
1) Each pixel in the cropped frame is converted to a number (identifying the black/white scale of the pixel). 
2) A moving average over 'x' frames is used to establish as a baseline condition
3) The average of the current frame is compared to the moving average, if the average is "crossed" increment a counter
4) When the mean is crossed multiple times it is an indication that the process is upset

**Fourier's Transform Algorithm**
The second method utilized leveraged Fourier's Transform. The intent was to compare a series of frames and apply Fourier's Transform on each pixel. Fourier's transform will map each pixel to a sinusoid, and the frequency and amplitude of each pixel would be an indication of upset or clean conditions.
1) Convert cropped frame to a numpy array
2) Cropped box will initially be sized as a 100x85 array (each entry in the array reflects a pixel)
3) Apply 1D Fourier Transform on 'x' frames the 3d array will have dimensions (100,85,x)
![Cropped images over 9 frames](https://lh3.googleusercontent.com/pw/ABLVV85-4y3H3E_xzDjcnRQsKmNCBwQWcXfLeXP-Rfkc5LsPe2AYGdUrjvYzAg5QrsiJncCBz7jevM3uquO7CXEPGOYKgrlI4Ww11m_YDZ3KuDCxLlhn-WBRbRQ7HucKqSGzIW0GUCkRcZxqm957gudFzMmfCEyokt6HHrKzYBOwN37ZR-l84Qr5JhN0dffL-mIn39lySnvNjwNH3NEasv4Y-Qe2nDLDTAQ1anpsbkDUXb1hS7xUG9AyP0JuRg0WIgHFupjF0vLv7_2eXwMy16bvfNGduTqL8I9wb45-aFNzWIBc-OMewEPF4tmsn3ZJ8XW0COhgxDMj7kT0O3B3jFC3qhFmlRF45rOye2TqYb5IP7WNdu-A2fpKe-aVGq5wKxyVz82J31faDl6-_kVojcurpaDQh4-stUrN6f-3eH2swU9RFuboXw35rDVO-6QK-Y95tS_bZlBjHz5lZ-O72UkDnupUGOvys-UYlNAFX88lUGb7XDl42NB-4xlboDO6x5H8f0kGiEV3YeViNVxK5vnaXRA_4X09YqEeJ9MU4hhRMAyRlrpUA_afGv2zIBOjjK7cPgfESYeUluanoZJEm1krVolw1P8YFIVBSm6VBkSJfAetEE9K9AzEQE-69Sq5H6_rY81sXz_Wsc0WKuHuIrI-sL89SSTVdfD0Z7S3hCPdTDewgo8ITAoSKdu03pt9KcomAsydBIl1oSrRfE1iyduiVB08bNs7BdiUAVdL81b4-pC8kAk1rXzun1TX06dRCZgiXyhZHAtGDoCDMVQCZVuh5RBK7f7Gq7PTqVQWG_NfVtgyQJlKbA2y2yYlWCXuFci5zV2P4-39QJpEiC_2IX_DkrmPs3VwiLRkX81YQbqdZ-jP-YvLbNcvAdqPW1V9b5CIlTiU-AUl-P8cc-AiocucO_e5xA2KVIHHb_TZdboClg=w1285-h607-s-no-gm?authuser=0)
4) Fourier Transform will result in a series of sinusoids, data analysis will be run to determine what combination of amplitudes and frequencies are indicative of upset conditions
![Fourier Transform sinusoids, left represents clean conditions, right represents upset conditions](https://lh3.googleusercontent.com/pw/ABLVV84MIDSk7o9VQnWUuEPQRvGkmlB-n2rxURMoDx0d_v7Q2SdVI2bKi6273ir6wDs0zCXqaKGG2iHvD57S2ghIoyR7n-uIGOzl6anr6-QJPqhA46chvG5Mj1FqpLjI3b_ZFkQDMQIMIwuhMnGKjbuLl0l4esy8arOrlb5byyC9ngUkINDs19zqL_oZrhn14GYS5qPsbdxpyIR38KjHtNYRXy-HehxBTVmoapEf81YoPCWM0G4EB1tCqXFvtqvBZwyhtySf99l7n-AuhppX6rLTdbiy5flhBcbytNSAruE1oQAJDViBEd-eTXlhH8NcJSVx2-YH9T4uOk-c1NnnbAZlR-rYUpM-EBUQtcTQ9wZP7EBqGxGs66CpuIDOemdN8n4cBFk2gSV-kG_wTKjI3-mVv8w1x_GiGnmE_GHHUaylIh-BqrjSRhMnZFptE20comyUSr8ts19F4C6CBWvrSOQN1R8Q8TsoGqbLT7kNU7n73eVVeAI9TLi9SRf1Dm2636hfnDySPhB-rayjT82QHfObs_xMZuLIDcMFAs_SUqlvC6C_c1V71WvxtdH2ubt_EcthLy-4PPZ4ribIrkf59KduhnqKgM5CW__xsWeO0-VoP_U0gq1EV_kDS_B92-Ome_r610ePOtPkNs2uiINRfhUMByTqSPksUd6REZVCUhHQ-j8FkMopQUSq3XCM8GE9dgd06jlRY7bFLRuRzT5oiMn2gcRcoNwnY3iOeYnzIO2pZw1gQFCCI2nEyaOqFUxphpZHBDqbi0WUVE1eWOlx1b4xH3kVXXbDPs7aFjdibY6Ro5rV9pbGW-BT_iODXWSmgsj6IlLWnM1INywO3d9t_G_LQqHYojkmEMPR7waWWCcAppkagNul2ItGXVekPVktkHqPtfVZh_bgYQCfX9YQLEXkZlOaWFSoo0AzqLXsbppPag=w1199-h338-s-no-gm?authuser=0)

<!-- USAGE EXAMPLES -->
## Usage

1) Currently programmed to process mkv files, future update will need to be mapped to a live data feed
- Tkinter GUI is programmed for the crossing frequency method for demo purposes file (crossingFrequencyMethod (GUI).py)
2) Dynamic cropping function will be preset to run every 5 minutes
3) The detected box corner will be drawn on the screen (bright green) to tell the CRO where the algorithm monitoring


<!-- ROADMAP -->
## Roadmap

TODO List
 - Map input data source to a live camera feed so the algorithm can run continuously - the dynamic cropping algorithm will only run every 5 minutes to ease computational load
 - Create and evaluate other models including a convolutional neural network
 - Steam affects the clarity of the camera, digital or physical solution needs to be found

<!-- CONTACT -->
## Contact

Tommy Chu - www.linkedin.com/in/ttchu - tommy.chu3@gmail.com