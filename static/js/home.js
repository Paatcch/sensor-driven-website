"use strict";
/* global document XLMHttpRequest */

const latCO2 = document.querySelector('#latCO2');
const latCO2_time = document.querySelector('#latCO2_time');
const latTVOC = document.querySelector('#latTVOC');
const latTVOC_time = document.querySelector('#latTVOC_time');

const maxCO2 = document.querySelector('#maxCO2');
const maxCO2_time = document.querySelector('#maxCO2_time');
const maxTVOC = document.querySelector('#maxTVOC');
const maxTVOC_time = document.querySelector('#maxTVOC_time');

const minCO2 = document.querySelector('#minCO2');
const minCO2_time = document.querySelector('#minCO2_time');
const minTVOC = document.querySelector('#minTVOC');
const minTVOC_time = document.querySelector('#minTVOC_time');

function getMeasurements(){
    const request = new XMLHttpRequest();
    request.open('GET', '/updateMeasurements', true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.onload = function(){
        const response = JSON.parse(request.responseText)

        latCO2.textContent = `Latest value: ${response.latCO2[0]}`;
        latCO2_time.textContent = `Time: ${response.latCO2[1]}`;
        latTVOC.textContent = `Latest value: ${response.latTVOC[0]}`;
        latTVOC_time.textContent = `Time: ${ response.latTVOC[1]}`;

        maxCO2.textContent = `Maximum value: ${response.maxCO2[0]}`;
        maxCO2_time.textContent = `Time: ${response.maxCO2[1]}`;
        maxTVOC.textContent = `Maximum value: ${response.maxTVOC[0]}`;
        maxTVOC_time.textContent = `Time: ${response.maxTVOC[1]}`;
        
        minCO2.textContent = `Minimum value: ${response.minCO2[0]}`;
        minCO2_time.textContent = `Time: ${response.minCO2[1]}`;
        minTVOC.textContent = `Minimum value: ${response.minTVOC[0]}`;
        minTVOC_time.textContent = `Time: ${response.minTVOC[1]}`;
    };
    request.send();
}

if (latCO2, latCO2_time, latTVOC, latTVOC_time, minCO2, minCO2_time,
     minTVOC, minTVOC_time, maxCO2, maxCO2_time, maxTVOC, maxTVOC_time){
    setInterval(getMeasurements, 3000);
    getMeasurements();
}


