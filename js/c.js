/* ===========================================================
   STARLIGHT AI
   Enterprise Cybersecurity Recommendation Platform
=========================================================== */

// ==========================================================
// DOM ELEMENTS
// ==========================================================

const form = document.getElementById("assessmentForm");

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const data = {

        Industry: form.Industry.value,

        Employees: form.Employees.value,

        Cloud_Usage: form.Cloud_Usage.value,

        Firewall_Installed: form.Firewall_Installed.value,

        EDR_Installed: form.EDR_Installed.value,

        SIEM_Installed: form.SIEM_Installed.value,

        Security_Budget: form.Security_Budget.value,

        // MULTIPLE SELECT

        Compliance_Requirement:
            Array.from(
                document.getElementById("complianceValue").innerText =
data.Compliance_Requirement.join(", ")),

        Main_Threat_Concern:
            Array.from(
                document.getElementById("threatValue").innerText =
data.Main_Threat_Concern.join(", ")),

    };

    document.getElementById("loader").style.display = "flex";

    const response = await fetch("/predict", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(data)

    });

    const result = await response.json();

    document.getElementById("loader").style.display = "none";

    console.log(result);

    updateDashboard(result);

});

// ==========================================================
// GLOBAL VARIABLES
// ==========================================================

let probabilityChart = null;
let riskGauge = null;

let latestResult = null;
let latestInput = null;

// ==========================================================
// LOADER
// ==========================================================

function showLoader(){

if(loader){

loader.style.display="flex";

}

}

function hideLoader(){

if(loader){

loader.style.display="none";

}

}

// ==========================================================
// THEME
// ==========================================================

const savedTheme = localStorage.getItem("starlight_theme");

if(savedTheme==="light"){

document.body.classList.add("light");

if(themeToggle){

themeToggle.innerHTML='<i class="fa-solid fa-sun"></i>';

}

}

if(themeToggle){

themeToggle.addEventListener("click",()=>{

document.body.classList.toggle("light");

if(document.body.classList.contains("light")){

localStorage.setItem("starlight_theme","light");

themeToggle.innerHTML='<i class="fa-solid fa-sun"></i>';

}else{

localStorage.setItem("starlight_theme","dark");

themeToggle.innerHTML='<i class="fa-solid fa-moon"></i>';

}

});

}

// ==========================================================
// START BUTTON
// ==========================================================

if(startBtn){

startBtn.addEventListener("click",()=>{

document
.getElementById("assessment")
.scrollIntoView({

behavior:"smooth"

});

});

}

// ==========================================================
// FORMATTERS
// ==========================================================

function setText(id,value){

const el=document.getElementById(id);

if(el){

el.innerText=value ?? "--";

}

}

function capitalize(text){

if(!text) return "";

return text
.toString()
.charAt(0)
.toUpperCase()+
text.toString().slice(1);

}

// ==========================================================
// NOTIFICATION
// ==========================================================

function notify(message){

alert(message);

}
// ==========================================================
// FORM SUBMISSION
// ==========================================================

if(form){

form.addEventListener("submit", async function(e){

e.preventDefault();

showLoader();

recommendationCards.innerHTML="";
vendorCards.innerHTML="";

const formData = new FormData(form);

const payload = {};

formData.forEach((value,key)=>{

payload[key]=value;

});

latestInput = payload;

try{

const response = await fetch("/predict",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify(payload)

});

if(!response.ok){

throw new Error("Server Error");

}

const result = await response.json();

latestResult = result;

hideLoader();

// Dashboard
updateDashboard(result);

// Charts
updateCharts(result);

// Recommendation Cards
createRecommendationCards(result);

// Vendor Cards
createVendorCards(result);

// Summary Table
updateSummary(payload);

const resultsSection = document.getElementById("results");

if(resultsSection){
    resultsSection.scrollIntoView({ behavior: "smooth" });
}

}catch(error){

hideLoader();

console.error(error);

notify("Unable to generate recommendation. Please try again.");

}

});

}

// ==========================================================
// UPDATE DASHBOARD
// ==========================================================

function updateDashboard(result){

// Risk Score
setText(

"riskScore",

result.risk_score ?? "--"

);

// Risk Level
setText(

"riskLevel",

capitalize(result.risk_level)

);

// Confidence
setText(

"confidence",

(result.confidence ?? 0)+"%"

);

// Primary Solution
setText(

"primarySolution",

result.primary_solution ?? "--"

);

// AI Explanation
setText(

"explanation",

result.explanation ??

"No explanation available."

);

}

// ==========================================================
// SUMMARY TABLE
// ==========================================================

function updateSummary(data){

industryValue.innerText=data.Industry;

employeeValue.innerText=data.Employees;

complianceValue.innerText=data.Compliance_Requirement;

threatValue.innerText=data.Main_Threat_Concern;

budgetValue.innerText=data.Security_Budget;

}
// ==========================================================
// CHARTS
// ==========================================================

function updateCharts(result){

drawProbabilityChart(result);

drawRiskGauge(result);

}

// ==========================================================
// PROBABILITY CHART
// ==========================================================

