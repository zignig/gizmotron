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
  <a class="panel-block"> <img :src="image"></img>  </a>
  <a v-for="(name,value) in item.info" class="panel-block" v-bind:key="value">
      <span class="tag is-info is-rounded"> {{name}} </span>&nbsp; {{value}}
  </a>
</nav>
    `, 
}); 
