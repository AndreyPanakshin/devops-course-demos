add_library(word_printer_lib word_printer.cpp)

add_executable(word_printer main.cpp)

target_include_directories(word_printer_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(word_printer PRIVATE word_printer_lib)
