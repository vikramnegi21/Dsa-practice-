#include<iostream>
#include<algorithm>
using namespace std;
bool solve(){
    long long  n;
    cin>>n;
    if((n & (n - 1)) == 0){
        cout<<"NO"<<endl;
    }
    else{
        cout<<"YES"<<endl;
    }
}
int main (){
    int t;
    cin>>t;;
    while(t--){
        solve();
    }
    return 0;
}