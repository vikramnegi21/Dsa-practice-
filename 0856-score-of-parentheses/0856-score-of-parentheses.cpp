class Solution {
public:
    int scoreOfParentheses(string s) {
        stack<int> st;
        int count = 0;

        for(char ch : s) {
            if(ch == '(') {
                st.push(count);
                count = 0;
            }
            else {
                if(count == 0) {
                    count = 1;
                }
                else {
                    count = 2 * count;
                }

                count += st.top();
                st.pop();
            }
        }

        return count;
    }
};