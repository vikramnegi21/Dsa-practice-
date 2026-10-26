class Solution {
public:
    int shortestPathBinaryMatrix(vector<vector<int>>& grid) {
        int n=grid.size();
        queue<pair<int,pair<int,int>>>q;
              vector<vector<int>> vis(n, vector<int>(n, 0));

        if(grid[0][0]==1||grid[n-1][n-1]==1){
            return -1;
        }
            q.push({1,{0,0}});
            vis[0][0]=1;
            int dr[]={-1,-1,-1,0,0,1,1,1};
            int dc[]={-1,0,1,-1,1,-1,0,1};
            while(!q.empty()){
                auto it=q.front();
                q.pop();
                int dist=it.first;
               
                int r = it.second.first;

                auto c=it.second.second;
                if(r==n-1&&c==n-1){
                    return dist;
                }
                for(int i=0;i<8;i++){
                    int nr=r+dr[i];
                    int nc=c+dc[i];
                
                if(nr>=0&&nr<n&&nc>=0&&nc<n&&!vis[nr][nc]&&grid[nr][nc]==0){
                    vis[nr][nc]=1;
                    q.push({dist+1,{nr,nc}});
                }
                }
            }
        
        return -1;
    }
};