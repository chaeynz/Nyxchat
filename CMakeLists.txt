cmake_minimum_required(VERSION 3.25.1)
project(Nyxchat)

set(CMAKE_CXX_STANDARD 14)

# Include directories for header files
include_directories(include)

# Add subdirectories
add_subdirectory(src)
add_subdirectory(include/core)
