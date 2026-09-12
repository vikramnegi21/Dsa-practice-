class Solution {
public:
    long long totalCost(vector<int>& costs, int k, int candidates) {
        
        long long  ans=0;
        long long  hired=0;
        int n=costs.size();
        int i=0;
        int j=n-1;
        priority_queue<int,vector<int>,greater<int>>q1,q2;
        while(hired<k){
            while(q1.size()<candidates&&i<=j){
                q1.push(costs[i]);
                i++;
            }
            while(q2.size()<candidates&&j>=i){
                q2.push(costs[j]);
                j--;
            }
                        int min_q1 = q1.empty() ? INT_MAX : q1.top();
            int min_q2 = q2.empty() ? INT_MAX : q2.top();

            if(min_q1<=min_q2){
                ans+=min_q1;
                q1.pop();
            }
            else{
                ans+=min_q2;
                q2.pop();
            }
            hired++;
        }
        return ans;

    }
};