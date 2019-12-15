var navbar = Vue.component('nav-bar',
{
    data() {
            return { isActive: true }
            },
    props : {},
    methods: {
        login(){
            EventBus.$emit('click','hello');
            console.log('fnord');
        },
    },
    template : `
        <b-navbar type="is-black">
            <template slot="brand">
                <b-navbar-item href="#">
                    <b>Boneless</b>
                </b-navbar-item>
            </template>
            <template slot="start">
                <b-navbar-item href="#">
                    Home
                </b-navbar-item>
                <b-navbar-item href="#">
                    Documentation
                </b-navbar-item>
                <b-navbar-dropdown label="Info">
                    <b-navbar-item href="#">
                        About
                    </b-navbar-item>
                    <b-navbar-item href="#">
                        Contact
                    </b-navbar-item>
                </b-navbar-dropdown>
            </template>

            <template slot="end">
                <b-navbar-item tag="div">
                    <div class="buttons">
                        <a class="button is-primary">
                            <strong>Build</strong>
                        </a>
                        <a @click="login" class="button is-light">
                            Debug 
                        </a>
                    </div>
                </b-navbar-item>
            </template>
        </b-navbar>
    `
});

