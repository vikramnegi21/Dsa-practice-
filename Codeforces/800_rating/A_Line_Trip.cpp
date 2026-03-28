/*
    Problem: A. Line Trip
    Platform: Codeforces
    Rating: 800
    Approach: Greedy

    Idea:
    - Start from 0
    - Find max gap between consecutive points
    - Also consider last to x (double distance)
*/

#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    cin >> t;

    while(t--) {
        int n, x;
        cin >> n >> x;

        vector<int> a(n);
        for(int i = 0; i < n; i++) {
            cin >> a[i];
        }

        int last = 0;
        int ans = 0;

        for(int i = 0; i < n; i++) {
            ans = max(ans, a[i] - last);
            last = a[i];
        }

        // last point to x (important)
        ans = max(ans, 2 * (x - last));

        cout << ans << endl;
    }

    return 0;
}
