class Solution {
public:
void dfs(vector<vector<int>>& isConnected,int node,vector<int>&vis){
    int n=isConnected.size();
    vis[node]=1;
    for(int i=0;i<n;i++){
    
        if(isConnected[node][i]==1&&vis[i]==0){
            dfs(isConnected,i,vis);
        
        }
    }
}
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n=isConnected.size();
        int cnt=0;
        vector<int>vis(n,0);
        for(int i=0;i<n;i++){
            if(vis[i]==0){
                cnt++;
                dfs(isConnected,i,vis);
            }
        }
        return cnt;
        
    }
};