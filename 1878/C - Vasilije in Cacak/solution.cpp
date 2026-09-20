#include <iostream>
using namespace std;
 
void solve() {
    long long n, k, x;
    cin >> n >> k >> x;
 
    // Minimum sum: 1 se k tak ka sum -> k * (k + 1) / 2
    long long min_sum = k * (k + 1) / 2;
 
    // Maximum sum: last ke k numbers ka sum -> k * (2 * n - k + 1) / 2
    long long max_sum = k * (2 * n - k + 1) / 2;
 
    // Direct condition check
    if (x >= min_sum && x <= max_sum) {
        cout << "YES
";
    } else {
        cout << "NO
";
    }
}
 
int main() {
    // Fast I/O TLE se bachne ke liye
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
 
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}