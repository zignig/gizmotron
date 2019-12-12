Vue.component('section-table',
{ 
    data() {
        return {
            data : ['one','two'],
            columns : [],
        }
    },
    props: {
        issueItem: {
            type: String,
        },
    },
    template: '<b-table :data="data" :columns="columns"></b-table>',
}); 
