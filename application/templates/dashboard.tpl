{% extends 'layouts.tpl' %}
{% block body_container %}

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
 	<div class="button" id="prev">&larr; Previous</div>
	<div class="button" id="next">Next &rarr;</div>
	<button class="btn sub_button" type="submit" id="submit" >Submit</button> 
</form>




{% endblock %}

