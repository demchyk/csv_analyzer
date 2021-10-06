{% extends 'layouts.tpl' %}
{% block body_container %}


<br>
<br>

<form method = 'POST' class = 'position-relative' id = 'data-load'>

	<div id="svg_wrap"></div>


	<section>
		<select required="" name= 'zte_type' class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
			  <option value = '' disable selected>Choose cell technology</option>
			  <option value="WCDMA">WCDMA</option>
			  <option value="LTE">LTE</option>
			  <option value="GSM">GSM</option>
		</select>
	</section>



 	<section>
 		<p>Select date interval</p>
 		<input type="text" name="daterange" class="datepicker"/>
 	</section>


 	<section>
	 	<select required="" name= 'agregation_type' class="form-select form-select-lg mb-3 " aria-label=".form-select-lg example">
			  <option value = '' disable selected>Choose agregation type</option>
			  <option value="Cell">Cell</option>
			  <option value="Node">Node</option>
			  <option value="Claster">Claster</option>
		</select>
	 </section>


 	<div class="button" id="prev">&larr; Previous</div>
	<div class="button" id="next">Next &rarr;</div>
	<button class="btn sub_button" type="submit" id="submit" >Submit</button> 
</form>




{% endblock %}

