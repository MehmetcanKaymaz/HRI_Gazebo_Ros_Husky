cd ../../../
catkin_make &&
source devel/setup.bash
cd src/limitless_ai/src
rosrun limitless_ai vision.py __name:=vision_system &
rosrun limitless_ai ui.py __name:=ui_system
