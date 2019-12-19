Vue.component('board-def',
{ 
    data() {
        return {
            isActive: true 
        }
    },
    props: {
        item: Function,
    },
    computed: {
    },
    template: `  
<nav class="panel">
  <p class="panel-heading">
    <b>{{item.name}}</b>
  </p>
  <a v-for="(name,value) in item.info" class="panel-block">
      <span class="tag is-info is-rounded"> {{name}} </span>&nbsp; {{value}}
  </a>
</nav>
    `, 
}); 
