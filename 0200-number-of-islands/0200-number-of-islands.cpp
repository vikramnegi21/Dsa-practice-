class Solution {
public: 
void bfs(int i,int j, vector<vector<int>>&vis,vector<vector<char>>& grid){
    vis[i][j]=1;
    int n =grid.size();
    int m=grid[0].size();
    queue<pair<int,int>>q;
    q.push({i,j});
    int dro[]={-1,0,1,0};
   int dco[]={0,1,0,-1};
  while(!q.empty()){
    int r=q.front().first;
    int c=q.front().second;


q.pop();
for(int i=0;i<4;i++){
    int ro=r+dro[i];
    int co=c+dco[i];
    if(ro>=0&&ro<n&&co>=0&&co<m&&vis[ro][co]==0&&grid[ro][co]=='1'){
        q.push({ro,co});
        vis[ro][co]=1;

    }
}    
  }


 





}
    int numIslands(vector<vector<char>>& grid) {
        int n=grid.size();
        int m=grid[0].size();
        vector<vector<int>>vis(n,vector<int>(m,0));
        int count =0;
        
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
             if(grid[i][j]=='1'&& vis[i][j] == 0){
                count++;
                bfs(i,j,vis,grid);
             }
             else{
                vis[i][j]=0;
             }   
            }
        }
        return count;
        

    }
};