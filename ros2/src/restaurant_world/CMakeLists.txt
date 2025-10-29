cmake_minimum_required(VERSION 3.5)
project(restaurant_world)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

find_package(ament_cmake REQUIRED)

# Install directories (all exist based on earlier ls output)
install(
  DIRECTORY 
    launch
    worlds 
    models 
    params
    maps
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()