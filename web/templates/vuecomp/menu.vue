Vue.component('menu-main',
{ 
    data() {
        return {
            isActive: true ,
	    itemList: Array,
        }
    },
    props: {
    },
    template: `  
<b-menu>
        <b-menu-list label="Menu">
        </b-menu-list>
        <b-menu-list label="Actions">
            <b-menu-item v-for="i in itemList" :label="i"></b-menu-item>
        </b-menu-list>
    </b-menu>
    `,
}); 