function drawProbabilityChart(result){

const canvas=document.getElementById("probabilityChart");

if(!canvas) return;

const ctx=canvas.getContext("2d");

if(probabilityChart){

probabilityChart.destroy();

}

const labels=[];
const values=[];

if(result.probabilities){

Object.entries(result.probabilities).forEach(([key,val])=>{

labels.push(key);

values.push(val);

});

}else if(result.recommendations){

result.recommendations.forEach(r=>{

labels.push(r.solution);

values.push(r.score);

});

}

probabilityChart=new Chart(ctx,{

type:"bar",

data:{

labels:labels,

datasets:[{

label:"Confidence",

data:values,

backgroundColor:[
"#00d4ff",
"#00ffb3",
"#3b82f6",
"#38bdf8",
"#14b8a6"
],

borderRadius:10

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

plugins:{

legend:{

display:false

}

},

scales:{

y:{

beginAtZero:true,

max:100

}

}

}

});

}

// ==========================================================
// RISK GAUGE
// ==========================================================

function drawRiskGauge(result){

const canvas=document.getElementById("riskGauge");

if(!canvas) return;

const ctx=canvas.getContext("2d");

if(riskGauge){

riskGauge.destroy();

}

const score=parseInt(result.risk_score)||0;

riskGauge=new Chart(ctx,{

type:"doughnut",

data:{

labels:["Risk","Remaining"],

datasets:[{

data:[score,100-score],

backgroundColor:[

"#ff5c5c",

"#23364f"

],

borderWidth:0

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

rotation:-90,

circumference:180,

plugins:{

legend:{

display:false

}

}

}

});

}

// ==========================================================
// RECOMMENDATION CARDS
// ==========================================================

function createRecommendationCards(result){

recommendationCards.innerHTML="";

if(!result.recommendations || !Array.isArray(result.recommendations)){

return;

}

result.recommendations.forEach(rec=>{

recommendationCards.innerHTML+=`

<div class="rec-card">

<h3>${rec.solution}</h3>

<p>

${rec.reason}

</p>

<p>

<b>Implementation:</b><br>

${rec.implementation}

</p>

<p>

<b>Business Impact:</b><br>

${rec.business_impact}

</p>

<div class="score">

${rec.score}%

</div>

</div>

`;

});

}
// ==========================================================
// VENDOR CARDS
// ==========================================================

function createVendorCards(result){

vendorCards.innerHTML = "";

// safety check
if(!result || !result.recommendations || !Array.isArray(result.recommendations)){
    vendorCards.innerHTML = `
    <div class="vendor-card">
        <h3>No Vendor Data Available</h3>
        <p>Backend response missing recommendations</p>
    </div>`;
    return;
}

let allVendors = [];

// extract vendors safely
result.recommendations.forEach(rec => {

    // FIX: handle multiple backend formats
    const vendors = rec.vendors || rec.Vendors || rec.vendor_list || [];

    if(Array.isArray(vendors) && vendors.length > 0){

        vendors.forEach(v => {

            allVendors.push({
                product: v.product || rec.solution || "Cybersecurity Tool",
                vendor: v.vendor || v.name || "Unknown Vendor",
                deployment: v.deployment || "Cloud/On-prem",
                cost: v.cost || "Contact Sales"
            });

        });

    }

});

// fallback if nothing comes
if(allVendors.length === 0){

    vendorCards.innerHTML = `
    <div class="vendor-card">
        <h3>Vendor Data Not Available</h3>
        <p>Your backend is not sending vendor recommendations.</p>
    </div>`;
    return;
}

// render cards
allVendors.forEach(vendor => {

vendorCards.innerHTML += `
<div class="vendor-card">

<h3>${vendor.product}</h3>

<p><b>Vendor:</b> ${vendor.vendor}</p>
<p><b>Deployment:</b> ${vendor.deployment}</p>
<p><b>Cost:</b> ${vendor.cost}</p>

</div>
`;

});

}

// ==========================================================
// PDF DOWNLOAD
// ==========================================================

if(downloadPdfBtn){

downloadPdfBtn.addEventListener("click",()=>{

window.print(); // simple PDF via browser print

});

}

// ==========================================================
// PRINT BUTTON (fallback)
// ==========================================================

if(printBtn){

printBtn.addEventListener("click",()=>{

window.print();

});

}

// ==========================================================
// INITIALIZATION
// ==========================================================

document.addEventListener("DOMContentLoaded",function(){

new TomSelect("#complianceSelect",{

plugins:["remove_button"],

placeholder:"Select Compliance Requirements",

maxItems:null

});

new TomSelect("#threatSelect",{

plugins:["remove_button"],

placeholder:"Select Threats",

maxItems:null

});

});

// ==========================================================
// ERROR SAFE HELPERS
// ==========================================================

window.addEventListener("error",(e)=>{

console.error("Global Error:",e.message);

});

// ==========================================================
// EXPORT GLOBAL FUNCTIONS (optional debugging)
// ==========================================================

window.starlightAI={

updateDashboard,

updateCharts,

createRecommendationCards,

createVendorCards

};
// ============================
// USER DROPDOWN WORKING
// ============================

const userTrigger = document.getElementById("userTrigger");
const userDropdown = document.getElementById("userDropdown");
const logoutBtn = document.getElementById("logoutBtn");

if(userTrigger){

userTrigger.addEventListener("click", () => {

    if(userDropdown.style.display === "flex"){
        userDropdown.style.display = "none";
    } else {
        userDropdown.style.display = "flex";
    }

});

}

// close when clicking outside
document.addEventListener("click", (e) => {

if(!e.target.closest("#userMenu")){
    if(userDropdown){
        userDropdown.style.display = "none";
    }
}

});

// logout (demo)
if(logoutBtn){

logoutBtn.addEventListener("click", () => {

    alert("Logged out successfully");
    location.reload();

});

}
function toggleVendor(selectId, groupId){

    const select = document.getElementById(selectId);
    const group = document.getElementById(groupId);

    function update(){
        group.style.display =
            select.value === "Yes" ? "block" : "none";
    }

    update();

    select.addEventListener("change", update);
}

toggleVendor("firewallInstalled","firewallVendorGroup");
toggleVendor("edrInstalled","edrVendorGroup");
toggleVendor("siemInstalled","siemVendorGroup");