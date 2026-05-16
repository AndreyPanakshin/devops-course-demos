#include <iostream>
#include <string>
#include "word_printer.h"

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <word>" << std::endl;
        return 1;
    }

    std::string word = argv[1];
    std::cout << generateRepeatedWord(word) << std::endl;

    return 0;
}
