<template>
        <div  class="row w-100 ribbon" style="background-color: lightblue;">
			<div class="col  justify-content-md-start d-flex p-2">
				<div class="row w-100">
					<div v-for="button in buttons" type="button" class="col-2 justify-content-md-start d-flex ">
						<button  class="btn btn-labeled btn-success" @click="button.click()">
						<span class="btn-label m-1"><img :src="'files/img/'+button.img" class=""></span>{{ button.text }}</button>
					</div>
				 </div>
			 </div>
        </div>
</template>

<script>
/**
 * Create a button for each element of buttons
 * 
 */
export default { 
	
	/**
	 * @returns:
	 * 	buttons (array) each element has the following structure 
	 *  { text (string) 
	 * 	 img (string) the path relative to files/img folder
	 *   click (function) clicking on the button will trigger this function
	 * 	}
	 */
	data(){
		return {buttons:[]}
	   }
	};
</script>
<style>
</style>