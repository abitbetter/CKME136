<!doctype html>
<html>
	<head>
		<title>Restaurant Recommendations</title>
		
		<meta charset="utf-8">

		<meta name="viewport" content="width=device-width, initial-scale=1">

		<script src="https://code.jquery.com/jquery-1.9.1.min.js" type="text/javascript"></script>

		<!-- Latest compiled and minified CSS -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/
		bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
		
		<!-- Optional theme -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/
		bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

		<link type="text/css" rel="stylesheet" href="styles/main.css?<?php echo time(); ?>" />	
		<link href='https://fonts.googleapis.com/css?family=Nunito:400,300' rel='stylesheet' type='text/css'>
	</head>
	<body>
		<form>
			<div style="margin-top:50px;" class="container">
					<div class="row"> 
						<div class="col-sm-12 col-xs-12">
							<div class="panel panel-default">
								<div class="panel-heading" style='text-align:center;'>
									<h2>Restaurant Recommender System</h2>
								</div>
								<div class="panel-body">
									<fieldset>
								    <label class='block-when-small' for="price">Price Range:</label>
								    <select id='price' name='price'>
										<option value='1'>Low</option>
										<option value='2'>Mid Range</option>
										<option value='3'>High</option>
									</select>
								    <label class='left-margins block-when-small' for="price">Decor/Atmosphere:</label>
									<select id='decor' name='decor'>
										<option value='1'>Moderate</option>
										<option value='2'>Good</option>
										<option value='3'>Excelent</option>
									</select>
									<label class='left-margins block-when-small' for="price">Food Quality:</label>
									<select id='quality' name='quality'>
										<option value='1'>Moderate</option>
										<option value='2'>Good</option>
										<option value='3'>Excelent</option>
									</select>
									<label class='left-margins block-when-small' for="price">Service:</label>
									<select id='service' name='service'>
										<option value='1'>Moderate</option>
										<option value='2'>Good</option>
										<option value='3'>Excelent</option>
									</select>
								    </fieldset><br>
									<label for="price">Date and Time:</label>
									<input id="datetime" type="datetime-local" name='datetime' value="2017-10-01T07:00:00" required><br><br>

									<input id='submit' class="btn btn-success" type="submit" value="Submit Query" style='width:100%;'><br><br>
									<input id='similar' class="btn btn-success" type="submit" value="Find Similar Restaurants" style='width:100%; margin-bottom:0;'>
									<input id='button_storage' type="hidden" value="default value">
								</div>
							</div>
						</div>
						<!-- hide this until results are available -->
						<div id='recommendation' class="hide col-sm-12 col-xs-12">
							<div class="panel panel-default">
								<div class="panel-heading" style='text-align:center;'>
									<h2>Recommended Restaurants</h2>
								</div>
								<div class="panel-body">
									<div id="loading-image" style="text-align:center;">Processing Request</div>
									<div id="rest1"></div>
									<div id="feat1"></div><br>
									
									<div id="rest2"></div>
									<div id="feat2"></div><br>

									<div id="rest3"></div>
									<div id="feat3"></div><br>

									<div id="tweak"></div>

									<div id="test"></div>
								</div>
							</div>
						</div>
						
					</div>
				</div>
				<div class="body-push"></div>
			</div>

			<input id='prev_recommendation' type="hidden" value='999'>

			<script>
				$('#similar').removeClass("show").addClass("hide")

				//this determines what button was pressed
				$("#submit").click(function(){
					$('#button_storage').val('submit');
				});
				$("#similar").click(function(){
					$('#button_storage').val('similar');
				});

				$('form').on('submit', function(event){
					$('#recommendation').removeClass("hide").addClass("show")
					$('#rest1').removeClass("show").addClass("hide")
					$('#feat1').removeClass("show").addClass("hide")
					$('#rest2').removeClass("show").addClass("hide")
					$('#feat2').removeClass("show").addClass("hide")
					$('#rest3').removeClass("show").addClass("hide")
					$('#feat3').removeClass("show").addClass("hide")
					$('#tweak').removeClass("show").addClass("hide")
					$('#loading-image').show();

					$.ajax({
						datatype : "JSON",
						data: {
							'price' : $('#price').val(),
							'decor' : $('#decor').val(),
							'quality' : $('#quality').val(),
							'service' : $('#service').val(),
							'datetime' : $('#datetime').val(),
							'action' : $('#button_storage').val(),
							'prev_recommendation' : $('#prev_recommendation').val()
						},
						type : 'POST',
						url : '../cgi-bin/recommender/recommender.py',
					}).done(function(response) {
						var json = JSON.parse(response);
						$('#prev_recommendation').val(json.previous_data.rest_id)

						var rating = {}
						rating['rating1'] = json.rating1;
						rating['rating2'] = json.rating2;
						rating['rating3'] = json.rating3;

						if(json.success == false) {
							var dt = new Date($.now());
							$('#rest1').text(json.message + ' ' + dt);
							$('#rest1').removeClass("hide").addClass("show")					
						}
						else{
							var i = 1

							if(json.action === 'submit') {
								$.each(json.data, function(key, value){
									console.log(key, value)
									$('#rest'+i).html('Recommendation ' + i + ':<br>' + key);
									$('#feat'+i).text(value);
									$('#rest'+i).removeClass("hide").addClass("show")
									$('#feat'+i).removeClass("hide").addClass("show")
									i++;
								});
							} 
							else {
								$.each(json.data, function(key, value){
									console.log(key, value)
									var rating_value = rating['rating' + i];
									$('#rest'+i).html('Recommendation ' + i + ': ' + '(score: ' + rating_value + ')' + '<br>' + key);
									$('#feat'+i).text(value);
									$('#rest'+i).removeClass("hide").addClass("show")
									$('#feat'+i).removeClass("hide").addClass("show")
									i++;
								});
							}
							if(json.tweak == true) {
								$('#tweak').text("The following criteria in your query were modified: " + json.tweak_message);
								$('#tweak').removeClass("hide").addClass("show")
							}
						}
						
						$('#loading-image').hide()
						$('#similar').removeClass("hide").addClass("show")
					});

					event.preventDefault(); //prevent html form from automatically refreshing page when form is submitted(ie override default behaviour)
				})
			</script>
		</form>
	</body>
	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
	<!-- Latest compiled and minified JavaScript -->
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" 
	integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" 
	crossorigin="anonymous"></script>
</html>