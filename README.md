# COE506-Project

## Building

install opencv library

```bash
sudo apt install libopencv-dev
```

for python, you have to install opencv through pip

```bash
pip3 install opencv-python
```

### C

goto c directary and use cmake to build the application

```bash
cd c
mkdir build && cd build
cmake ..
make
```

and then if everything run smothly, you can launch the application

```bash
./median #seq c
./image_cuda_median #cuda c
./video_cuda_median #cuda c
./video_cuda_median videos_2_1080p.mp4
```

or alternatively, you can use the following link to dirtectly build it

```bash
g++ -std=c++11 -I/usr/local/include/opencv4  -L/usr/local/lib -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui median_filter.cpp -o median_filter
```

## Python

```
cd python
python median_filter.py 
```

## Results

to profile nsys

```bash
nsys profile --stats=true ./cuda_median
```

### sp_img_gray_noise_heavy

| Method     | Total Time | Kernal Time | Transfer Time |
| ---------- | ---------- | ----------- | ------------- |
| OpenCV     |            |             |               |
| Seq C      |            |             |               |
| Seq Python |            |             |               |
| CUDA C     |            |             |               |
| OpenACC    |            |             |               |
| CUDA Pyton |            |             |               |