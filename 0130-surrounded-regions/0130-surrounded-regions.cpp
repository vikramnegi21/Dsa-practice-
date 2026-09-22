class Solution {
public:

    int dro[4] = {-1, 1, 0, 0};
    int dco[4] = {0, 0, -1, 1};

    int n, m;

    void dfs(int i, int j, vector<vector<int>>& vis,
             vector<vector<char>>& board) {

        vis[i][j] = 1;

        for(int k = 0; k < 4; k++) {

            int r = i + dro[k];
            int c = j + dco[k];

            if(r >= 0 && r < n &&
               c >= 0 && c < m &&
               !vis[r][c] &&
               board[r][c] == 'O') {

                dfs(r, c, vis, board);
            }
        }
    }

    void solve(vector<vector<char>>& board) {

        n = board.size();
        m = board[0].size();

        vector<vector<int>> vis(n, vector<int>(m, 0));

        
        for(int j = 0; j < m; j++) {

            if(board[0][j] == 'O')
                dfs(0, j, vis, board);

            if(board[n-1][j] == 'O')
                dfs(n-1, j, vis, board);
        }

    
        for(int i = 0; i < n; i++) {

            if(board[i][0] == 'O')
                dfs(i, 0, vis, board);

            if(board[i][m-1] == 'O')
                dfs(i, m-1, vis, board);
        }

        
        for(int i = 0; i < n; i++) {
            for(int j = 0; j < m; j++) {

                if(board[i][j] == 'O' && !vis[i][j]) {
                    board[i][j] = 'X';
                }
            }
        }
    }
};