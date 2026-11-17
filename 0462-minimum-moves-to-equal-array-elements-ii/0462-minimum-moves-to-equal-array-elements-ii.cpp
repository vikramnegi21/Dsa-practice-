class Solution {
public:
    int minMoves2(vector<int>& nums) {
        
        sort(nums.begin(),nums.end());
        int ans=0;
         int mid = nums[nums.size()/2];
        for(int x:nums){
            ans+=abs(x-mid);
        }
        return ans;
    }
};