<template>
  	
        <div>
			aaa{{acount}}
			<a class="nav-link" href="#" @click="console.log(this);acount++">add </a>
        </div>
</template>

<script>
export default { 
	setup(){console.log(this);},
	data(){
		return {acount:1}
	   }
	};
</script>
<style>
</style>
