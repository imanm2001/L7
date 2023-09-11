<template>
		<a  v-if="user" class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
		Welcome {{user.firstname}}&nbsp;{{user.lastname}}
		</a>
		<div v-if="user" class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#" @click="logoutJS()">Logout</a>
		 </div>
  		<a  v-if="!user" class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
        <img src="files/img/user.png?a">
        </a>
        <div v-if="!user" class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#" @click="login(true)">Login</a>
          <a class="dropdown-item" href="#" @click="login(false)">Sign Up</a>
        </div>
		
</template>

<script>
export default {
	created(){
		let loginMenue=this
		//Check if the user has already logined.
		//isLogined is a webmethod
		this.proxy.isLoginedAsync((res)=>{
			if(res.result){
				window.L7.logined(res.result);
			}
		});	
	},
	methods: {
		/**
			Load the login component
			@arg (Boolean) true: display the login form, false: display the sign up form
		*/
		login(arg){
			window.L7.loader.loadComponentTo('login',"loginDiv",$("#loginForm"),{login:arg});
		},
		/**
		logout the user
		*/
		logoutJS(){
		
			let menu=this;

			this.logoutAsync((res)=>{

				if(res.result){
					menu.$data.user=null;
					window.L7.logout();
				}
			});
		}
	},
	data(){
		return {singleInstance:true,user:null}
   }

};
</script>
<style>
</style>
