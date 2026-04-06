#include <bits/stdc++.h>
using namespace std;

int threeSumClosest(vector<int>& nums, int target) {

    /*
    🧠 Approach:

    1. Hume 3 elements ka sum chahiye jo target ke sabse closest ho.

    2. Pehle array ko sort karenge.
       → Taaki two-pointer technique use kar sake.

    3. Har index i ke liye:
       - left = i + 1
       - right = n - 1

    4. Sum nikalo:
       sum = nums[i] + nums[left] + nums[right]

    5. Agar ye sum target ke closer hai previous answer se:
       → update answer

    6. Pointer movement:
       - Agar sum < target → left++
       - Agar sum > target → right--
       - Agar sum == target → exact match → return sum

    7. Final answer = jo sum target ke sabse closest ho.

    ⏱️ Time Complexity: O(n^2)
    */

    sort(nums.begin(), nums.end());

    int n = nums.size();
    int closestSum = nums[0] + nums[1] + nums[2];

    for(int i = 0; i < n - 2; i++) {
        int left = i + 1;
        int right = n - 1;

        while(left < right) {
            int sum = nums[i] + nums[left] + nums[right];

            // update closest sum
            if(abs(target - sum) < abs(target - closestSum)) {
                closestSum = sum;
            }

            if(sum < target) {
                left++;
            }
            else if(sum > target) {
                right--;
            }
            else {
                return sum; // exact match
            }
        }
    }

    return closestSum;
}
