cmake_minimum_required(VERSION 3.0)

set(TARGET **target filename**)

#-----------------------------------------------------------------------------#

find_package(OpenCV REQUIRED)

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_C_COMPILER gcc)

#-----------------------------------------------------------------------------#

add_subdirectory()

add_executable(${TARGET} **source files**)

add_library(${TARGET} STATIC **source files**)

target_link_libraries(${TARGET} ${OpenCV_LIBS} 
								**lib**
)

target_include_directories(${TARGET} PUBLIC ${OpenCV_INCLUDE_DIRS}
											**dirs**
)

#-----------------------------------------------------------------------------#

target_compile_options(${TARGET} PUBLIC -std=gnu++11
										-Wall
										-Werror
										-O2
)

#-----------------------------------------------------------------------------#

install(TARGETS ${TARGET} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/bin)