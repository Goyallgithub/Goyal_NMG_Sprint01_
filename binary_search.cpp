#include <iostream>
#include <vector>
#include <algorithm>

/**
 * Performs a binary search on a sorted vector to find the index of a target element.
 *
 * @param arr The sorted vector to search through.
 * @param target The value to search for.
 * @return The index of the target if found, otherwise -1.
 */
int binarySearch(const std::vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2; // Prevents overflow for large indices

        if (arr[mid] == target) {
            return mid;
        }
        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1; // Target not found
}

int main() {
    // Binary search requires a sorted array
    std::vector<int> data = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};

    int targets[] = {23, 2, 91, 100, 5};

    std::cout << "Searching in array: ";
    for (int x : data) std::cout << x << " ";
    std::cout << "\n\n";

    for (int target : targets) {
        int result = binarySearch(data, target);
        if (result != -1) {
            std::cout << "Element " << target << " found at index " << result << "\n";
        } else {
            std::cout << "Element " << target << " not found in the array\n";
        }
    }

    return 0;
}
