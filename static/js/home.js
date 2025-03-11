"use strict";
/* global document XLMHttpRequest */

const latCO2 = document.querySelector('#latCO2');
const latCO2_time = document.querySelector('#latCO2_time');
/*
const latTVOC = document.querySelector('#latTVOC');
const minCO2 = document.querySelector('#minCO2');
const maxCO2 = document.querySelector('#maxCO2');
const minTVOC = document.querySelector('#minTVOC');
const maxTVOC = document.querySelector('#maxTVOC');
*/
console.log('aaah');

function getMeasurements(){
    const request = new XMLHttpRequest();
    request.open('GET', '/updateMeasurements', true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.onload = function(){
        const response = JSON.parse(request.responseText)
        console.log('ugabug');
        latCO2.textContent = response.latCO2; //Jeg er ikke sikker på latCO2["CO2"]
        console.log('ugabug2');
        //latCO2_time.textContent = response.latCO2["time"];
    };
    request.send();
}

if (latCO2){ //latCO2_time, latTVOC, minCO2, minTVOC, maxCO2, maxTVOC
    console.log('aaah');
    setInterval(getMeasurements, 3000); //Skal sættes til 60000 (1 minut)
    getMeasurements();
}else{
    console.log('hmm');
}


