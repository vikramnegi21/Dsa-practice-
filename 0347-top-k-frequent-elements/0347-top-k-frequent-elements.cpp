class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        
        int n =nums.size();
        unordered_map<int,int>mp;
        for(int x:nums){
            mp[x]++;
        }
        vector<pair<int,int>>ans;
        for(auto it :mp){
        ans.push_back({it.second,it.first});
        }
        vector<int>result;
        sort(ans.rbegin(),ans.rend());
        for(int i=0;i<k;i++){
            result.push_back(ans[i].second);
        }
        return result;
    }
};