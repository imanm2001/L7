<template>
	<div class="row w-100 m-2 align-middle">
		<div class="col  justify-content-md-start d-flex m-2 font-weight-normal">
		<button  class="btn btn-labeled btn-success m-2" :disabled="startIndex==1" @click="prevPage()">&lt;</button>
		<div class="font-weight-normal m-2">
		{{startIndex}}/{{totalPages}}
		</div>
		<button  class="btn btn-labeled btn-success m-2" :disabled="startIndex==totalPages" @click="nextPage()">&gt;</button>
		</div>
	</div>
	<table class="table table-striped">
		<thead>
			<tr>
				<th scope="col">#</th>
				<th v-for="col in tableData.columns">{{col.label}}</th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="(row,index) in tableData.data" role="button" :class="String(selRow==index?'table-primary':'')" @click="select(index)">
				<th scope="row">{{index+1}}</th>
				<td class="overflow-hidden" v-for="(col,index) in row">
					<div  v-if="index<tableData.columns.length&& tableData.columns[index].hasOwnProperty('isHTML')&&tableData.columns[index].isHTML" v-html="col"></div>
					<div  v-else >{{ col }}</div>
				</td>
			</tr>
		</tbody>
	</table>

</template>

<script>
	/** 
	 *  Table will load the data through by calling loader (function) . The loader can either return the who data, or a part of it in a page.
	 * 
	 */
export default {
	/**
	 * Load the data for the first page
	 */
	created(){
		this.proxy.reloadData(1);
	},

	methods:{
		/**
		 * @returns the index of the selected row in the whole dataset as loader might provide a portion of the dataset
		 */
		getSelectedRow(){
			
			return (this.$data.startIndex-1)*this.$data.rowsPerPage+this.$data.selRow
		},
		/**
		 * select a specifc row of the table
		 * @param {int} index selected row
		 */
		select(index){
			this.$data.selRow=index;
		},
		/**
		 * Displays the next page
		 */
		nextPage(){
		
			this.$data.startIndex=Math.min(this.$data.totalPages,this.$data.startIndex+1);
			this.reloadData();
			
		},
		/**
		 * Displays the previous page
		 */
		prevPage(){
		
			this.$data.startIndex=Math.max(1,this.$data.startIndex-1);
			this.reloadData();
			
		},
		/**
		 * Reload the data by calling the loader and using the page index
		 */
		reloadData(){
			if(this.loader){
				let tbl=this;
				this.loader(this.$data.startIndex,(data)=>{
					tbl.$data.tableData=data;
					this.$data.totalPages=data.totalPages;
					this.$data.rowsPerPage=data.rowsPerPage;
					this.$data.startIndex=Math.min(this.$data.startIndex,data.totalPages);
				});
				
			}
		}
	},
/**
 * @returns{
 * 	tableData {rows Array{String}, columns{Array{Dictionary}}}: rows in the current page. Each row is an array of strings. 
 * 			columns has the following structure {label: String, isHTML}. label determines the title of the column and if isHTML is set,
 * 			the content of the column will be added to cell without strelizing it
 *  loader {function(index {int}, callback {function(data)})} loads the data based on the index and send it  to the callback function}
 * startIndex {int} the index of page which is used to load the data
 * selRow {int} the selected row
 * rowsPerPage {int} number of the rows in each page
 */
	data(){
		return {tableData:{},loader:null,startIndex:1,totalPages:1,selRow:-1,rowsPerPage:10}
	   }
	};
</script>
<style>
</style>