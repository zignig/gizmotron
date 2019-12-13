
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
//Vue.use(Vuex);

// create and event bus
EventBus = new Vue();

vm = new Vue({
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
    methods: {
        setIssue: function (obj) {
            this.issueItem = obj;
        },
        setCurrent : function (obj) {
            this.current = obj;
        },
        setTree: function (obj) {
            this.modeltree = obj;
        },
        setup : function () {
            // base load
            axios.get('/list')
                .then( response => (this.devices= response.data));

            EventBus.$on('pin',function(payload){
                EventToServer('pin',payload);
            });
            EventBus.$on('issue',function(payload){
                vm.setIssue(payload);
            });

            let es = new EventSource('/events');
            es.onerror = function(e){
                console.log(e);
            }

            es.addEventListener('menu', event => {
            }, false);

        }
    }
});

