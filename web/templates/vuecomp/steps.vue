Vue.component('compile-steps',
{ 
    data() {
        return {
            isActive: true 
        }
    },
    props: {
        issueItem: {
            type: String,
        },
    },
    template: `  
    <section>
        <b-steps size="is-large">
            <b-step-item label="Account" icon="account"></b-step-item>
            <b-step-item label="Profile" icon="account"></b-step-item>
            <b-step-item label="Social" icon="account"></b-step-item>
        </b-steps>
    </section>`,
}); 
