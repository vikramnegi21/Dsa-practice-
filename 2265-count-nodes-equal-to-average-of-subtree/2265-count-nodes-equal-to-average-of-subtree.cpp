/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
int summ(TreeNode*root,int &count){
    if(root==NULL) return 0;
    count++;
   return  root->val +summ(root->left,count)+summ(root->right,count);
    
    

    }

int solve(TreeNode*root){
    if(root==NULL) return 0;
    int ans=0;
    int count =0;
    int sum=0;
    sum=summ(root,count);
    if(root->val==sum/count){
        ans+=1;
    }
   ans+=solve(root->left);
   ans+= solve(root->right);
   return ans;

}
    int averageOfSubtree(TreeNode* root) {
        return solve(root);
    
        
    }
};