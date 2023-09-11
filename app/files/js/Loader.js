export class Loader {
	
    components = {};//Keep a reference to all of the loaded components
	
	/**
		merge the default data of the component, and the passed parameters to load the component
		@comp (Vue component) the component to be loaded
		@params (Dictionary) the values to be override and merge
	*/
    mergeData(comp, params) {
        if (params&&Object.keys(params).length>0) {
			if(!comp.params){
				comp.params={}
			}
			comp.params=Object.assign(comp.params,params);
        }
    }
	/**
	 load the component on-demand
	 @name (String) name of the component
	 @id (String) id if not empty, a div element will be created and the component will append to it. The created div will be added to the parentTag
	 @parentTag (jQuery selector)
	 @params (Dictionary) the parameters will be merge with existing parameters returned by data() function of the component
	 @callBack (function(component)) callBack will be called after creating the component. component is created component 
						@component.htmlTag (jQuery) a reference to the element that contains the component
						@component.name (String) name of the component
						@component.node (Object) a reference to the application created by Vue
						@component.proxy (Proxy) a reference to the Proxy object created by Vue
						@component.tagId (String)  id of the element that the component is added to
						
						
						
	*/
    loadComponentTo(name, id, parentTag, params = {},callBack=null) {
        var comp = null;
		//If the component is already loaded and it is a single instance component, assign the new parameters to it, otherwise load the component 
        if (!(name in window.L7.loader.components)||L7.loader.components[name].length==0) {
            window.L7.loader.components[name] = [];
        } else {
			let temp=window.L7.loader.components[name][0];
			
			
            if (temp.proxy.$data.hasOwnProperty('singleInstance')  && temp.proxy.singleInstance) {
				
                comp = temp;
				for(let key in params){
					temp.proxy.$data[key]= params[key];
				}
	
            }
        }
		//Create the component if it has not been created before
        if (comp == null) {
            var remove = id == "";
            if (remove) {
                id = name + window.L7.loader.components[name]
            }
            parentTag.append($("<div id='" + id + "'>loading...</div>"))

            import('/component/' + name + '?' + $.now()).then((mod) => {

                comp = mod.default;
				
				comp.tagId=id;
				window.L7.loader.components[name].push(comp);
				
				if(comp.data){
					comp.params=comp.data();
				}else{
					comp.params={};
				}
				
				comp.data=function(){return comp.params};
				comp.name=name;
                window.L7.loader.mergeData(comp, params);
			
				if(comp.hasOwnProperty('created')){
			
					comp.oldCreated=comp.created;
					comp.created=function(){comp.proxy=this; 	this.$nextTick().then((v)=>{comp.oldCreated();})};
				}else{
					comp.created=function(){comp.proxy=this;};
				}
				
	
				
                var vnode = Vue.createApp();
                var placeHolder = $("#" + id);
                if (remove) {

                    var tagParent = placeHolder.parent();
                    placeHolder.remove();
                    placeHolder = tagParent;

                }
				//Add the component tag 
                placeHolder.html("<" + name + ">");
				
                vnode.component(name.toLowerCase(), comp);
                vnode.mount(placeHolder[0]);
				comp.node=vnode
				comp.htmlTag=placeHolder;
				if(callBack){
					callBack(comp);
				}

            });
        }else if(callBack){
			callBack(comp);
		}

    }

}

