class Solution {
public:
    vector<int> eventualSafeNodes(vector<vector<int>>& graph) {
        int n=graph.size();
        vector<vector<int>> rev(n); 
        vector<int>in(n,0);
        vector<int>ans;
        queue<int>q;
        for(int i=0;i<n;i++){
            for(auto it:graph[i]){
                rev[it].push_back(i);
                in[i]++;
            }
        }
        for(int i=0;i<n;i++){
            if(in[i]==0){
                q.push(i);

                
            }
        }
           while(!q.empty()){
            int node=q.front();
            q.pop();
            ans.push_back(node);
            for(auto it:rev[node]){
                in[it]--;
                if(in[it]==0){
                    q.push(it);
                
           }

            }
        }
        sort(ans.begin(),ans.end());
        return ans;
        
    }
};