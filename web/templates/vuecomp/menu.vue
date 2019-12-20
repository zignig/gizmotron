Vue.component('menu-main',
{ 
    data() {
        return {
        }
    },
    props: {
	itemList: Array,
        name: "",
    },
    methods: {
        select(item){
            store.commit('set_current',item);
        },
    },
    template: `  
    <b-menu>
        </b-menu-list>
        <b-menu-list label="Boards">
            <b-menu-item @click="select(item)" v-for="item  in itemList" :label="item.name" v-bind:key="item.name">
            </b-menu-item>
        </b-menu-list>
    </b-menu>
    `,
}); 
