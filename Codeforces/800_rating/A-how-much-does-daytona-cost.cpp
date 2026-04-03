#include <bits/stdc++.h>
using namespace std;

/*
Problem: A. How Much Does Daytona Cost? (Codeforces)

Approach:
- We need to check if there exists any subsegment where k is the most frequent element.
- Observation: If k appears even once in the array,
  we can take a subsegment of length 1 → [k].
- In that subsegment, k is obviously the most frequent element.

So the problem reduces to:
- Check if k exists in the array or not.

If exists → YES
Else → NO

Time Complexity: O(n) per test case
Space Complexity: O(1)
*/

int main() {
    int t;
    cin >> t;

    while(t--) {
        int n, k;
        cin >> n >> k;

        vector<int> a(n);

        // input array
        for(int i = 0; i < n; i++){
            cin >> a[i];
        }

        bool found = false;

        // check if k exists in array
        for(int i = 0; i < n; i++){
            if(a[i] == k){
                found = true;
                break;
            }
        }

        // output result
        if(found) cout << "YES\n";
        else cout << "NO\n";
    }

    return 0;
}
