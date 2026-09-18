#include <iostream>
#include <string>
#include <vector>
#include <map>
 
using namespace std;
 
void solve() {
    string s, t;
    cin >> s >> t;
 
    map<char, int> freq;
    for (char c : t) {
        freq[c]++;
    }
 
    int j = t.length() - 1; // t ka pointer end par
 
    for (int i = s.length() - 1; i >= 0; i--) {
        if (j >= 0 && s[i] == t[j]) {
            freq[s[i]]--;
            j--;
        } else if (freq[s[i]] > 0) {
            // Extra character mila jo t mein late aana tha
            cout << "NO
";
            return;
        }
    }
 
    if (j < 0) {
        cout << "YES
";
    } else {
        cout << "NO
";
    }
}
 
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    while (n--) {
        solve();
    }
    return 0;
}