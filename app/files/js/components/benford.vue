<template>
	<div class="w-100" >
        <div class="row w-100">
			<div class="col-sm-auto d-flex justify-content-md-start">
				<button  class="btn btn-labeled btn-primary" @click="selectFile()">Select a file</button>
			</div>
			<div class="col w-100" v-if="prevRows.length">
				<div class="row">
					<div class="col-sm-auto d-flex justify-content-md-start">
						Delimiter :
					</div>
					<div class="col-sm-auto d-flex justify-content-md-start">
						<select class="custom-select" id="delimiter" v-model="conf.delimiterIndex">
							<option v-for="(key,index) in Object.keys(delimiters)" :key="index" :value="index">{{delimiters[key]}}</option>
						</select>
					</div>
					<div v-if="conf.delimiterIndex==(delimitersKeys.length-1)" class="col-sm-auto d-flex justify-content-md-start">
						<input type="text" class="inputfield ml-2"  v-model="conf.delimiter" style="width:80px">
					</div>
					<div class="col-sm-auto d-flex justify-content-md-start">
						Quote :
					</div>
					<div class="col-sm-auto d-flex justify-content-md-start">
						<select class="custom-select" id="quote" v-model="conf.quoteIndex">
							<option v-for="(key,index) in Object.keys(delimiters)" :key="index" :value="index">{{delimiters[key]}}</option>
						</select>
					</div>
					<div v-if="conf.quoteIndex==(delimitersKeys.length-1)" class="col-sm-auto d-flex justify-content-md-start">
						<input type="text" class="inputfield ml-2"  v-model="conf.quote" style="width:80px">
					</div>
					<div class="col-sm-auto d-flex justify-content-md-start">
						Has Header :
					</div>
					<div class="col-sm-auto "><div class="form-check  "><input type="checkbox" class="form-check-input big-checkbox"  v-model="conf.hasHeader" id="flexCheckDefault"></div></div>
					
					<div class="col-sm-auto d-flex justify-content-md-start">
						Column :
					</div>
					<div class="col-sm-auto d-flex justify-content-md-start">
						 <select class="custom-select" id="columnSelect" v-model="conf.columnIndex">
						 
							<option v-for="(col,index) in columns" :selected="index==conf.columnIndex" :key="index" :value="index">{{col.label}}</option>
							
						  </select>
					</div>
					<div class="col-sm-auto d-flex justify-content-md-start">
						<button  class="btn btn-labeled btn-primary" @click="saveSettings()">Save settings</button>
					</div>
				</div>
			</div>
        </div>
		<div v-if="prevRows.length>0" class="container">
			<div class="row w-100">
				<div class="col m-2 alert alert-warning">
					Save the settings to update the plot
				</div>
			</div>
			<div class="row w-100">
				<div class="col">
					<img :src="'plot/'+fid+'?'+time">
				</div>
			</div>
			<div class="row w-100">
				<div class="col">	This preview shows only the first 10 rows</div>
			</div>
		</div>
		<div class="row w-100">
			<div class="col">
				<div class="row w-100">
					<div class="col" id="prevTblBenford">
						
					</div>
				</div>
			</div>
        </div>
	</div>
	
</template>

<script>
/**
 * Configure the csv reader by setting delimiter, quotechar, determining the columns names, and selecting the column used as the input of
 * Benford's law algorithm
 */
