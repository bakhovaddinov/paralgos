#include <iostream>
#include <vector>
#include <random>
#include <ctime>
#include <omp.h>

std::vector<int> generateRandomVector(int size) {
    std::vector<int> vector(size);
    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_int_distribution<int> dist(0, 999);

    for (int i = 0; i < size; ++i) {
        vector[i] = dist(mt);
    }

    return vector;
}

int findMaxElementParallel(const std::vector<int>& vector, int numThreads) {
    int maxElement = 0;

    omp_set_num_threads(numThreads);

#pragma omp parallel for reduction(max : maxElement)
    for (int i = 0; i < vector.size(); ++i) {
        if (vector[i] > maxElement) {
            maxElement = vector[i];
        }
    }

    return maxElement;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " array_size" << std::endl;
        return 1;
    }

    int arraySize = std::stoi(argv[1]);

    if (arraySize < 1) {
        std::cerr << "Array size should be at least 1." << std::endl;
        return 1;
    }

    std::vector<int> vector = generateRandomVector(arraySize);

    for (int numThreads = 1; numThreads <= 10; ++numThreads) {
        int maxElement = 0;
        double startTime = omp_get_wtime();

        maxElement = findMaxElementParallel(vector, numThreads);

        double endTime = omp_get_wtime();

        std::cout << "Threads: " << numThreads
                  << "\tExecution Time: " << std::fixed << endTime - startTime << " seconds"
                  << "\tMax Element: " << maxElement << std::endl;
    }

    return 0;
}
