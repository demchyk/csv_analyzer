{% extends 'layouts.tpl' %}
{% block body_container %}
{% if error %}
<script>alert('{{error}}')</script>
{% endif %}

<form action = '/load-data-action' method = 'POST' class = 'position-relative' id = 'data-load'>
	<select required="" name= 'zte_type' class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
	  <option value = '' disable selected>Choose cell technology</option>
	  <option value="WCDMA">WCDMA</option>
	  <option value="LTE">LTE</option>
	  <option value="GSMV3">GSMV3</option>
	</select>
 	<br>
	<button type="submit" class="btn btn-primary btn-lg position-relative top-100">Submit</button> 
</form>
{% endblock%}