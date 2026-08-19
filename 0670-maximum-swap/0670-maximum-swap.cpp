class Solution {
public:
    int maximumSwap(int num)  {
     string s=to_string(num);
     for(int i=0;i<s.size();i++){
        int maxi=i;
        for(int j=i+1;j<s.size();j++){
            if (s[j]>=s[maxi]){
                maxi=j;
            }
        }
        if(s[maxi]>s[i]){
            swap(s[i],s[maxi]);
            break;
        }
     }
     return stoi(s);
        
    }
};