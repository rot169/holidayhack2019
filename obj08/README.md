# Holiday Hack 2019 - Objective 8 - Beating the CAPTEHA

### Intro
This code forms part of my solution to the 2019 SANS Holiday Hack. See the main video for details: [LINK_TBC]

### Credits
Based on sample code from Chris Davis (github.com/chrisjd20/img_rec_tf_ml_demo), which itself is based on a Tensorflow example (https://raw.githubusercontent.com/tensorflow/hub/master/examples/image_retraining/retrain.py) .

### Prerquisistes
(Per Chris' sample code)
```
sudo apt install python3 python3-pip -y
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install --upgrade setuptools
sudo python3 -m pip install --upgrade tensorflow==1.15
sudo python3 -m pip install tensorflow_hub              #this one may or may not be needed in order to run
```

### Contents
image_scraper.py - make a call to the Frido Sleigh CAPTEHA and store each image & label. Run repeated times to collect a body of training samples, which must then be manually classified.
retrain.py - builds an image-recognition model based on training data.
predict_images.py - feeds images through the ML model to determine their classification.
predict_capteha.py - makes a call to the Frido Sleigh CAPTEHA, feeds data through the ML model, and submits a CAPTEHA response.
capteha_bypass.py - defeats the Frido Sleigh CAPTEHA and submits repeated competition entries.
