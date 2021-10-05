{% extends 'layouts.tpl' %}
{% block body_container %}
{% if error %}
<script>alert('{{error}}')</script>
{% endif %}
<br>
<br>
<form method = 'POST' class = 'position-relative' id = 'data-load'>
	<select required="" name= 'zte_type' class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
	  <option value = '' disable selected>Choose cell technology</option>
	  <option value="WCDMA">WCDMA</option>
	  <option value="LTE">LTE</option>
	  <option value="GSM">GSM</option>
	</select>
 	<br>
	<button type="submit" class="btn btn-primary btn-lg position-relative top-100 start-50 translate-middle-x">Submit</button> 
</form>
{% endblock%}