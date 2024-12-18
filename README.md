# Trash Collection - Detection

This is a build inspired by the following Project:

<p align="center">
<img src="https://raw.githubusercontent.com/wiki/pedropro/TACO/images/logonav.png" width="25%"/>
</p>

TACO is a growing image dataset of waste in the wild. It contains images of litter taken under
diverse environments: woods, roads and beaches. These images are manually labeled and segmented
according to a hierarchical taxonomy to train and evaluate object detection algorithms. Currently,
images are hosted on Flickr and we have a server that is collecting more images and
annotations @ [tacodataset.org](http://tacodataset.org)


<div align="center">
  <div class="column">
    <img src="https://raw.githubusercontent.com/wiki/pedropro/TACO/images/1.png" width="17%" hspace="3">
    <img src="https://raw.githubusercontent.com/wiki/pedropro/TACO/images/2.png" width="17%" hspace="3">
    <img src="https://raw.githubusercontent.com/wiki/pedropro/TACO/images/3.png" width="17%" hspace="3">
    <img src="https://raw.githubusercontent.com/wiki/pedropro/TACO/images/4.png" width="17%" hspace="3">
    <img src="https://raw.githubusercontent.com/wiki/pedropro/TACO/images/5.png" width="17%" hspace="3">
  </div>
</div>
</br>

For convenience, annotations are provided in COCO format. Check the metadata here:
http://cocodataset.org/#format-data

For more details check their (https://pedropro.github.io/ and https://seomis.cc/) paper: https://arxiv.org/abs/2003.06975


# The Story
So this is... a mess.
The premise is summed to one line - 
I want to pick up trash I see while hiking, and I want drones to help me do it so it will be faster.

Hi!<br/>
My name is Dvir Flom and I'm learning to be a Data Scientist. By myself.<br/>
After teaching for many years (Math, Computer Science and Physics in academy) I've learned the best learning paradigm for me is Project Oriented.<br/>
And my project is to use detection and classification models to locate Trash.<br/>
I really don't think I can clean up a lot myself, nor do I believe that this project will have a profound impact, but it's cool. And I like the idea.
And a few people around me said they will help along if they can. So here I go.

Trying to build on the TACO Project (just for trash detection) would have been perfect, but a 5 year old project doesn't live up to it.<br/>
At first the idea of running a Masked RCNN model would have been the dream, but now YOLO is the state-of-the-art (SOTA) architecture 
and the python packages needed to run the Matterport implementation for the MRCNN are from 2017 are not easily available.
Soooo - 
1. I took the images from the TACO dataset
2. Translated the coco annotations to yolo
3. Trained the model
4. Rinsed and repeated

To say the least this was and is excruciating and horrible, and I don't even have a GPU on my laptop. So to train YOLOv8n with 60 classes in 1500 images (Total, not each),
Would take me ~60 Hours each time. <br/>
Well I guess now is the time to move on to cloud computing, and I'll go with the easy choice for now - Google Colab.

## State-of-the-Mess
This is basically my TO-DO List:
1. Join all the helper functions into a Utils package.
2. Write a clear roadmap on how to use all of this (begining to working model).
3. Move the data to Google Colab.
4. Train the weights on the "cloud".
5. Download weights and make sure they infer correctly on test images.
6. Move on to the next phase - Detecting & Classifying trash in videos.
7. Move on to the next piece of this total project - Analizing drone videos and mapping trash unto a map.