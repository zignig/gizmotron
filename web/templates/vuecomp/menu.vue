Vue.component('menu-main',
{ 
    data() {
        return {
        }
    },
    props: {
	itemList: Array,
    },
    methods: {
        login(iname){
            console.log(name);
        },
    },
    template: `  
    <b-menu>
        </b-menu-list>
        <b-menu-list label="Boards">
            <b-menu-item @click="login" v-for="i in itemList" :label="i">
            </b-menu-item>
        </b-menu-list>
    </b-menu>
    `,
}); 
