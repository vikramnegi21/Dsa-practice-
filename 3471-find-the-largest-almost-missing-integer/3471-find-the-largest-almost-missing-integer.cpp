class Solution {
public:
    int largestInteger(vector<int>& nums, int k) {
        unordered_map<int,int>mp;
        int n=nums.size();


        for(int i=0;i<=n-k;i++){
                    unordered_set<int>st;

            for(int j=i;j<i+k;j++){
            st.insert(nums[j]);
            
        }
        for(auto it:st){
            mp[it]++;
        }
        }
        int maxx=INT_MIN;
        for(auto m:mp){
            if(m.second==1&&m.first>maxx){
maxx=m.first;
            }
        }
    if(maxx==INT_MIN){
        return -1;
    }
    else {
        return maxx;
    }
    }
};