class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {

        int n = nums.size();
        unordered_map<int, int> mp;
        for (int x : nums) {
            mp[x]++;
        }
        priority_queue<pair<int, int>> q;
        for (auto it : mp) {
            q.push({it.second, it.first});
          
        }
        vector<int> ans;
        while (k--) {
            ans.push_back(q.top().second);
              q.pop();
        }
        return ans;
    }
};