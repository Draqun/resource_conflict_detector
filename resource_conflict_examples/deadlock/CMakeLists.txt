cmake_minimum_required (VERSION 3.10)
project (deadlock_example)

find_package(Threads)

set(VERSION_MAJOR 1)
set(VERSION_MINOR 0)
set(BINARY_NAME deadlock_example)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Werror -g")
set(CMAKE_CXX_STANDARD 17)

include_directories(".")

add_executable(${BINARY_NAME} deadlock.cpp helpers.cpp helpers.hpp)
target_link_libraries(${BINARY_NAME} ${CMAKE_THREAD_LIBS_INIT})
