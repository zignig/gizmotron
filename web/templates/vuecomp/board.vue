Vue.component('board-def',
{ 
    data() {
        return {
            isActive: true 
        }
    },
    props: {
        item: {},
    },
    computed: {
        image: function(){
            return "/static/img/"+this.item.name+".jpg"
        },
    },
    template: `  
<nav class="panel">
  <p class="panel-heading">
    <b>{{item.name}}</b>
  </p>
  <div class="box">
  <div class="field is-grouped is-grouped-multiline">
	<div v-for="(name,value) in item.info " class="control" v-bind:key="value">
		<div class="tags has-addons">
		  <a class="tag ">{{value}}</a>
		  <a class="tag is-primary">{{name}}</a>
		</div>
	</div>
  </div>
  </div>
  <a class="panel-block"> <img :src="image"></img>  </a>
</nav>
    `, 
}); 
