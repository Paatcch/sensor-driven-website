"use strict";
/* global document XLMHttpRequest */

//Get the timezone offset in milliseconds
const time_offSet_in_ms = new Date().getTimezoneOffset()*60*1000;

//parts that should be hidden or shown depending on if there is data in the database
const no_data_message = document.querySelector('#NoDataMessage');
const outer_container_for_measurements = document.querySelector('#outerContainerForMeasurements');

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
        if(request.status === 200){
            const response = JSON.parse(request.responseText);
            if(!response.latCO2 || !response.latTVOC){ //If there are no data in the database
                no_data_message.removeAttribute('hidden');
                outer_container_for_measurements.setAttribute('hidden', '');
            }else{
                no_data_message.setAttribute('hidden', '');
                outer_container_for_measurements.removeAttribute('hidden');
                latCO2.textContent = response.latCO2[0];
                latCO2_time.textContent = to_local_time(response.latCO2[1]);
                latTVOC.textContent = response.latTVOC[0];
                latTVOC_time.textContent = to_local_time(response.latTVOC[1]);
        
                maxCO2.textContent = response.maxCO2[0];
                maxCO2_time.textContent = to_local_time(response.maxCO2[1]);
                maxTVOC.textContent = response.maxTVOC[0];
                maxTVOC_time.textContent = to_local_time(response.maxTVOC[1]);
                
                minCO2.textContent = response.minCO2[0];
                minCO2_time.textContent = to_local_time(response.minCO2[1]);
                minTVOC.textContent = response.minTVOC[0];
                minTVOC_time.textContent = to_local_time(response.minTVOC[1]);
            }
        }else{
            console.error(`ERROR: ${request.status}`);
        }
    };
    request.send();
}

//converts the time in UTC from the databse to the local time dependent on where the user is.
function to_local_time(UTC_time){
    const time_UTC_obj = new Date(UTC_time);
    const time_local_obj = new Date(time_UTC_obj.getTime() - time_offSet_in_ms);
    console.log(time_local_obj.toLocaleString());
    return time_local_obj.toLocaleString();
}

if (latCO2, latCO2_time, latTVOC, latTVOC_time, minCO2, minCO2_time,
     minTVOC, minTVOC_time, maxCO2, maxCO2_time, maxTVOC, maxTVOC_time){
    setInterval(getMeasurements, 60000);
    getMeasurements();
}


