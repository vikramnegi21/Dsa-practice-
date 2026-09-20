#include<iostream>
#include<algorithm>
using namespace std;
void solve(){
    long long n;
    long long count=0;
    cin>>n;
    for(long long  i=1;;i++){
        if(n%i==0){
            count++;
          
        }
        else{
            break;
        }
    }
      cout<<count<<"
";
        
}
int main(){
    int t;
    cin>>t;
    while(t--){
        solve();
    }
    return 0;
}