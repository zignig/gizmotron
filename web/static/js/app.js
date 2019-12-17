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
        boards : [],
        current_board : Object,
    },
    getters: {
      list : state => {
            return state.boards
        },
      current_board: state => {
            return state.current_board
        }
    },
    mutations: {
       full_list: (state,boards) =>{
            state.boards = boards;
            state.current_board = boards[0];
        },
       set_current: (state,item) =>{
            state.current_board = item;
        } 
    },
    actions: {
    }
});

vm = new Vue({
    store,
    el: '#app',
    data() { 
        return {
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
            axios.get('/list.json')
                .then(function(response){ 
                    console.log(response.data);
                    //vm.devices = response.data;
                    store.commit('full_list',response.data);
                }
            );

            //let es = new EventSource('/events');
            //es.onerror = function(e){
            //    console.log(e);
            //}

            //es.addEventListener('menu', event => {
            //}, false);

        }
    }
});

