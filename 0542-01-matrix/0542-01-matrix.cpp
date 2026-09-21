class Solution {
public:
    vector<vector<int>> updateMatrix(vector<vector<int>>& mat) {
        
        int n=mat.size();
        int m=mat[0].size();
        queue<pair<pair<int,int>, int >>q;
        vector<vector<int>>vis(n,vector<int>(m,0));
         vector<vector<int>>dis(n,vector<int>(m,0));

         for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(mat[i][j]==0){
                    q.push({{i,j},0});
                    vis[i][j]=1;
                }
                else{
                    vis[i][j]=0;
                }
            }
         }
         int dro[]={-1,0,1,0};
         int dco[]={0,1,0,-1};
         while(!q.empty()){
            int r=q.front().first.first;
            int c=q.front().first.second;
            int a=q.front().second;
            q.pop();
            dis[r][c]=a;
            for(int i=0;i<4;i++){
                int ro=r+dro[i];
                int co=c+dco[i];
                if(ro>=0&&ro<n&&co>=0&&co<m&& vis[ro][co]==0){
                 
                    vis[ro][co]=1;
                       q.push({{ro,co},a+1});
                }

            }
         }
         return dis;
    }
};