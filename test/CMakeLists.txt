add_executable(run_tests test.cpp)

target_link_libraries(run_tests PRIVATE word_printer_lib)

add_test(NAME UnitTests COMMAND run_tests)
