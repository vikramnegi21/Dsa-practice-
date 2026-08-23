class Solution {
public:
    vector<int> smallerNumbersThanCurrent(vector<int>& nums) {
    int n=nums.size();
    vector<int>ans;
    for(int i=0;i<n;i++){
        int j=0;
        int count=0;
        while(j<n){
            if(nums[i]>nums[j]){
                count++;
            }
            j++;
        }
                    ans.push_back(count);


    }
    return ans;
        
    }
};