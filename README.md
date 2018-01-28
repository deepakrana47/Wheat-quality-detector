# Wheat-quality-detector


This is a simple implementation for wheat quality detection, which takes an image of wheat grain seperated from one other. Then perform smoothening, thresholding and segmentation to get seperate images of wheat. And then detect good or not good for every wheat image.

-It takes an image as input.

-Return number of good grains and not good grains or impurity and image pointing to good grains (blue) and not good grains or imputities (red).

To use:

Install python and python modeules (pip, numpy, keras and opencv).

  To install python:
  
    > sudo apt-get install python2.7
  
  To install pip:
  
    > sudo apt-get install python-pip
  
  To install numpy, keras, opencv
  
    > sudo pip install numpy keras opencv

Run:

    > $ python cmd_wheat_quality_detector.py
  
    > Enter the file(wheat image) location to dectect : Test.jpg

With this implementaion these is still problem with segmentation for close by grains.
This implementaion idea is base on : "Prakhar K, Anurendra Kumar, Satyam Dwivedi(2017) AUTOMATIC WHEAT GRAIN QUALITY ESTIMATION, EE604 Project Report, IIT Kanpur" (link: http://home.iitk.ac.in/~anurendk/ee604/Report.pdf)
