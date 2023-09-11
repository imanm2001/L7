<template>
    <div v-if="login" class="container-fluid h-100 w-100">
		<form @submit.prevent="loginJS" >
			<div class="row w-100">
				<div class="col-md w-20">
				</div>
				<div class="col-md">
					<div class="row" id="alert"></div>
					<div class="row text-nowrap m-1">
						<div class="col-sm-1 d-flex justify-content-md-end m-0"><p class="justify-content-md-end" >User Name : </p></div>
						<div class="col-lg-10 d-flex justify-content-md-start"><input type="text" class="form-control"  placeholder="User Name" v-model="username"></div>
					</div>
					<div class="row text-nowrap m-1">
						<div class="col-sm-1 d-flex justify-content-md-end m-0"><p style="align:right">Password : </p></div>
						<div class="col-lg-10 d-flex justify-content-md-start"><input type="password" class="form-control input-lg"  v-model="password" placeholder="Password"></div>
					</div>
					<div class="row text-nowrap m-1">
						<div class="col-sm d-flex justify-content-md-center m-0"><input class="btn btn-primary" type="submit" value="Submit">&nbsp;or&nbsp;<a href="#" @click="login=false">Create a new account</a></div>
					</div>
				</div>
					
				<div class="col-md w-20">
				</div>
			</div>
		</form>
	</div>
	<div v-else class="container-fluid h-100 w-100">
		<form @submit.prevent="createAccountJS" oninput='pass2.setCustomValidity(pass1.value != pass2.value ? "Passwords do not match." : "")'>
			<div class="row w-100">
				<div class="col-md w-20" >
				</div>
				<div class="col-md">
					<div class="row" id="alert"></div>
					<div class="row text-nowrap m-1">
						<div class="col-sm-1 d-flex justify-content-md-end m-0"><p class="justify-content-md-end ">First Name : </p></div>
						<div class="col-lg-10 d-flex justify-content-md-start"><input type="text" class="form-control"  placeholder="First Name" v-model="firstname" required></div>
					</div>
					<div class="row text-nowrap m-1">
						<div class="col-sm-1 d-flex justify-content-md-end m-0"><p class="justify-content-md-end ">Last Name : </p></div>
						<div class="col-lg-10 d-flex justify-content-md-start"><input type="text" class="form-control" placeholder="Last Name" v-model="lastname" required></div>
					</div>
					<div class="row text-nowrap m-1">
						<div class="col-sm-1 d-flex justify-content-md-end m-0"><p class="justify-content-md-end ">User Name : </p></div>
						<div class="col-lg-10 d-flex justify-content-md-start"><input type="text" class="form-control"  placeholder="User Name" v-model="username" required></div>
					</div>
					<div class="row text-nowrap m-1">
						<div class="col-sm-1 d-flex justify-content-md-end m-0"><p style="align:right">Password : </p></div>
						<div class="col-lg-10 d-flex justify-content-md-start"><input type="password" class="form-control input-lg"  placeholder="Password" v-model="password" name="pass1" required></div>
					</div>
					<div class="row text-nowrap m-1">
						<div class="col-sm-1 d-flex justify-content-md-end m-0"><p style="align:right">Re-enter Password : </p></div>
						<div class="col-lg-10 d-flex justify-content-md-start"><input type="password" class="form-control input-lg"  placeholder="Re-enter Password" name="pass2" required></div>
					</div>
					
					<div class="row text-nowrap m-1">
						<div class="col-sm d-flex justify-content-md-center m-0"><input class="btn btn-primary" type="submit" value="Submit" ></div>
					</div>
				</div>
				<div class="col-md w-20">
				</div>
			</div>
		</form>
	</div>

</template>

<script>
export default {
methods:{
/**
read the form, encrtpy the passord, and submit it to Django using createAccountAsync webmethod
*/
	createAccountJS(){
		let pass=window.L7.md5(this.password);
		this.createAccountAsync(this.firstname,this.lastname,this.username,pass,(res)=>{

			if(res.result){
				this.login=true;
				this.username="";
				this.password="";
				this.firstname="";
				this.lastname="";
				this.$nextTick().then((v)=>{
					$("#alert").addClass("alert alert-info").html("User was created")});
			}else{
				$("#alert").addClass("alert alert-danger").html("User exists");
				
			}
		});

	},
	/**
	Login after encrtping the password using loginUserAsync webmethod
	*/
	loginJS(){
		let pass=window.L7.md5(this.password);
		
		
		this.loginUserAsync(this.username,pass,(res)=>{
			if(res.result){
			$("#alert").removeClass("alert alert-danger").html("");
				
				window.L7.logined(res.result);
			}else{
				$("#alert").addClass("alert alert-danger").html("Invalid Username or Password");
			}
		});
	}
},
	data(){
		return {
			singleInstance:true,
			login:true,
			username:'',
			password:'',
			firstname:'',
			lastname:''
		
		}
   }

 };
</script>
<style>
</style>