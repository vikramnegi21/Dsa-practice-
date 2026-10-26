class Solution {
public:
int  m;
int  n;
long long  dfs(vector<vector<int>>& grid, int r,int c){
   if (r < 0 || r >= m || c < 0 || c >= n ||
            grid[r][c] == 0) {
            return 0;
            }
    long long  sum=    grid[r][c];
grid[r][c]=0;
        long long left=dfs(grid,r,c-1);
    long long  right=dfs(grid,r,c+1);
    long long up=dfs(grid,r-1,c);
    long long down=dfs(grid,r+1,c);
    return sum+=left+right+up+down;
    
        
    
}
    int countIslands(vector<vector<int>>& grid, int k) {
        m=grid.size();
n=grid[0].size();
int  count=0;
for(long long  i=0;i<m;i++){
    
    for(long long  j=0;j<n;j++){
        if(grid[i][j]>0){
            
            if(dfs(grid,i,j)%k==0){
                count++;
            }
        }
    }
}
return count;
    }
};