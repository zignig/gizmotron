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
  <a v-for="info in item.info" class="panel-block">
    <span class="panel-icon">
      <i class="fas fa-code-branch" aria-hidden="true"></i>
      {{info}}
    </span>
  </a>
</nav>
    `, 
}); 
