<template>
        <div id="ribbonContainer" class="row w-100 m-2 ribbon">
			
        </div>
        <div  class="row w-100 m-2">
			<div class="col">
				<div id="appletContainer"></div>
			</div>
        </div>
</template>

<script>
/**
List all avaiable applets. Load and unload them on-demand
*/
export default {
	/** 
	 * Get a list of all avaiable applets by calling listAppletsAsync webmthod. Creates a ribbon with buttons that loads the applete. The webmethod
	 * will return name,title, and the corresponding img of each applet using the following structure
	 * appName {String}  name of the applet
	 * appTitle {String} title of the applet
	 * appImg {String} path to image relative to files/img/
	 * 
	*/
	
	created(){
		let appletManager=this;
		this.methods.listAppletsAsync((res)=>{
			this.proxy.$data.applets=res.result;
			let ribbonButtons=[]
			for(let id in res.result){
				let applet=res.result[id];
				ribbonButtons.push({id:applet.appName,text:applet.appTitle,img:applet.appImg,click:()=>{appletManager.proxy.loadComponent(applet.appName);}});
			}
			window.L7.loader.loadComponentTo('ribbon', "ribbonDiv", $("#ribbonContainer"),{buttons:ribbonButtons});
		});
	},
	methods:{
		/**
		 * unmount the previously loader component and load the new component 
		 * @param {String} comp name of the component
		 */
		loadComponent(comp){
			if(!this.$data.loadedApp||comp!=this.$data.loadedApp.name){
				let appletManager=this;
				if(this.$data.loadedApp){
					window.L7.unmount(this.$data.loadedApp);
				}
				window.L7.loader.loadComponentTo(comp, comp+"Div", $("#appletContainer"),{},(comp)=>{appletManager.$data.loadedApp=comp});
			}
		}
	},
	/**
	 * @returns appletes {Array} an array of all avaiable arrays
	 * 			loadedApp {Object} a refrence to the loaded applet
	 */
	data(){
		return {applets:[],loadedApp:null};
	}
};
</script>
<style>
</style>