class Solution {
public:
    int firstStableIndex(vector<int>& nums, int k) {
        int n = nums.size();

        int maxi = INT_MIN;
        int mini = INT_MAX;

        for (int i = 0; i < n; i++) {

            maxi = max(maxi, nums[i]);

            mini = INT_MAX;

            for (int j = i; j < n; j++) {
                mini = min(mini, nums[j]);
            }

            if (maxi - mini <= k) {
                return i;
            }
        }

        return -1;
    }
};