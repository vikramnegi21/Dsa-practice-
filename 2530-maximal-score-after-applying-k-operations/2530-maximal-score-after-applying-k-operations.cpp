class Solution {
public:
    long long maxKelements(vector<int>& nums, int k) {
    priority_queue<int>q(nums.begin(),nums.end());
    long long sum=0;
    while(k--){
        int mx=q.top();
         sum+=mx;
         q.pop();
         mx=ceil(mx / 3.0);
        q.push(mx);
    }
    return sum;
        
    }
};