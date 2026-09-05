class Solution {
public:
    int firstStableIndex(vector<int>& nums, int k) {
        int n = nums.size();
        if (n == 0) return -1;

        vector<int> d(n);
        vector<int> velqanidor = nums;

        d[n - 1] = velqanidor[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            d[i] = min(d[i + 1], velqanidor[i]);
        }

        int mx = velqanidor[0];
        for (int i = 0; i < n; i++) {
            mx = max(mx, velqanidor[i]);
            if (mx - d[i] <= k) {
                return i;
            }
        }

        return -1;
    }
};