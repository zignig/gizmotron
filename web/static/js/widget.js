// navfoot
var widget = Vue.component('navblob',
{ template : '#navblob',
 name: 'navblob',
    data() {
        return {
            isActive: false
        }
    },
    props: {
        issueItem: {
            type: String,
        },
    },
}); 
