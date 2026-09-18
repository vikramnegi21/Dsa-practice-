class Solution {
public:
    int maxArea(vector<int>& height) {
        int maxwater=0;
        int lp=0,rp=height.size()-1;
        while(lp<rp){
            int width= rp-lp;
          int   ht=min(height[lp], height [rp]);
            int cw=ht*width;
            maxwater=max(cw,maxwater);
            height[lp] < height[rp] ? lp++ : rp--;
            
        }
        return maxwater;
        
    }
};