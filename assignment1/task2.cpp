#include <iostream>
#include <vector>
#include <random>
#include <omp.h>

std::vector<std::vector<int>> generateRandomMatrix(int size)
{
    std::vector<std::vector<int>> matrix(size, std::vector<int>(size));
    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_int_distribution<int> dist(0, 9);

    for (auto& row : matrix)
    {
        for (int& element : row)
        {
            element = dist(mt);
        }
    }

    return matrix;
}

void multiplyMatrices(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& result)
{
#pragma omp parallel for collapse(2)
    for (size_t i = 0; i < A.size(); ++i)
    {
        for (size_t j = 0; j < B[0].size(); ++j)
        {
            result[i][j] = 0;
            for (size_t k = 0; k < A[0].size(); ++k)
            {
                result[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

double measureMatrixMultiplicationTime(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& result, int loopOrder, int numThreads)
{
    double startTime, endTime;

    for (size_t i = 0; i < A.size(); ++i)
    {
        for (size_t j = 0; j < B[0].size(); ++j)
        {
            result[i][j] = 0;
        }
    }

    startTime = omp_get_wtime();

    if (loopOrder == 0)
    {
#pragma omp parallel for collapse(3) num_threads(numThreads)
        for (size_t i = 0; i < A.size(); ++i)
        {
            for (size_t j = 0; j < B[0].size(); ++j)
            {
                for (size_t k = 0; k < A[0].size(); ++k)
                {
                    result[i][j] += A[i][k] * B[k][j];
                }
            }
        }
    }
    else if (loopOrder == 1)
    {
#pragma omp parallel for collapse(3) num_threads(numThreads)
        for (size_t i = 0; i < A.size(); ++i)
        {
            for (size_t k = 0; k < A[0].size(); ++k)
            {
                for (size_t j = 0; j < B[0].size(); ++j)
                {
                    result[i][j] += A[i][k] * B[k][j];
                }
            }
        }
    }
    else if (loopOrder == 2)
    {
#pragma omp parallel for collapse(3) num_threads(numThreads)
        for (size_t j = 0; j < B[0].size(); ++j)
        {
            for (size_t i = 0; i < A.size(); ++i)
            {
                for (size_t k = 0; k < A[0].size(); ++k)
                {
                    result[i][j] += A[i][k] * B[k][j];
                }
            }
        }
    }

    endTime = omp_get_wtime();

    return endTime - startTime;
}

void runMatrixMultiplicationExperiment(int matrixSize)
{
    std::vector<std::vector<int>> matrixA = generateRandomMatrix(matrixSize);
    std::vector<std::vector<int>> matrixB = generateRandomMatrix(matrixSize);
    std::vector<std::vector<int>> result(matrixSize, std::vector<int>(matrixSize));

    for (int loopOrder = 0; loopOrder < 3; ++loopOrder)
    {
        const char* loopOrderStr[] = {"i-j-k", "i-k-j", "j-i-k"};

        for (int numThreads = 1; numThreads <= 10; ++numThreads)
        {
            double executionTime = measureMatrixMultiplicationTime(matrixA, matrixB, result, loopOrder, numThreads);

            std::cout << "Loop Order: " << loopOrderStr[loopOrder] << "\tThreads: " << numThreads
                      << "\tExecution Time: " << executionTime << " seconds\tEfficiency: "
                      << (executionTime / ((numThreads == 1) ? executionTime : executionTime / numThreads))
                      << std::endl;
        }
    }
}

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " matrix_size" << std::endl;
        return 1;
    }

    int matrixSize = std::stoi(argv[1]);

    if (matrixSize < 1)
    {
        std::cerr << "Matrix size should be at least 1." << std::endl;
        return 1;
    }

    runMatrixMultiplicationExperiment(matrixSize);

    return 0;
}
