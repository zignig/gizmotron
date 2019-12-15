function EventToServer(section,name){
    axios.post('/postevent',{
        section: section,
        name: name,
    });
}

// shh
Vue.config.productionTip = false;
// add semantic ui
Vue.use(Buefy.default);
Vue.use(Vuex);

store = new Vuex.Store({
    state  : {
        code : []
    },
    getters: {
    },
    mutations: {
    },
    actions: {
    }
});

vm = new Vue({
    store,
    el: '#app',
    data()  {
        return {
		count: 0,
		devices: [],
	}
    },
    created() {
        this.setup();
    },
    mounted() {
    },

    methods: {
        setup : function () {
            // base load
            axios.get('/list')
                .then( response => (this.devices= response.data));

            //let es = new EventSource('/events');
            //es.onerror = function(e){
            //    console.log(e);
            //}

            //es.addEventListener('menu', event => {
            //}, false);

        }
    }
});

