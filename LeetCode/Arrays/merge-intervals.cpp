/*
🔹 Approach (Merge Intervals - Striver Style)

1. Sort all intervals based on their starting time.
2. Traverse each interval one by one.
3. If the current interval is already covered by the last merged interval,
   skip it to avoid redundant work.
4. Otherwise, try to merge it with upcoming intervals:
   - If next interval starts before current end → merge
   - Update the end accordingly
5. Push the final merged interval into the result.

🔹 Key Idea:
Sorting ensures overlapping intervals come together, allowing merging efficiently.

🔹 Time Complexity: O(n log n)
🔹 Space Complexity: O(n)
*/

class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        int n = intervals.size();

        sort(intervals.begin(), intervals.end());
        vector<vector<int>> ans;

        for(int i = 0; i < n; i++){
            int start = intervals[i][0];
            int end = intervals[i][1];

            if(!ans.empty() && end <= ans.back()[1]){
                continue;
            }

            for(int j = i + 1; j < n; j++){
                if(intervals[j][0] <= end){
                    end = max(end, intervals[j][1]);
                } else {
                    break;
                }
            }

            ans.push_back({start, end});
        }

        return ans;
    }
};
