class Solution {
public:
    int distributeCandies(vector<int>& candyType) {
unordered_set<int> st(candyType.begin(), candyType.end());
int n=candyType.size();
    if(st.size() == 1)
        return 1;

    return min(n/2,(int)st.size());
        
        
    }
};