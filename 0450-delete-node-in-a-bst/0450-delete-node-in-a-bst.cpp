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
TreeNode* helper(TreeNode* root){
    if(root->left==NULL){
        return root->right;
    }
    if(root->right==NULL){
        return root->left;
    }
            TreeNode* rightChild = root->right;
        TreeNode* successor = root->right;
while(successor->left!=NULL){
    successor=successor->left;
}
successor->left=root->left;
return rightChild;

}

    TreeNode* deleteNode(TreeNode* root, int key) {
        if(root==NULL){
            return NULL;
        }
        if(root->val==key){
            return helper(root);
        }
        TreeNode*curr=root;
        while(curr!=NULL){
            if(curr->val<key){
                if(curr->right!=NULL&&curr->right->val==key){
                    curr->right=helper(curr->right);
                }
                else{
                    
                    curr=curr->right;
                }
                
            }
            else{
                if(curr->left != NULL && curr->left->val == key) {
                if(curr->left!=NULL){
                    curr->left=helper(curr->left);
                }
                }
                else{
                                        curr=curr->left;

                }
            }
        }
        return root;
        
    }
};