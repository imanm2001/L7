'use strict';
import {Loader} from '/files/js/Loader.js';
// This will fix the conflict between bootstrap buttons and jQuery-ui
$(document).ready(function () {
    var bootstrapButton = $.fn.button.noConflict()
        $.fn.bootstrapBtn = bootstrapButton;
});

//Attach global functions to the window to make it accessable to all components
window.L7 = {
	/**
		@str {String} the input string to be encoded using md5 algorithm
	*/
	md5(str){
		return CryptoJS.MD5(str).toString(CryptoJS.enc.Base64);
	},
	/*
    getCookie2(name) {
        var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        if (match)
            return match[2];
    },*/
	/**
		load, mount and unmount the components on-demand
	*/
    loader: new Loader(),
	/**
		return the CSRF used by Django
	*/
	getCSRF(){
		return $("[name='csrfmiddlewaretoken']")[0].value
	},
	/**
		callWebMethod uses a variable length arguments to pass the parameters to the corresponding method on server using ajax.
		the result will be returned either through return (sync) or the callBack (async) which has the following format 
			@success (bool) determines if the there was any error
			@msg (String) @msg can be used to determined the error that cause the failur
			@result (Object) a JSON objected created by python
	*/
    callWebMethod() {

        let arglen = arguments.length // Number of arguments
        let asyncCall = arguments[arglen - 1]; // Is it sync or async
        let totalParams = arglen - 2; //the first two arguments are the component's name and the method's name
        let callBack = asyncCall ? arguments[--totalParams] : undefined; //In case of async call, use the callback to return the result
		
		
        let params = Array();
        for (var i = 2; i < totalParams; i++) {
            params[i - 2] = arguments[i];
        }
		
        let data = null; //returned data
        var url = '/webmethod/' + arguments[0] + '/' + arguments[1]
		
		let paramsSerilized = Object.assign({}, {
		    csrfmiddlewaretoken: window.L7.getCSRF()
		}, {
		    params: JSON.stringify(params)
		});

        $.ajax({
            url: url,
            type: 'POST',
            async: asyncCall,
            cache: false,
            timeout: 10000,
            data: paramsSerilized

        }).done(function (msg) {
            
            let obj = JSON.parse(msg);
			if (obj.success) {
				//if it is an async call, call the callback otherwise return the data
				if (asyncCall) {
					callBack(obj);
				} else {
                
                    data = obj;

                }
			}else {
				window.L7.showDialog(obj.msg);
			}
            
        });

        return data;

    },
	/**
		Created a new dialog and loads the component into it
		@compName: name of the component
		@compParams: the initial values for the component's data
		@callBack: @callBack will be called aftr loading the component
		@dialogParams: the parameters of the dialog
		@button: buttons of the dialog
		@return: the created dialog
	*/
	loadComponentToDialog(compName,compParams,callBack,dialogParams,button){
		let dialog=window.L7.showDialog($("<div id='compDialogContainer'>"),dialogParams,button);
		
		let component=null;
		window.L7.loader.loadComponentTo(compName, "comDialogDiv", $("#compDialogContainer"),compParams,(comp)=>{component=comp;callBack(comp);});
		dialog.on('dialogclose', function(event) {
				window.L7.unmount(component);
		});
		return dialog;
	},
	/**
		Displays a dialog
		@content: content of the dialog
		@params: dialog's paramters
		@button: dialog's buttons
		@return: created dialog
		
	*/
    showDialog(content,params,buttons) {
        let dialog=$("<div id='dialog"+$.now()+"'>");
		
		dialog.append(content);
		if(!buttons){
			buttons={'Ok': function () {
					$(this).dialog("close");
					return true;
				}
			};
		}
		let dparams={
            resizable: true,

            modal: true,
            position: {
                my: "center ",
                at: "center ",
                of: window
            },
            closeText: "Close",
            buttons: buttons
        };
		if(params){
			dparams=Object.assign(dparams,params);
		}
		dialog.on('dialogclose', function(event) {
			dialog.remove();
		});
		dialog.dialog(dparams);
        return dialog;
		
    },
	/**
		Login the user, store the information, and load the app.vue component
		@user (Object) 
		@user.firstname (String) user's firstname
		@user.lastname (String) user's lastname
	*/
	logined(user){
		if(user){
			window.L7.loader.components['loginMenu'][0].proxy.$data.user=user;
			window.L7.vm.$data.user=user;
		}
		if(window.L7.loader.components.hasOwnProperty('login')&&window.L7.loader.components['login'].length>0){
			window.L7.unmount(window.L7.loader.components['login'][0]);
		}
		
		window.L7.vm.$nextTick().then((v)=>{
			window.L7.loader.loadComponentTo('app', "appDiv", $("#appContainer"));
		});

		
		
	},
	/**
	Logout the user
	*/
	logout(){
		
		window.L7.loader.components['loginMenu'][0].proxy.$data.user=null;
		window.L7.vm.$data.user=false;
		
		window.L7.unmount(window.L7.loader.components['app'][0]);


		
		
	},
	/**
	Unmount the component
	@component: the component to unmount
	*/
	unmount(component){
		var components=window.L7.loader.components[component.name];
		const index = components.indexOf(component);
		
		if (index > -1) { 
			components.splice(index, 1); 
		}
		
		component.node.unmount();
		if(component.tagId&&component.tagId!=""){
			$("#"+component.tagId).remove();
		}
		
	}
};

//Load the loginMenue component and add it to dropdown
window.L7.loader.loadComponentTo('loginMenu', "", $("#loginDropDown"));
//Create a cue app
let vm = Vue.createApp({

    data() {
        return {
            user: null
           
        }
    }
    
})
window.L7.vm=vm.mount('#vue-app');

