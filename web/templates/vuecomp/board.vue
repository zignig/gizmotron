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
    template: `  
<nav class="panel">
  <p class="panel-heading">
    <b>{{item.name}}</b>
  </p>
  <div class="panel-block">
    <p class="control has-icons-left">
      <input class="input" type="text" placeholder="Search">
      <span class="icon is-left">
        <i class="fas fa-search" aria-hidden="true"></i>
      </span>
    </p>
  </div>
  <p class="panel-tabs">
    <a class="is-active">All</a>
    <a>Public</a>
    <a>Private</a>
    <a>Sources</a>
    <a>Forks</a>
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
