cmake_minimum_required(VERSION 3.0)

set(TARGET **target name**)

#-----------------------------------------------------------------------------#

add_subdirectory(**pathA pathB**)

add_library(${TARGET} STATIC **source files**)

target_link_libraries(${TARGET} ${TIVAWARE_PATH}/driverlib/gcc/libdriver.a
								**lib**
)

target_include_directories(${TARGET} PRIVATE ${TIVAWARE_PATH} 
											**dirs**
)

#-----------------------------------------------------------------------------#

target_compile_options(${TARGET} PUBLIC -std=gnu11
										-mthumb
										${CPU}
										${FPU}
										${FLOAT}
										-ffunction-sections 
										-fdata-sections    
										-MD                                         
										-pedantic           
										-O2
										-Wall
										-Werror
)

target_compile_definitions(${TARGET} PUBLIC TARGET_IS_${REV}
											PART_${MCU}
)

#-----------------------------------------------------------------------------#

#install(TARGETS ${TARGET} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/bin)