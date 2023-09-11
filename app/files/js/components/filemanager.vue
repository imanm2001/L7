<template>
<div class="container d-flex justify-content-center mt-100">
    <div class="row w-100">
        <div class="col-md-12">

			<div class="file-drop-area w-100" style="background-color: lightblue;">
			  <span class="choose-file-button">Choose files</span>
			  <span class="file-message w-100">or drag and drop files here</span>
			  <input class="file-input" type="file" multiple>
			</div>
            
        </div>
        
    </div>
    
    
</div>
<div id="tableFMContainer">
	
</div>
</template>

<script>
/**
 List all uploaded files by the user
	Upload new files
	Delete existing files
*/
export default {
/**
 * This function is passed to the table to list the uploaded files
 * @param {int} index index of the page that loads the files
 * @param {function (data)} callBack after geting the list of the files, it is fed to the table through callBack
 */
	dataLoader(index,callBack){
		let fm=this;
		this.proxy.listFilesAsync(index,(res)=>{
			
			fm.proxy.files=[];
			fm.proxy.fids=[];
			let resFiles=res.result.files;
			for(var i=0;i<resFiles.length;i++){
				let resFile=resFiles[i]
				fm.proxy.files[i]=[resFile.filename,resFile.date,'<button type="button" class="btn btn-danger fm-rm-but" fid="'+resFile.id+'" fname="'+resFile.filename+'">&#x2716;</button>'];
				fm.proxy.fids[i]=resFile.id
			}
			callBack({columns:[{label:'Filename'},{label:'Date'},{label:'Delete',isHTML:true}],data:fm.proxy.files,totalPages:res.result.totalPages,rowsPerPage:10});
			this.table.proxy.$nextTick().then((v)=>{
				fm.htmlTag.find(".fm-rm-but").off('click').on("click",function(){
					fm.proxy.removeFile($(this).attr("fid"),$(this).attr("fname"));
				});
			});
		});
	},
	/**
	 * Add the drag and drop area for uploading the files
	 */
	created(){
		let fm=this;
		$('.file-input').off('change').on('change',  function() {
			var files=$(this)[0].files;
			var filesCount = files.length;
			var textbox = $(this).prev();
			if (filesCount === 1) {
				var fileName = $(this).val().split('\\').pop();
				textbox.text(fileName);
			} else {
				textbox.text(filesCount + ' files selected');
			}
			var fd = new FormData();
			for(var i=0;i<filesCount;i++){
				fd.append('file'+i,files[i]);
			}
			fd.append('csrfmiddlewaretoken', window.L7.getCSRF());
			 $.ajax({
				 url: '/upload',
				 type: 'post',
				 data: fd,
				 contentType: false,
				 processData: false,
				 dataType: 'json',
				 success: function(response){
					  fm.table.proxy.reloadData();
				}
			});
		});
		window.L7.loader.loadComponentTo("ltable", "fmTableDiv", $("#tableFMContainer"),{columns:[],loader:(startIndex,callBack)=>{return fm.dataLoader(startIndex,callBack);}},(comp)=>{fm.table=comp});
	}
	,
	methods: {
		/**
		 * @returns returns the file id
		 */
		getSelectedRow(){
			let selFile=this.$.type.table.proxy.getSelectedRow();
			return this.$data.fids[selFile];
		},
		/**
		 * Shows a dialog to confim deleting the file
		 * @param {String} fid file id
		 * @param {Strubg} fname file name
		 */
		removeFile(fid,fname){
			var fm=this;
			
			window.L7.showDialog("Do you want to delete:<br>"+fname,{
				resizable: true,
				modal: true,
				position: {
					my: "center ",
					at: "center ",
					of: window
				},
				closeText: "Close",
			
					
				},{
				'Yes': function () {
					fm.delFileAsync(fid,(res)=>{
						if(!res.result){
							 window.L7.showDialog("An error happend");
						}
						fm.$.type.table.proxy.reloadData();
						});
					$(this).dialog("close");
					return true;
				},
				'No': function () {
					$(this).dialog("close");
					return true;
					}
				});
		}
	},
	/**
	 * @returns {fids: string[] file ids
	 * 			files: string[] file names}
	 */
	data(){
		return {fids:[],files:[[]]}
	}
};
</script>
<style>
</style>
