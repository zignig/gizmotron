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
        login(){
            Eventbus.emit('click','hello');
        },
    },
    template: `  
    <b-menu>
        </b-menu-list>
        <b-menu-list label="Boards">
            <b-menu-item v-for="i in itemList" :label="i">
            </b-menu-item>
        </b-menu-list>
    </b-menu>
    `,
}); 
