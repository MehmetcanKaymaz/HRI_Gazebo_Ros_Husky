
world_file="$(pwd)/worlds/level3.world"
echo $world_file
roslaunch husky_gazebo husky_empty_world.launch world_name:="$world_file" &
