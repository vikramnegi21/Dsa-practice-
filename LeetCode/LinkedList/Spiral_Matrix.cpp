/**
 * 🚀 Spiral Matrix
 *
 * 💡 Approach:
 * - Matrix ko spiral order me traverse karne ke liye hum 4 boundaries use karte hain:
 *   1. top    -> starting row
 *   2. bottom -> ending row
 *   3. left   -> starting column
 *   4. right  -> ending column
 *
 * 🧠 Idea:
 * - Jab tak boundaries valid hain (top <= bottom && left <= right):
 *   1. Left → Right (top row)
 *   2. Top → Bottom (right column)
 *   3. Right → Left (bottom row)   [agar top <= bottom]
 *   4. Bottom → Top (left column)  [agar left <= right]
 *
 * - Har step ke baad boundary shrink karte hain
 *
 * 🔄 Steps:
 * 1. top = 0, bottom = n-1, left = 0, right = m-1
 * 2. Traverse in 4 directions
 * 3. Har traversal ke baad boundary update
 *
 * ⚡ Time Complexity: O(N * M)
 * ⚡ Space Complexity: O(1) (excluding output array)
 */

class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {

        vector<int> ans;

        int n = matrix.size();        // rows
        int m = matrix[0].size();     // columns

        // Step 1: initialize boundaries
        int top = 0, bottom = n - 1;
        int left = 0, right = m - 1;

        // Step 2: traverse in spiral order
        while(top <= bottom && left <= right) {

            // Left → Right (top row)
            for(int i = left; i <= right; i++) {
                ans.push_back(matrix[top][i]);
            }
            top++;

            // Top → Bottom (right column)
            for(int i = top; i <= bottom; i++) {
                ans.push_back(matrix[i][right]);
            }
            right--;

            // Right → Left (bottom row)
            if(top <= bottom) {
                for(int i = right; i >= left; i--) {
                    ans.push_back(matrix[bottom][i]);
                }
                bottom--;
            }

            // Bottom → Top (left column)
            if(left <= right) {
                for(int i = bottom; i >= top; i--) {
                    ans.push_back(matrix[i][left]);
                }
                left++;
            }
        }

        return ans;
    }
};
