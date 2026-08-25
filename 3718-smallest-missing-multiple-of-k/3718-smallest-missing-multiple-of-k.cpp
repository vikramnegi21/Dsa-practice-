class Solution {
public:
    int missingMultiple(vector<int>& nums, int k) {
        int n = nums.size();

        unordered_set<int> mp(nums.begin(), nums.end());
        for (int i = 1;; i++) {
            if (mp.find(i) == mp.end() && i % k == 0) {
                return i;
            }
        }
        return 0;
    }
};