{% extends 'layouts.tpl' %}
{% block body_container %}
{% if error %}
<script>alert('{{error}}')</script>
{% endif %}

<form action = '/export-to-csv-action' method = 'POST' class = 'position-relative' id = 'data-load' enctype="multipart/form-data">

	<div id="svg_wrap"></div>


	<section>
	<div class="form_container export_to_csv_container">
	<input type="file" name="export_to_csv_input_file" id="export_to_csv_input_file" class="inputfile inputfile-4" accept=".pkl" />
	<label for="export_to_csv_input_file"><figure><svg xmlns="http://www.w3.org/2000/svg" width="20" height="17" viewBox="0 0 20 17"><path d="M10 0l-5.2 4.9h3.3v5.1h3.8v-5.1h3.3l-5.2-4.9zm9.3 11.5l-3.2-2.1h-2l3.4 2.6h-3.5c-.1 0-.2.1-.2.1l-.8 2.3h-6l-.8-2.2c-.1-.1-.1-.2-.2-.2h-3.6l3.4-2.6h-2l-3.2 2.1c-.4.3-.7 1-.6 1.5l.6 3.1c.1.5.7.9 1.2.9h16.3c.6 0 1.1-.4 1.3-.9l.6-3.1c.1-.5-.2-1.2-.7-1.5z"/></svg></figure> <span>Choose a pickle&hellip;</span></label>
	</div>
	<div class="checkbox_export_csv">
		<label>
			<input type="checkbox" name="cluster_check" value="cluster"> <span>Analyze only nodes from cluster.txt</span>
		</label>
	</div>
	</section>
 	<section>
 		<p>Select date interval</p>
		<div id="reportrange" style="background: #fff; cursor: pointer; padding: 5px 10px; border: 1px solid #ccc; width: 100%">
			<i class="fa fa-calendar"></i>&nbsp;
		<span></span><input type="text" name="daterange" class ="disabled_input disabled"> <i class="fa fa-caret-down"></i>
		</div>
	</section>
 	<section>
 		<p>Choose agregation cell type</p>
	 	<select required=""  name= 'aggregation_cell_type' class="form-select form-select-lg mb-3 " aria-label=".form-select-lg example">	
			<option value = '' disable selected></option>
			<option value="CELL">Cell</option>
			<option value="NODE">Node</option>
			<option value="CLUSTER">Whole Cluster</option>
		</select>

		<p>Choose agregation time type</p>
	 	<select  required="" name= 'aggregation_time_type' class="form-select form-select-lg mb-3 " aria-label=".form-select-lg example">	
			<option value = '' disable selected></option>
			<option value="H">Hour</option>
			<option value="D">Day</option>
			<option value="7D">7 Days</option>
			<option value="MS">Month</option>
			<option value="Y">Year</option>
		</select>
	 </section>
 	<div class="button" id="prev">&larr; Previous</div>
	<div class="button" id="next">Next &rarr;</div>
	<button class="btn sub_button" type="submit" id="submit" >Submit</button> 
</form>




{% endblock %}

