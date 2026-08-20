class Solution {
public:
    vector<int> resultArray(vector<int>& nums) {
        int n=nums.size();
        vector<int>arr1;
        vector<int>arr2;
        vector<int>ans;
        for(int i=0;i<n;i++){
            arr1.push_back(nums[i]);
            break;
        }
        for(int i=1;i<n;i++){
            arr2.push_back(nums[i]);
            break;
        }
        for(int i=2;i<n;i++){
            if(arr1.back()>arr2.back()){
                arr1.push_back(nums[i]);
            }
            else{
                arr2.push_back(nums[i]);
            }
        }
        for(int i=0;i<arr1.size();i++){
            ans.push_back(arr1[i]);
        }
        for(int i=0;i<arr2.size();i++){
            ans.push_back(arr2[i]);
        }
        return ans;
        
    }
};