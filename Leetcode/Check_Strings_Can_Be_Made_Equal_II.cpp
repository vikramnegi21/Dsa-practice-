#include <bits/stdc++.h>
using namespace std;

/*
🧩 LeetCode 2840 - Check if Strings Can be Made Equal With Operations II

🧠 Approach (Frequency Count - Optimal):
- Even indices apas me swap ho sakte hain
- Odd indices apas me swap ho sakte hain

👉 Isliye:
- Even positions ke characters ka frequency same hona chahiye
- Odd positions ke characters ka frequency same hona chahiye

⚙️ Steps:
1. 2 arrays banao:
   - even[26]
   - odd[26]

2. s1 ke liye:
   - even index → increment
   - odd index → increment

3. s2 ke liye:
   - even index → decrement
   - odd index → decrement

4. Agar sab values 0 ho → return true

⏱️ Complexity:
- Time: O(n)
- Space: O(1)

🏷️ Tags:
- Strings
- Hashing
- Greedy
*/

class Solution {
public:
    bool canBeEqual(string s1, string s2) {

        vector<int> even(26, 0), odd(26, 0);

        for(int i = 0; i < s1.size(); i++) {
            if(i % 2 == 0) {
                even[s1[i] - 'a']++;
                even[s2[i] - 'a']--;
            } else {
                odd[s1[i] - 'a']++;
                odd[s2[i] - 'a']--;
            }
        }

        // Check all zero
        for(int i = 0; i < 26; i++) {
            if(even[i] != 0 || odd[i] != 0)
                return false;
        }

        return true;
    }
};
