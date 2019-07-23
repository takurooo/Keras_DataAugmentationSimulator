# Keras_DataAugmentationSimulator
  
 Simulation for [Keras ImageDataGenerator](https://keras.io/ja/preprocessing/image/).



![sample](https://user-images.githubusercontent.com/35373553/61723441-1da4e400-ada7-11e9-982b-e602c43c9776.gif)


# Requirement
- PIL
- numpy
- matplotlib
- Keras


# Usage
```
python main.py <img_path>
```
Open a window as below.
![sample1](https://user-images.githubusercontent.com/35373553/61723891-d4a15f80-ada7-11e9-9968-18db13b73c45.png)

Simulator starts when you set parameters.


| widget  | name         | Description | 
| ---     | ---          | ---                                           |
| Slider  | rotate       | Degree range for random rotations.            |
| Slider  | width_shift  | Fraction of total width.                      |
| Slider  | height_shift | Fraction of total height.                     |
| Slider  | shear        | Shear Intensity.                              |
| Slider  | zoom         | Range for random zoom.                        |
| Slider  | interval     | Display interval (sec)                        |
| Button  | quit         | Quit simulation.                              |
| Button  | start        | Start simulator.                              |
| Button  | stop         | Stop simulator.                               |