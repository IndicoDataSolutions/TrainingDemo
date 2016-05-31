$(document).ready(function() {
	$("img.search-result").click(function() {
		$(this).toggleClass("selected");
	});
});

$(document).ready(function() {
	$("#addData").click(function() {
		var collection = $(".panel-title>h4").contents().filter(function(){ 
			return this.nodeType == 3; 
		})[0].nodeValue.trim();
		console.log(collection);
		var api_key = $("#apiKey").val();
		var selectedImages = $("img.selected");
		var label = $("#dataLabel").val();
		var dataArray = [];
		selectedImages.each(function(index, value){
			dataArray.push([value.getAttribute("data-source"), label]);
		});

		addData(
			dataArray,
			collection,
			api_key,
			function(resp){
				alert(resp);
				$("img.selected").toggleClass("selected");
		});
	});
});

$(document).ready(function() {
	$("#previewPredict").click(function() {
		var collection = $(".panel-title>h4").contents().filter(function(){ 
			return this.nodeType == 3; 
		})[0].nodeValue.trim();
		var dataUrl = $("#dataUrl").val();
		var api_key = $("#apiKey").val();
		predict(dataUrl, collection, api_key, function(resp) {
			alert(resp);
		});
	});
});

function predict(data, collection, api_key, callback) {
	var log = function(res){ console.log(res) };
	var url = 'https://apiv2.indico.io/custom/predict?key=' + api_key;

	var callback = callback || log;

	$.post(url, JSON.stringify({
		data: data,
		collection: collection
	}), callback);
}

function addData(data, collection, api_key, callback) {
	var log = function(res){ console.log(res) };
	var url = 'https://apiv2.indico.io/custom/batch/add_data?key=' + api_key;

	var callback = callback || log;

	$.post(url, JSON.stringify({
		data: data,
		collection: collection
	}), callback);
}
