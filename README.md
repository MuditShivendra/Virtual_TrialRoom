# Virtual_TrialRoom

## Problems Identified
-While shopping fashion on an e-commerce platform like Amazon, it is difficult for a user to visualise the fit and appearance of products on the said user.

-This uncertainty results in more returns from users who cannot get the gist of the product they have ordered.

-Shoppers often prefer offline modes of shopping when purchasing fashion goods since they can judge how a given product looks on them.

## So what are we doing here?
Existing Virtual TryOns require complex hardware support which is in most cases not available with the general public.The application should be designed in such a way that it needs no external hardware and should be able to run on the user's smartphone with a camera. 
So here we are with a

-Creating an AR-based platform through which users can virtually try out products they want to buy on any e-commerce platform using their video feed

-With the help of state of the art technology, customers will be able to see how the product suits them with different size models and different ambiences, which is not possible while purchasing offline

-People can see a 360-degree view of themselves and the product on the platform and hence get a personalised feel on how the product is for them and further spark interest in relatability.

## Presentation is available here - 
https://docs.google.com/presentation/d/1yrY2oVPTiEstRpIIyMXnouS-HPtyUC6mBmn5M1dY2jg/edit?usp=sharing

## Explanation video is available here - 
To be added

##Realtime TryOn apk (prototype) is available here - 
https://drive.google.com/file/d/10jMRRBXvuxti4zMq110eqFpUHtfPZc10/view?usp=sharing

## Requirements

* Python 3
* [`axel`](https://github.com/axel-download-accelerator/axel)
* CDF (https://www.scivision.dev/spacepy-install-anaconda-python/)
* [Unity](http://unity3d.com/) 5.3 or higher.
* [Android SDK](https://developer.android.com/studio/index.html#downloads)
  (when developing for Android).

## Unity Setup - 
- add the unity project from `/Unity/Trial_room`
- open the `SampleScene.unity` present in `/Unity/Trial_room/Assets/Scenes/` in the unity editor


## Backend Setup - 
-run `pip install -r requirements.txt` located in `/backend/`
-Build c++ library for post processing in `backend/tf-pose-estimation/`
```
$ cd tf_pose/pafprocess
$ swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
```
-Go to the directory `/backend/server/` and run `python database_server.py`
-Once the server is setup, enter the ip address in credential.cs and upload_video.cs present in `/Unity/Trial_room/Assets/Scripts/`

## DataSet 
* **We are using Human3.6m dataset which is to be downloaded from** http://vision.imar.ro/human3.6m/
* View the following repo readme to see the steps to process the dataset- https://github.com/anibali/h36m-fetch

## References - 
  
  Original Repo(Caffe) tf-pose-estimation: https://github.com/CMU-Perceptual-Computing-Lab/openpose

  Openpose' for human pose estimation have been implemented using Tensorflow. It also provides several variants that have made some changes to the network structure for **real-time processing on the CPU or low-power embedded devices.**
  
  3d-pose-baseline : https://github.com/una-dinosauria citation :
  ```
@inproceedings{martinez_2017_3dbaseline,
  title={A simple yet effective baseline for 3d human pose estimation},
  author={Martinez, Julieta and Hossain, Rayat and Romero, Javier and Little, James J.},
  booktitle={ICCV},
  year={2017}
}
```

  


