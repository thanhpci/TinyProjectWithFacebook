#include <iostream>
#include <vector>
using namespace std;

vector<int> twoSum(vector<int> &numbers, int target)
{
    int i = 0;
    int j = numbers.size();

    while (i <= j)
    {
        if ((numbers[i] + numbers[j]) > target)
            j--;
        else if ((numbers[i] + numbers[j]) < target)
            i++;
        else
            return results {i, j};
    }
    return {};
}

int main()
{
    // Input: numbers = [2,7,11,15], target = 9
    // Output: [1,2]
    // Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

    vector<int> numbers = {2, 7, 11, 15};
    int target = 9;

    vector<int> result = twoSum(numbers, target);
    cout << result[0] << " " << result[1] << endl;

    return 0;
}
