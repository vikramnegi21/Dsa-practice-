class Solution {
public:
    vector<int> smallerNumbersThanCurrent(vector<int>& nums) {
        vector<int>result=nums;
        sort(result.begin(),result.end());
        vector<int>ans;
    for(int i=0;i<nums.size();i++){
        int j=0;
        while(nums[i]!=result[j]){
            j++;
        }
        ans.push_back(j);
    }
    return ans;
    }
};