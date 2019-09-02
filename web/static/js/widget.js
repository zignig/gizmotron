// navfoot
var widget = Vue.component('widget',
{ template : '#widget',
 name: 'widget',
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
    methods:{
    
}}); 
