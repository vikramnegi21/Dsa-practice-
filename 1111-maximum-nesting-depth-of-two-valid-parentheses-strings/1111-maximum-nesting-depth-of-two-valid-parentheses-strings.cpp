class Solution {
public:
    vector<int> maxDepthAfterSplit(string seq) {
        vector<int>ans;
        stack<int>st;
        for(char ch:seq){
            if(ch=='('){
                st.push(ch);
                ans.push_back(st.size()%2);
            }
            else {
                ans.push_back(st.size()%2);
                st.pop();
            }
        }
        return ans;
        
    }
};