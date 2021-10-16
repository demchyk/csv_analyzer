{% extends 'layouts.tpl' %}
{% block body_container %}
{% if error %}
<script>alert('{{error}}')</script>
{% endif %}

<form method = 'POST' class = 'position-relative' id = 'data-load'>

	<div id="svg_wrap"></div>


	<section>
		<p>Choose cell technology</p>
		<select onchange="get_button(this);" required="" name= 'zte_type' class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
			  <option value = ''selected></option>
			  <option value="WCDMA">WCDMA</option>
			  <option value="LTE">LTE</option>
			  <option value="GSMV3">GSMV3</option>
		</select>
		<br>
		<div class="checkbox">
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

