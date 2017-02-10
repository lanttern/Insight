function chart(results){
  var gaugeChart = AmCharts.makeChart( "chartdiv1", {
  "type": "gauge",
  "theme": "light",
  "axes": [ {
    "axisThickness": 1,
    "axisAlpha": 0.2,
    "tickAlpha": 1,
    "valueInterval": 10,
    "bands": [ {
      "color": "#84b761",
      "endValue": 40,
      "innerRadius": "75%",
      "startValue": 0
    }, {
      "color": "#fdd400",
      "endValue": 60,
      "innerRadius": "75%",
      "startValue": 40
    }, {
      "color": "#cc4748",
      "endValue": 100,
      "innerRadius": "75%",
      "startValue": 60
    } ],
    "bottomText": "Your risk is: \n" + results + " %",
    "bottomTextYOffset": -20,
    "endValue": 100
  } ],
  "arrows": [ {"value": results} ],
  "export": {
    "enabled": false
  }
} );
}

function chart2(){
  var max_value = 0.0477;
  var chart = AmCharts.makeChart("chartdiv2", {
  "type": "serial",
  "theme": "light",
  "marginRight": 70,
  "dataProvider": [
    {
    "risk factor": "stroke seizure",
    "risk level": Math.round(4.76/max_value),
  },
  {
    "risk factor": "stroke age",
    "risk level": Math.round(3.23/max_value),
  },
  {
    "risk factor": "atrial fibrillation",
    "risk level": Math.round(3.08/max_value),
  },
  {
    "risk factor": "prior stroke",
    "risk level": Math.round(2.86/max_value),
  },
    {
    "risk factor": "mother stroke",
    "risk level": Math.round(2.84/max_value),
  },
  {
    "risk factor": "intracerebral hemorrhage",
    "risk level": Math.round(2.75/max_value),
  },
  {
    "risk factor": "aneurysm",
    "risk level": Math.round(2.68/max_value),
  },
  {
    "risk factor": "atrial fibrillation and coumadin",
    "risk level": Math.round(2.56/max_value),
  },
     {
    "risk factor": "subarachnoid hemorrhage",
    "risk level": Math.round(2.50/max_value),
  },
  {
    "risk factor": "hypertension",
    "risk level": Math.round(2.3/max_value),
  },
  {
    "risk factor": "high cholesterol",
    "risk level": Math.round(2.28/max_value),
  },
  {
    "risk factor": "mucin cystadenoma",
    "risk level": Math.round(2.25/max_value),
  },
    {
    "risk factor": "neurological disease",
    "risk level": Math.round(2.25/max_value),
  },
  {
    "risk factor": "mellitus dermatomes",
    "risk level": Math.round(2.18/max_value),
  },
  {
    "risk factor": "early stroke",
    "risk level": Math.round(2.08/max_value),
  },
  {
    "risk factor": "history stroke",
    "risk level": Math.round(2.05/max_value),
  },
  {
    "risk factor": "hypertension medical condition",
    "risk level": Math.round(1.72/max_value),
  },
  {
    "risk factor": "hemorrhage",
    "risk level": Math.round(1.61/max_value),
  },
  {
    "risk factor": "hypertension medical condition",
    "risk level": Math.round(1.72/max_value),
  },
  {
    "risk factor": "cardiac sentation",
    "risk level": Math.round(1.24/max_value),
  },
  {
    "risk factor": "tobacco and alcohol",
    "risk level": Math.round(1.14/max_value),
  },
  {
    "risk factor": "social alcohol",
    "risk level": Math.round(1.09/max_value),
    "test": "test",
  },
  {
    "risk factor": "macular degeneration",
    "risk level": Math.round(0.81/max_value),
  },
  {
    "risk factor": "borderlin diabetes",
    "risk level": Math.round(0.65/max_value),
  },
  {
    "risk factor": "hypertension diabetes",
    "risk level": Math.round(0.47/max_value),
  },
  {
    "risk factor": "current smoker",
    "risk level": Math.round(0.19/max_value),
  },
  {
    "risk factor": "memory problem",
    "risk level": Math.round(0.17/max_value),
  },
  {
    "risk factor": "nitric oxid",
    "risk level": Math.round(0.16/max_value),
  },
  {
    "risk factor": "smoke drink",
    "risk level": Math.round(0.15/max_value),
  },
  ],
  "valueAxes": [{
    "axisAlpha": 0,
    "position": "left",
    "title": "Relevant to stroke"
  }],
  "startDuration": 1,
  "graphs": [{
    "balloonText": "<b>[[category]]: [[value]]</b>",
    "fillColorsField": "color",
    "fillAlphas": 0.9,
    "lineAlpha": 0.2,
    "type": "column",
    "valueField": "risk level"
  }],
  "chartCursor": {
    "categoryBalloonEnabled": true,
    "cursorAlpha": 0,
    "zoomable": true
  },
  "categoryField": "risk factor",
  "categoryAxis": {
    "gridPosition": "start",
    "labelRotation": 45
  },
  "export": {
    "enabled": false
  }

});
}

chart2();
chart(results);
