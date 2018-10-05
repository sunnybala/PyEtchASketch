# PyEtchASketch
Drawing pictures using an etch a sketch, motors and python.

I did the image analysis (EtchASketch.py) on my PC. It generates a path in the Paths/ folder. 
I then ran pictureDraw.py (which imports stepperMotor.py) on my raspberry pi to actually draw the images. You'll need to adjust these files to calibrate for your specific build.

A few sample images ad their outputs are pre-populated. I used sigma parameters between .33 and 1. n


A Quick Tutorial to get started:

Place 'PyEtchASketch' folder on your RaspberryPi. For this example located: ~/Desktop/PyEtchASketch

From Terminal:


pi@raspberrypi:~ $ sudo apt-get install pip
pi@raspberrypi:~ $ pip install pandas
pi@raspberrypi:~ $ cd ~/Desktop
pi@raspberrypi:~/Desktop $ git clone https://github.com/sunnybala/PyEtchASketch.git
pi@raspberrypi:~ $ cd ~/Desktop/PyEtchASketch
pi@raspberrypi:~/Desktop/PyEtchASketch $ python