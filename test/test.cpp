#include "word_printer.h"
#include <cassert>
#include <iostream>

void test_empty_string() {
    assert(generateRepeatedWord("") == "");
    std::cout << "Test test_empty_string passed." << std::endl;
}

void test_short_word() {
    assert(generateRepeatedWord("cat") == "cat cat cat");
    std::cout << "Test test_short_word passed." << std::endl;
}

void test_one_letter_word() {
    assert(generateRepeatedWord("a") == "a");
    std::cout << "Test test_one_letter_word passed." << std::endl;
}

int main() {
    test_empty_string();
    test_short_word();
    test_one_letter_word();

    std::cout << "All tests passed." << std::endl;

    return 0;
}
