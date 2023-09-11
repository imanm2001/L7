<template>
        <div id="appletsContainer">
        </div>
</template>

<script>
export default { 
//Get list of all of available applets
	created(){
		
		window.L7.vm.$nextTick().then((v)=>{
			window.L7.loader.loadComponentTo('applets', "appletsDiv", $("#appletsContainer"));
		});},
	data(){
		return {};
	   }
	};
</script>
<style>
</style>
