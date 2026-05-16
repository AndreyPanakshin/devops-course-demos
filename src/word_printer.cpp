#include "word_printer.h"
#include <iostream>

std::string generateRepeatedWord(const std::string& word) {
    if (word.empty()) {
        return "";
    }
    std::string result = "";
    for (size_t i = 0; i < word.length(); ++i) {
        result += word;
        if (i < word.length() - 1) {
            result += " ";
        }
    }
    return result;
}
