Vue.component('prog-bar',
{ 
    data() {
        return {
            isActive: true 
        }
    },
    props: {
        issueItem: {
            type: String,
	    value: 0,
        },
    },
    template: `  
    <section>
        <b-progress :value="80" show-value format="percent"></b-progress>
    </section>
    `,
}); 
