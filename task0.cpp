#include <iostream>
#include <sstream>
#include <string>

int countWords(std::string& line) {
    const std::string escapeSequences[] = {"\\n", "\\t", "\\s"};
    int wordCount = 0;

    for (const auto& escape : escapeSequences) {
        size_t found = line.find(escape);
        while (found != std::string::npos) {
            line.replace(found, escape.length(), " ");
            found = line.find(escape, found + 1);
        }
    }

    std::istringstream stream(line);
    std::string word;
    while (stream >> word) {
        ++wordCount;
    }

    return wordCount;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " 'enter your string here'" << std::endl;
        return 1;
    }

    std::string inputString = argv[1];
    int wordCount = countWords(inputString);
    std::cout << "Number of words: " << wordCount << std::endl;

    return 0;
}
