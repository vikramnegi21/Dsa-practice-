class Solution {
public:
    int smallestIndex(vector<int>& nums) {

        int n = nums.size();

        for(int i = 0; i < n; i++) {

            int x = nums[i];
            int sum = 0;

            while(x > 0) {
                int a = x % 10;
                sum += a;
                x = x / 10;
            }

            if(i == sum) {
                return i;
            }
        }

        return -1;
    }
};