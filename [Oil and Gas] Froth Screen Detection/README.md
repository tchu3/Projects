

<!-- OBJECTIVE -->
## OBJECTIVE

OBJECTIVE: Create a computer vision algorithm that **OBJECTIVELY** detects whether the process in the plant is upset.
![Clean froth on the left and upset froth on the right](https://lh3.googleusercontent.com/pw/ABLVV862XzTYtbYuMaUOvVBJeCakIY5vacykrBvr1IWcnhki4jBU6d89ZRAvxcU5Knw2wy90OQZQyZoWruwisYNtNKRHjO5_LC4XoxnU557cYocOr7ZkOz0uZ-oPLVRwWY__RK4nSKty-XHatd9xaJ11fgpRSXyvuoocanvLHM99hkLXY91Drsz2XVlPHqraEYMry3k3IQ8Tf2A3lOkY0zJrNBtk_dpHlOq6RQHjZcht7G6OnknRWH2L0X4eCaRTIuTmiIE_CrFIfq002TOQXp3YBNTkUQJl1-gc3QGaC6jibJa0ESwZq9_z_OQ-1jnq5KZ6TxE3L8JGZ2hDY-hPb6M3Ekd9Kf4Bb7mRLHiR8NKEAxrJZ36YuElmoenTQl7p3WNhAiGIo9IIwmcrZ9YK7TJr9XnMMOdYIaKF6KQplDIsfEt1bG6bfdm2ScZANYl6RE6ZV0d-7i1t35sT3O4-W4bc1JC55zwf7CvZjFYq-34FnSxyIFd9F327aTtpBZDyVFDFN37O0o4yzZ4ACqNUvWee6kYRJ3H0BUPWDLIuUyloo35TJNnC6tnyzRsIliJUzCLptamkgvAr_Y9b7YmYbqOUPA6On3l3Tlsh1JRPD2i8wK1gkLe-LsDpXDqCHNNDAo5OvNXrgdK1IRAD5bYq2H4H_Wp9i6zALDtFlFTXuvFA-NurKtaq8_cmzV4BW9XhucGIoQzVCjGwZBbFTLQ87sW6UysCYfdb09DCQ-XEPs0I6le-wpMJjkegsPCINV52vlmh9RbPgktBE7YdelBsoA7QunzByK9uuL6wEBHnBlqI5-ASPxyS3QWV9POnKpGFQZ265Qv7edD0VV418JoJcjsjdGznpQqkEttIxfbFbxpgO6s0m0qn7aZgiA6BJyKBJB3zKbxo3-qpMusufgdeOWVS3Aic2Vm2vgC0MOMfjv8ptQ=w1025-h360-s-no-gm?authuser=0)

<!-- ABOUT THE PROJECT -->
## ABOUT THE PROJECT

The current process has a CRO (control room operator) visually inspect cameras setup in the froth screen building, and make a determination of whether the process is upset by how "watery" the froth looks on the screen. Water content in the froth is an indication of poor processing and causes restrictions down stream in the process. When the process is upset the throughput of the plant is affected, ultimately affecting production rates.

**Data Collection**
Process engineering team kept a log of upset conditions in the plant. Over multiple months, I collected videos of upset and clean froth, tagging each video and pulling the frames for each instance. An issues arises that these cameras are affected by steam in the froth building obstructing the view of the froth box, and the CRO has control of the camera changing the location of the froth box in the frame.

**Video and Image Processing**
1) Brighten and contrast - increase contrast and reduce brightness for optimum image processing
2) Greyscale - Convert image to greyscale for simplistic processing (no additional value is lost by converting to greyscale)
3) Canny Algorithm - Run canny algorithm over image - blur is applied to reduce noise in the image, the Sobel filters are convolved in the x,y direction to determine gradients to detect an edge
![Post-processed Canny Image](https://lh3.googleusercontent.com/pw/ABLVV85LLooTHonx7G7V_PuAF3PcwHNayEDus_0vfyBrTpJgpeCCh3FeHfUMZP4W8237xDZ-JM9NwBsBjJ0VtMNEwBSiPYuA6gPJy2McmwqIGUk7cmD5IkBEHFqbddUiCSYIBL-EipVC-kBJKMn2wWffr_lFdhmk_lwkiqV64tH34iOq2CtJOffZYt3YXlmla5VyPvoJAhTUMnLKIgYD_payc9LCxiPTbvt8QtDNNpaAb_URFqtOL9jXyrmnEbmohKln5eO9M-NA-jnWQJbYO5SPn1eLU8LFMKDFUfpxXxFCkwgGe8G9OaxzjrUBmeTQJCtbvEzMckWBRGJ1qBPQBpMqRWNrVwT5rizHDf70YS1GOLeHXKpdXCWN8Miaw_MpYoymHNpuY7jbYNLV6QZnPMgJ_Uu2LFVwfwssduwBH_4S0c_06Rw8JIHwk8rqKOCyC2y3T4ZS3WR1tihDtYzCGu-toFWYExu8hrRcBNSpg5-r_nY-vo0lXsLdX16056uXsF9Xr9WAkL01-e2ttVsuvS26FfL54tKzvPgzX8ozcSHR7gwDGW1WI0dOyub16AQ-gyx3Zz24ik1aT9eJb_ukTLvDjw9oCws2A2Kx26W3I5faX9PWwpVIdnaK85yYdN1aPrNVG8T3xFft3TIHGMmQzcpuHXcFDwd1iQeOluyxdKZp5m02zxP-n8jNEsAfOtYyMTj7ATAT4RVWlZPHNFSq-DdJXYeo09670ejsfI8O39ll_v5jhVVMJgNJEai0Qp6txRLEdElSHMF_i75qUi1mafzvfbjuZTglfAXGiyUWNaDsnceWCfBupARlOZxn2LHzfvE5pZGFL1RxUe832gmuRRkz7oJg1irH1qo7tR5WSCfw5jKc3Z66UwrRScBiEIUQEb6c5p-S5gTd--Strr7gU7zl6rjrXFIYl-8gIO-Zc_cySg=w352-h240-s-no-gm?authuser=0)
4) Houghs Transform - transforms (x,y) coordinates to polar coordinates (theta, r), intersections in the (theta, r) plane are indications of a line. Hyperparameters are minimum number of points, minimum line length, and line gap. Given a list of lines found in the image, use lines with "target" slopes to identify location of the 4 main edges of a box.
![Post-processed Hughes Transform](https://lh3.googleusercontent.com/pw/ABLVV85NasLI-4jD7vNOn8_crk0TN4htTZB10s4rx9HAm8aYWn3-lZMmvvq4HQfSLW9VsdHrkAszewAE1Imz5MoPYFPUj7eVOF1T-_Tt8kPjRcbhwwB79dD1LCK_3XMgxoWZ8z9_9k8x5bkBjDoaF1DkJO1c-lVoAZHw8JJT98c0mfH5PAeM_z4QAzkFUBR1_GnJ48Jo4mmu4HMCQtZEjsq5ccflw2QvdBMW_2v8CDfB6mXY6uZ9k_na0yTJFAWAovFYTkj9lhLQp-yG5wY7cOmbkEqP8nELhfY-meFc83-5C6v1NphyDLPShT0Jgb-KgvqOnOshIF7GolsS7Swn_TpeKVtNGO_a5qQ0Ba3fGHZFlXULXcJCggm5p2HEwpLtafvgYiPgW8rKqszKzz0sLqtRVjST-RVbMP3ho7sjCF7e2LBup0ohfgq6r1av86tZyV84QVyyTORcQrUQjjxhdQkgM8ByBSz9JTRdlYgtuOOHRLTnUSQRNhjn0HRWuSs5yO4tOtmteUcfZomfvULwAV0NKqI6ne1biHZJc2UhGhPqM2rIl303qD8quA9N_DEzn2PB0oTwxpkQL-roJomFUeApWa0NC-b5aexgGBDUSzccrULlfbsAkgd6vjcJzDfn2ojmF-F4hhaNW3iTnSDDH4JhM_g-v44qEmD3hGtbUis6O2FW2cFBgs_sQshgCGZoUyf6BdRzwHlypR0CBSLwWYwJhCRMKD8V86AKQzelSNFu-_vWxHS05_YTQwjPAoN-ZwKUCrXRN_49MH2CIS6QO7dIAc_v5FOxcKWnn9ADRFPf5P1NhD7RpaAXn2N7tUzat0-97S7oQVliiJVznzu5X_Dj6kzqBfiXjOJz40ys85DXb0gcBdMVMTDongjQgQRn3ZXkv2Gl657xUKLbPBOOzpQJEYFO6G7qFabxwH3VydaS0A=w1118-h400-s-no-gm?authuser=0)
3) Dynamically Crop Image - getCroppedBox function - after identifying the top of the box, draw an (x,x) rectangle in the bottom left corner for evaluation in the model
![Detection of Cropped Box](https://lh3.googleusercontent.com/pw/ABLVV86Fd4gwDixppIZu1Toh3cqhsmWRFhNkboOakMVXohOSTNoW5np8QFCCCt9XCRk7ov4-vEH7kWJDjgtAEsuFvZP7UPrYcM5D7ii2YU-D7Nx87jtym7Grx6uCYvNBNHJQXhr40fHS2LNx7eFyGU03HlYUMhdHGOSMBIAY2Vys1A4HRyuaWbEfQWzhAT3878GqyXk6BHgOeTn-frXGrwj58WFOZOsZqd_pGZVR0V0pdIGPOo7d1Wi-XIgE2TOuaCGjLIy7cNuIdkPth7gJsbye7vKXl6DDmCe9-5OEHO9oJnDZ2yirrp_KVArg6mDG3iAncFmSKvMrRhW0UCUxyIbdtjhZOFIcyxoGvOe8WOBXpiAsZwIYy7JBa0BgG0Y0EK-QiXksLoVitqiXtUDItnApvBXQDADxtrEGnunZFDIRvKPIuOcS4knjXSJ-1c0f4_oLr34MmpcxR-29z3Nv7fcq8Pl_lNmt0aAk9RuLV4ZvrUCJ7RRE7D0D2BXVLxmxRRs6jfcYhFp6nKVeoX-9eEXKfEp6KhscapjDUHKjksZX_bNU93E7ggAcpggVduinNCJtcBmP0hmYzUb7rn4wPoLk26ox6GDQgU8sR5Vz6Lf-F6tpYgihnN-XqE111Q-Jqa54odMYfTQ30PUHcjjZW4fAIyiJkXLt-7z7BqxuY8w33bQMu9E2mCWZk35RRNdji7mikFo0Rt77NTM8DpyOPP4xU6VjSNy1uEP2nzmWgxhlJoOgpiKfZeAYbT7ALdDMXNECkSba22EbSJCpHXxfEZKC2ArvPCGsI3KSfhjjRFrxTepaHjJ6Al7r8dvLIB33m8ENvBCqynKZ-OKfTN503N-4rwNaEzpYn9nDFl9ZziTeeXztHxBDsEcOYeWcI_y1TJ6Hq9Zoctk85vaREUiKT2VXBt8PNToHK5ujc3beqqD1XA=w583-h358-s-no-gm?authuser=0)

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

1) Currently programmed to process mp4 files, future update will need to be mapped to a live data feed
2) Dynamic cropping function will be preset to run every 5 minutes
3) The detected box corner will be drawn on the screen (bright green) to tell the CRO where the algorithm monitoring


<!-- ROADMAP -->
## Roadmap

TODO List
 - Map input data source to a live camera feed so the algorithm can run continuously - the dynamic cropping algorithm will only run every 5 minutes to ease computational load
 - Create and evaluate other models including a convolutional neural network

<!-- CONTACT -->
## Contact

Tommy Chu - www.linkedin.com/in/ttchu - tommy.chu3@gmail.com

