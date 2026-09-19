class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int n =grid.size();
        int m=grid[0].size();
        vector<vector<int>>vis(n,vector<int>(m,0));
        queue<pair<pair<int,int>,int>>q;
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(grid[i][j]==2){
                    q.push({{i,j},0});
                    vis[i][j]=2;
                }
                else{
                    vis[i][j]=0;
                }
            }
        }


        int drow[]={-1,0,1,0};
        int dcol[]={0,1,0,-1};
        int tm=0;
    while(!q.empty()){
        int r=q.front().first.first;
        int c=q.front().first.second;
        int t=q.front().second;

        q.pop();
        tm=max(tm,t);

        for(int i=0;i<4;i++){
            int ro=r+drow[i];
            int co=c+dcol[i];
            if(ro>=0&&ro<n&&co>=0&&co<m&&vis[ro][co]!=2&& grid[ro][co]==1){
                q.push({{ro,co},t+1});
                vis[ro][co]=2;

            }
        }



    }
    for(int i=0;i<n;i++){
        for(int  j=0;j<m;j++){
            if(vis[i][j]!=2&&grid[i][j]==1){
                return -1;
            }
        }
    }
    return tm ;

        
    }
};