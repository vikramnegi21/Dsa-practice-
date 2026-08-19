class Solution {
public:
    int maxNumberOfFamilies(int n, vector<vector<int>>& reservedSeats) {

        unordered_map<int, unordered_set<int>> mp;

        // Reserved seats store karna
        for (auto &s : reservedSeats) {
            int row = s[0];
            int seat = s[1];

            mp[row].insert(seat);
        }

        // Jis row mein koi reservation nahi hai,
        // usme 2 families aa sakti hain
        int result = (n - mp.size()) * 2;

        // Sirf reserved wali rows check karenge
        for (auto &[row, bookedseats] : mp) {

            bool groupA = bookedseats.count(2) == 0 &&
                          bookedseats.count(3) == 0 &&
                          bookedseats.count(4) == 0 &&
                          bookedseats.count(5) == 0;

            bool groupB = bookedseats.count(4) == 0 &&
                          bookedseats.count(5) == 0 &&
                          bookedseats.count(6) == 0 &&
                          bookedseats.count(7) == 0;

            bool groupC = bookedseats.count(6) == 0 &&
                          bookedseats.count(7) == 0 &&
                          bookedseats.count(8) == 0 &&
                          bookedseats.count(9) == 0;

            if (groupA && groupC) {
                result += 2;
            }
            else if (groupA || groupB || groupC) {
                result += 1;
            }
            else {
                result += 0;
            }
        }

        return result;
    }
};