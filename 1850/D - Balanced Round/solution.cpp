#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
void solve(){
    long  long n,k;
    cin>>n>>k;
    vector<long long> a(n);
    for(int i=0;i<n;i++){
cin>>a[i];
 
    }
    //sort  kiya kuiki closet chiye 
    sort(a.begin(),a.end());
    int curr=1;
    int maxi=1;
    for(int i=1;i<n;i++){
        //check kiya ki difference k se kam hai ya nahi
        if(abs(a[i]-a[i-1])<=k){
            curr++;
        }
        else{
            //agar difference k se zyada hai to curr ko 1 kar do
            curr=1;
        }
        //maximum length chiye toh is liye y kiya 
        maxi=max(maxi,curr);
    }
    // yha n-maxi kiya kuiki maximum length ko minus kar do taki jo bache wo answer ho
    cout<<n-maxi<<"
";
}
 
int main (){
int t;
cin>>t;
while(t--){
    solve();
}
    return  0;
}