class Solution {
public:
    int minimumEffortPath(vector<vector<int>>& heights) {
       // priority_queue<pair<int,pair<int,int>>,vector<pair<int,pair<int,int>>,greater<pair<int,pair<int,int>>>>q;
       priority_queue<pair<int,pair<int,int>>, vector<pair<int,pair<int,int>>>, greater<pair<int,pair<int,int>>>> q;
        

        int m=heights.size();
         int n=heights[0].size();
         vector<vector<int>>dis(m,vector<int>(n,1e9));
         dis[0][0]=0;
         q.push({0,{0,0}});
         int dr[]={-1,0,1,0};
         int dc[]={0,1,0,-1};
         while(!q.empty()){
            auto it=q.top();
            q.pop();
            
            int diff=it.first;
            int r=it.second.first;
            int c=it.second.second;
if(r==m-1&&c==n-1){
    return diff;
}

            for( int i=0;i<4;i++){
                int nr=r+dr[i];
                int nc=c+dc[i];
            
            if(nr>=0&&nr<m&&nc>=0&&nc<n){
                int neww=max(abs(heights[r][c]-heights[nr][nc]),diff);
                if(neww<dis[nr][nc]){
                    dis[nr][nc]=neww;
                
                q.push({neww,{nr,nc}});
                }
            }
            }
         }
         return 0;

        
    }
};