export default {
	/**
	 * Add a table to display the data of the flat file
	 */
	created(){
		let bf=this;
		bf.proxy.$data.delimitersKeys=Object.keys(bf.proxy.$data.delimiters);
		window.L7.loader.loadComponentTo("ltable", "bfTableDiv", $("#prevTblBenford"),{columns:[],loader:(startIndex,callBack)=>{return bf.dataLoader(startIndex,callBack);}},(comp)=>{bf.proxy.$data.table=comp});
	},
	/**
	 * Table uses this to load the data of the flat file
	 * @param {*} index 
	 * @param {*} callBack 
	 */
	dataLoader(index,callBack){
		let bf=this;
		if(this.proxy.$data.data&&this.proxy.$data.data.length>0){
			callBack({columns:this.proxy.$data.columns,data:this.proxy.$data.data,totalPages:1,rowsPerPage:10});
		}
	},
	methods:{
		/**
		 * Save the settings of the flat file in db and plot the histogram again
		 */
		saveSettings(){
			let conf=this.$data.conf;
			this.saveSettingsOnServerAsync(this.$data.fid,conf.hasHeader,conf.delimiter,conf.quote,conf.columnIndex,(res)=>{
				this.$data.time=$.now();
			});
		},
		/**
		 * Shows a dialog to select the flat file
		 */
		selectFile(){
			let buttons={
				Select:(evt)=>{
					let bf=this;
					let fid=this.fileManager.proxy.getSelectedRow();
					this.$data.time=$.now();
					var promise = new Promise((resolve, reject)=> {
						bf.loadFile(fid,resolve, reject);
					});
					promise.then(()=>{
						
						bf.$data.table.proxy.reloadData()
						
						
					});
					
					this.$data.fileDialog.dialog("close");
					return true;
				},
				Cancel:(evt)=> {

					this.$data.fileDialog.dialog("close");
					return true;
				}}
			
			this.$data.fileDialog= window.L7.loadComponentToDialog("filemanager",{},(comp)=>{this.$data.fileManager=comp},{width:"90%",height:"600"},buttons);
		},
		/**
		 * 
		 * @param {string} str delimiter
		 * @returns return the index of the delimiter 
		 */
		findKey(str){
			let ret=this.delimitersKeys.indexOf(str);
			if(ret==-1){
				ret=this.delimitersKeys.length-1;
			}
			return ret;
		},
		/**
		 * 
		 * @param {string} fid fileid
		 * @param {function} resolve Promise's resolve
		 * @param {function} reject  Promise's reject
		 */
		loadFile(fid,resolve,reject){
			let bf=this;
			bf.$data.fid=fid;
			bf.loadConfAsync(fid,(res)=>{
				
				bf.$data.conf=Object.assign({hasHeader:true,delimiter:',',columnIndex:0,delimiterIndex:0,quote:'"',quoteIndex:2},res.result);
				let delKeys=Object.keys(this.$data.delimiters)
				
				bf.$data.conf.delimiterIndex=this.findKey(bf.$data.conf.delimiter);
				bf.$data.conf.quoteIndex=this.findKey(bf.$data.conf.quote);
				
				
				this.previewAsync(fid,10,(res)=>{
				
					
					
					if(res.result.length>0){
						
						bf.$data.prevRows=res.result;
						bf.process();
						resolve();
					}else{
						window.L7.showDialog("File is empty");
						reject();
					}
				});
			});
		},
		/**
		 * Process the flat file data, using Papa's parser using the settings.
		 */
		process(){
			this.$data.columns=[];
			this.$data.data=[];
			let maxColumnNum=0;
			
			if(this.$data.conf.delimiterIndex<this.$data.delimitersKeys.length-1){
				this.$data.conf.delimiter=this.$data.delimitersKeys[this.$data.conf.delimiterIndex]
			}
			if(this.$data.conf.quoteIndex<this.$data.delimitersKeys.length-1){
				this.$data.conf.quote=this.$data.delimitersKeys[this.$data.conf.quoteIndex]
			}
			let prevData = Papa.parse(this.$data.prevRows,{quoteChar:this.$data.conf.quote,escapeChar:this.$data.conf.quote,delimiter:this.$data.conf.delimiter,header:this.$data.conf.hasHeader});
			for(let i=0;i<prevData.data.length-1;i++){
				let columns=prevData.data[i];
				maxColumnNum=Math.max(maxColumnNum,columns.length);
				this.$data.data[i]=columns;
				
			}
			if(this.$data.conf.hasHeader){
				let headers=prevData.meta.fields;
				for(let i=0;i<headers.length;i++){
					this.$data.columns[i]={label:headers[i]};
				}
			}else{
				for(let i=0;i<maxColumnNum;i++){
					this.$data.columns[i]={label:"Column_"+i};
				}
			}
				this.$data.conf.columnIndex=Math.min(this.$data.conf.columnIndex,this.$data.columns.length-1);
			
		}
		
		
	},
	data(){
		return {fileDialog:null,
			fileManager:null,
			prevRows:[],
			data:[],
			columns:[],
			conf:{hasHeader:true,delimiter:',',columnIndex:0,delimiterIndex:0,quote:'"',quoteIndex:2},
			delimitersKeys:[],
			fid:"",
			time:0,
			delimiters:{
				',':',',
				';':';','"':'"','\'':'\'',
				' ':'[Space]',
				'\t':'[Tab]',
				'Others':'Others'
			}
		}
	},
	   
	watch: {
		conf: {
			handler: function(val,o){
			this.process();
			this.$data.table.proxy.reloadData()
		},deep: true}
	}
};
</script>
<style>
</style>