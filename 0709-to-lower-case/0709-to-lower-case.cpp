class Solution {
public:
    string toLowerCase(string s) {
        string ans="";
        for(char h :s){
            ans.push_back(tolower(h));
        }
        return ans ;
        
    }
};