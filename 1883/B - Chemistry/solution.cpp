#include <iostream>
#include <vector>
#include<string>
using namespace std;
 
bool canMakePalindrome(string s, int k) {
    vector<int> freq(26, 0);
 
    for (char ch : s) {
        freq[ch - 'a']++;
    }
 
    int odd = 0;
 
    for (int x : freq) {
        if (x % 2 != 0) {
            odd++;
        }
    }
 
    if (odd > k + 1) {
        return false;
    }
 
    return true;
}
 
int main() {
    int t;
    cin >> t;
 
    while (t--) {
        int n, k;
        cin >> n >> k;
 
        string s;
        cin >> s;
 
        if (canMakePalindrome(s, k)) {
            cout << "YES" << endl;
        } 
        else {
            cout << "NO" << endl;
        }
    }
 
    return 0;
}