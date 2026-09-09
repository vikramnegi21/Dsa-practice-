class Solution {
public:
    string frequencySort(string s) {
        unordered_map<char,int>mp;
        for(char ch:s){
            mp[ch]++;
        }
        string ans="";
        priority_queue<pair<int,char>>q;
        for(auto it:mp){
            q.push({it.second,it.first});
        }
        while(!q.empty()){
            int freq=q.top().first;
            char ch =q.top().second;

            q.pop();
            while(freq--){
                ans+=ch;
            }
        }

        return ans;
    }
};