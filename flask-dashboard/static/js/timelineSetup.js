/***********************

javascript doesn't work exactly right wityh flask when its in a seperate file

***********************/

function onLoad() {
	var eventSource = new Timeline.DefaultEventSource();
	var bandInfos = [
		Timeline.createBandInfo({
				eventSource:    eventSource,
				date:           "Jun 1 2017 00:00:00 GMT",
				width:          "65%",
				intervalUnit:   Timeline.DateTime.MINUTE,
				intervalPixels: 200
		}),
		Timeline.createBandInfo({
				overview:       true,
				eventSource:    eventSource,
				date:           "Jun 1 2017 00:00:00 GMT",
				width:          "15%",
				intervalUnit:   Timeline.DateTime.HOUR,
				intervalPixels: 300
		}),
		Timeline.createBandInfo({
				overview:       true,
				eventSource:    eventSource,
				date:           "Jun 1 2017 00:00:00 GMT",
				width:          "13%",
				intervalUnit:   Timeline.DateTime.DAY,
				intervalPixels: 400
		}),
		Timeline.createBandInfo({
				overview:       true,
				eventSource:    eventSource,
				date:           "Jun 1 2017 00:00:00 GMT",
				width:          "7%",
				intervalUnit:   Timeline.DateTime.MONTH,
				intervalPixels: 500
		})
	];
	bandInfos[1].syncWith = 0;
	bandInfos[2].syncWith = 1;
	bandInfos[3].syncWith = 2;
	bandInfos[1].highlight = true;
	bandInfos[2].highlight = true;
	bandInfos[3].highlight = true;


	tl = Timeline.create(document.getElementById("my-timeline"), bandInfos);
	{% if org %}
		Timeline.loadXML("../data/events.xml", function(xml, url) { eventSource.loadXML(xml, url); });
		console.log({{org}});
	{% else %}
		Timeline.loadXML("../data/events.xml", function(xml, url) { eventSource.loadXML(xml, url); });
		console.log("no org");
	{% endif %}


	//document.getElementById("timeline-band-0").style.backgroundColor = "red";
	let children = document.getElementById("timeline-band-3").childNodes;
	let children1 = children[0].childNodes;
	let children2 = children1[0].childNodes;
	children2[0].style.backgroundColor = "rgba(170, 170, 170, 0.58)";

	// var icons = document.getElementsByClassName("timeline-event-icon");
	// for (var i = 0; i < icons.length; i++) {
	// 	icons[i];
	// }

}

var resizeTimerID = null;
function onResize() {
		if (resizeTimerID == null) {
				resizeTimerID = window.setTimeout(function() {
						resizeTimerID = null;
						tl.layout();
				}, 500);
		}
}
