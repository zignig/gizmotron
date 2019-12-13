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
	<div class="level">
	<b-steps size="is-small">
            <b-step-item label="Parse" ></b-step-item>
            <b-step-item label="Build"  ></b-step-item>
            <b-step-item label="Optimize"  ></b-step-item>
        </b-steps>
	</div>
	</section>
    `, 
}); 
