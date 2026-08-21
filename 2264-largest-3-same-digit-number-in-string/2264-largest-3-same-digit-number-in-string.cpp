class Solution {
public:
    string largestGoodInteger(string num) {
        int n=num.length();
        int maxii=INT_MIN;
        
        for(int i=0;i<n-2;i++){
            if(num[i]==num[i+1]&&num[i+1]==num[i+2]){
                
            

        
        maxii=max(num[i]-'0',maxii);
            }
        }
        if(maxii == INT_MIN)
            return "";

        return string(3,maxii+'0');
        
    }
};