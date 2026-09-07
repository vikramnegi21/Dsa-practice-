class Solution {
public:
    int minStoneSum(vector<int>& piles, int k) {
        int n=piles.size();
        int i=0;int sum=0;
        vector<int>ans;
       priority_queue<int>pq(piles.begin(),piles.end());

       while(pq.size()>0 && i<k){
        int a=pq.top();
        pq.pop();
        int ans=a/2;
        pq.push(a-ans);
        i++;
       }
       while(pq.size()>0){
        sum+=pq.top();
        pq.pop();
       }
       return sum;

        }
};