Vue.component('async-test',
{ 
    data() {
        return {
            isActive: true 
        }
    },
    resolve(){
        console.log("loadme");
    },
}); 
