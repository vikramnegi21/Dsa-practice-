class Solution {
public:
    vector<string> findRelativeRanks(vector<int>& score) {
        priority_queue<pair<int,int>> q;

        for(int i = 0; i < score.size(); i++) {
            q.push({score[i], i});
        }

        vector<string> ans(score.size());
        int rank = 1;

        while(!q.empty()) {
            int index = q.top().second;
            q.pop();

            if(rank == 1)
                ans[index] = "Gold Medal";
            else if(rank == 2)
                ans[index] = "Silver Medal";
            else if(rank == 3)
                ans[index] = "Bronze Medal";
            else
                ans[index] = to_string(rank);

            rank++;
        }

        return ans;
    }
};