# ==========================================================
# STARLIGHT AI
# Enterprise Cybersecurity Recommendation System
# app.py
# ==========================================================

from flask import Flask, render_template, request, jsonify

import pandas as pd
import numpy as np
import joblib
import logging
import traceback

# ==========================================================
# FLASK CONFIGURATION
# ==========================================================

app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

# ==========================================================
# LOAD MACHINE LEARNING MODEL
# ==========================================================

try:

    model = joblib.load("recommendation_model.pkl")

    label_encoder = joblib.load("label_encoder.pkl")

    logging.info("Model Loaded Successfully")

except Exception as e:

    logging.error("Unable to load model")

    logging.error(str(e))

    model = None

    label_encoder = None

# ==========================================================
# DEFAULT VALUES
# ==========================================================

DEFAULT_RISK_LEVEL = "Medium"

DEFAULT_CONFIDENCE = 0.0

MAX_RECOMMENDATIONS = 5
# ==========================================================
# ENTERPRISE CYBERSECURITY PRODUCT DATABASE
# ==========================================================

products = {

# ======================================================
# SIEM
# ======================================================

"SIEM Solution":[

{
"name":"Microsoft Sentinel",
"vendor":"Microsoft",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Splunk Enterprise Security",
"vendor":"Splunk",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"IBM QRadar",
"vendor":"IBM",
"deployment":"On-Premise",
"cost":"High"
},

{
"name":"Google Chronicle",
"vendor":"Google",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Elastic SIEM",
"vendor":"Elastic",
"deployment":"Hybrid",
"cost":"Medium"
}

],

# ======================================================
# EDR
# ======================================================

"EDR Platform":[

{
"name":"CrowdStrike Falcon",
"vendor":"CrowdStrike",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"SentinelOne Singularity",
"vendor":"SentinelOne",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Microsoft Defender for Endpoint",
"vendor":"Microsoft",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Sophos Intercept X",
"vendor":"Sophos",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Trend Vision One",
"vendor":"Trend Micro",
"deployment":"Cloud",
"cost":"Medium"
}

],

# ======================================================
# XDR
# ======================================================

"XDR Platform":[

{
"name":"Microsoft Defender XDR",
"vendor":"Microsoft",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Trend Vision One",
"vendor":"Trend Micro",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Cortex XDR",
"vendor":"Palo Alto",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"FortiXDR",
"vendor":"Fortinet",
"deployment":"Cloud",
"cost":"Medium"
}

],

# ======================================================
# IAM
# ======================================================

"IAM":[

{
"name":"Microsoft Entra ID",
"vendor":"Microsoft",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Okta Identity Cloud",
"vendor":"Okta",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Ping Identity",
"vendor":"Ping",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"OneLogin",
"vendor":"OneLogin",
"deployment":"Cloud",
"cost":"Low"
}

],

# ======================================================
# PAM
# ======================================================

"PAM":[

{
"name":"CyberArk",
"vendor":"CyberArk",
"deployment":"Hybrid",
"cost":"High"
},

{
"name":"BeyondTrust",
"vendor":"BeyondTrust",
"deployment":"Hybrid",
"cost":"High"
},

{
"name":"Delinea Secret Server",
"vendor":"Delinea",
"deployment":"Hybrid",
"cost":"Medium"
}

],

# ======================================================
# CASB
# ======================================================

"CASB":[

{
"name":"Microsoft Defender for Cloud Apps",
"vendor":"Microsoft",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Netskope",
"vendor":"Netskope",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Skyhigh Security",
"vendor":"Skyhigh",
"deployment":"Cloud",
"cost":"High"
}

],

# ======================================================
# CLOUD SECURITY
# ======================================================

"Cloud Security Platform":[

{
"name":"Prisma Cloud",
"vendor":"Palo Alto",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Wiz",
"vendor":"Wiz",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Lacework",
"vendor":"Fortinet",
"deployment":"Cloud",
"cost":"High"
}

],

# ======================================================
# MDR
# ======================================================

"MDR Service":[

{
"name":"CrowdStrike Falcon Complete",
"vendor":"CrowdStrike",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Sophos MDR",
"vendor":"Sophos",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Rapid7 MDR",
"vendor":"Rapid7",
"deployment":"Cloud",
"cost":"Medium"
}

],

# ======================================================
# SOC
# ======================================================

"SOC-as-a-Service":[

{
"name":"Arctic Wolf SOC",
"vendor":"Arctic Wolf",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Rapid7 SOC",
"vendor":"Rapid7",
"deployment":"Cloud",
"cost":"Medium"
}

],

# ======================================================
# WAF
# ======================================================

"WAF":[

{
"name":"Cloudflare WAF",
"vendor":"Cloudflare",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"AWS WAF",
"vendor":"Amazon",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Imperva WAF",
"vendor":"Imperva",
"deployment":"Cloud",
"cost":"High"
}

],

# ======================================================
# DLP
# ======================================================

"DLP Solution":[

{
"name":"Forcepoint DLP",
"vendor":"Forcepoint",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Microsoft Purview",
"vendor":"Microsoft",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Symantec DLP",
"vendor":"Broadcom",
"deployment":"Hybrid",
"cost":"High"
}

],

# ======================================================
# EMAIL SECURITY
# ======================================================

"Email Security Gateway":[

{
"name":"Proofpoint",
"vendor":"Proofpoint",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Mimecast",
"vendor":"Mimecast",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Microsoft Defender for Office 365",
"vendor":"Microsoft",
"deployment":"Cloud",
"cost":"Medium"
}

],

# ======================================================
# VULNERABILITY MANAGEMENT
# ======================================================

"Vulnerability Management":[

{
"name":"Tenable Nessus",
"vendor":"Tenable",
"deployment":"On-Premise",
"cost":"Medium"
},

{
"name":"Qualys VMDR",
"vendor":"Qualys",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Rapid7 InsightVM",
"vendor":"Rapid7",
"deployment":"Cloud",
"cost":"Medium"
}

],

# ======================================================
# THREAT INTELLIGENCE
# ======================================================

"Threat Intelligence Platform":[

{
"name":"Recorded Future",
"vendor":"Recorded Future",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Mandiant Threat Intelligence",
"vendor":"Google",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Anomali ThreatStream",
"vendor":"Anomali",
"deployment":"Cloud",
"cost":"High"
}

],

# ======================================================
# ZERO TRUST
# ======================================================

"ZTNA Solution":[

{
"name":"Zscaler ZPA",
"vendor":"Zscaler",
"deployment":"Cloud",
"cost":"High"
},

{
"name":"Cloudflare Zero Trust",
"vendor":"Cloudflare",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Prisma Access",
"vendor":"Palo Alto",
"deployment":"Cloud",
"cost":"High"
}

],

# ======================================================
# RANSOMWARE
# ======================================================

"Ransomware Protection":[

{
"name":"Sophos Intercept X",
"vendor":"Sophos",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Bitdefender GravityZone",
"vendor":"Bitdefender",
"deployment":"Cloud",
"cost":"Medium"
},

{
"name":"Microsoft Defender",
"vendor":"Microsoft",
"deployment":"Cloud",
"cost":"Medium"
}

],

# ======================================================
# ENCRYPTION
# ======================================================

"Data Encryption Platform":[

{
"name":"Thales CipherTrust",
"vendor":"Thales",
"deployment":"Hybrid",
"cost":"High"
},

{
"name":"Vormetric",
"vendor":"Thales",
"deployment":"Hybrid",
"cost":"High"
},

{
"name":"Microsoft Purview Encryption",
"vendor":"Microsoft",
"deployment":"Cloud",
"cost":"Medium"
}

]

}
# ==========================================================
# RISK CALCULATION ENGINE
# ==========================================================

def calculate_risk(data):

    score = 0

    # ======================================================
    # FIREWALL
    # ======================================================

    if data["Firewall_Installed"] == "No":
        score += 20
    else:
        score += 5

    # ======================================================
    # EDR
    # ======================================================

    if data["EDR_Installed"] == "No":
        score += 25
    else:
        score += 5

    # ======================================================
    # SIEM
    # ======================================================

    if data["SIEM_Installed"] == "No":
        score += 20
    else:
        score += 5

    # ======================================================
    # CLOUD USAGE
    # ======================================================

    cloud = data["Cloud_Usage"]

    if cloud == "High":
        score += 15

    elif cloud == "Medium":
        score += 8

    else:
        score += 3

    # ======================================================
    # EMPLOYEES
    # ======================================================

    employees = int(data["Employees"])

    if employees >= 10000:
        score += 15

    elif employees >= 5000:
        score += 12

    elif employees >= 1000:
        score += 8

    elif employees >= 500:
        score += 5

    else:
        score += 2

    # ======================================================
    # SECURITY BUDGET
    # ======================================================

    budget = data["Security_Budget"]

    if budget == "Very Low":
        score += 20

    elif budget == "Low":
        score += 12

    elif budget == "Medium":
        score += 6

    else:
        score += 2

    # ======================================================
    # INDUSTRY
    # ======================================================

    industry = data["Industry"].strip().lower()

    high_risk = [

        "banking",
        "finance",
        "healthcare",
        "government",
        "defense",
        "insurance"

    ]

    medium_risk = [

        "education",
        "manufacturing",
        "retail",
        "telecom"

    ]

    if industry in high_risk:

        score += 15

    elif industry in medium_risk:

        score += 8

    else:

        score += 4

    # ======================================================
    # THREAT CONCERN
    # ======================================================

    threat = data["Main_Threat_Concern"]

    if threat in [

        "Ransomware",
        "Data Breach",
        "APT",
        "Zero Day"

    ]:

        score += 15

    elif threat in [

        "Cloud Security",
        "IoT Attack",
        "DDoS"

    ]:

        score += 10

    else:

        score += 5

    # ======================================================
    # COMPLIANCE
    # ======================================================

    compliance = data["Compliance_Requirement"]

    if compliance in [

        "PCI-DSS",
        "HIPAA",
        "FISMA"

    ]:

        score += 10

    elif compliance in [

        "ISO27001",
        "SOC2",
        "NIST"

    ]:

        score += 7

    else:

        score += 5

    # ======================================================
    # LIMIT SCORE
    # ======================================================

    score = min(score, 100)

    # ======================================================
    # RISK LEVEL
    # ======================================================

    if score <= 30:

        level = "Low"

    elif score <= 55:

        level = "Medium"

    elif score <= 75:

        level = "High"

    else:

        level = "Critical"

    return score, level
# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

# ==========================================================
# GET PRODUCTS
# ==========================================================

def get_products(solution):

    # Exact Match

    if solution in products:

        return products[solution]

    # Ignore Case Match

    for key in products.keys():

        if key.lower() == solution.lower():

            return products[key]

    # Partial Match

    for key in products.keys():

        if solution.lower() in key.lower():

            return products[key]

        if key.lower() in solution.lower():

            return products[key]

    # Default Products

    return [

        {

            "name":"Microsoft Defender",

            "vendor":"Microsoft",

            "deployment":"Cloud",

            "cost":"Medium"

        },

        {

            "name":"CrowdStrike Falcon",

            "vendor":"CrowdStrike",

            "deployment":"Cloud",

            "cost":"High"

        },

        {

            "name":"Cisco SecureX",

            "vendor":"Cisco",

            "deployment":"Hybrid",

            "cost":"Medium"

        }

    ]


# ==========================================================

def generate_explanation(data, risk_level):

    return (

        f"Based on the organization's profile, "
        f"the industry '{data['Industry']}' with "
        f"'{data['Main_Threat_Concern']}' as the primary "
        f"security concern and compliance requirement "
        f"'{data['Compliance_Requirement']}' indicates "
        f"a {risk_level} cybersecurity risk. "
        f"The AI model has recommended the most suitable "
        f"security solution using machine learning and "
        f"enterprise cybersecurity best practices."

    )


# ==========================================================

# ==========================================================
# FORMAT VENDOR DATA
# ==========================================================

def format_vendor_data(solution):

    vendor_list = []

    available_products = get_products(solution)

    vendor_list.append({
        "name": solution,
        "products": [
            {
                "title": item["name"],
                "description": f"Vendor: {item['vendor']} | Deployment: {item['deployment']} | Cost: {item['cost']}"
            }
            for item in available_products
        ]
    })

    return vendor_list


# ==========================================================

def validate_request(data):

    required_fields = [

        "Industry",

        "Employees",

        "Cloud_Usage",

        "Firewall_Installed",

        "EDR_Installed",

        "SIEM_Installed",

        "Compliance_Requirement",

        "Main_Threat_Concern",

        "Security_Budget"

    ]

    for field in required_fields:

        if field not in data:

            return False, f"Missing field : {field}"

        if str(data[field]).strip() == "":

            return False, f"Empty field : {field}"

    return True, "Valid"


# ==========================================================

def preprocess_input(data):

    df = pd.DataFrame([{

        "Industry": data["Industry"],

        "Employees": int(data["Employees"]),

        "Cloud_Usage": data["Cloud_Usage"],

        "Firewall_Installed": data["Firewall_Installed"],

        "EDR_Installed": data["EDR_Installed"],

        "SIEM_Installed": data["SIEM_Installed"],

        "Compliance_Requirement": data["Compliance_Requirement"],

        "Main_Threat_Concern": data["Main_Threat_Concern"],

        "Security_Budget": data["Security_Budget"],

        "Risk_Level": DEFAULT_RISK_LEVEL

    }])

    return df


# ==========================================================

# ==========================================================
# TOP AI RECOMMENDATIONS
# ==========================================================

def get_top_recommendations(probabilities):

    top=np.argsort(probabilities)[::-1][:MAX_RECOMMENDATIONS]

    recommendations=[]

    for idx in top:

        solution=label_encoder.inverse_transform([idx])[0]

        recommendations.append({

            "solution":solution,

            "score":round(float(probabilities[idx]*100),2),

            "vendors":format_vendor_data(solution)

        })

    # Highest score first

    recommendations=sorted(

        recommendations,

        key=lambda x:x["score"],

        reverse=True

    )

    return recommendations
# ==========================================================
# HOME ROUTE
# ==========================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "running",

        "application": "STARLIGHT AI",

        "version": "2.0",

        "model_loaded": model is not None,

        "encoder_loaded": label_encoder is not None

    })


# ==========================================================
# MODEL STATUS
# ==========================================================

@app.route("/model-status")
def model_status():

    if model is None or label_encoder is None:

        return jsonify({

            "status": "error",

            "message": "Model not loaded."

        }), 500

    return jsonify({

        "status": "success",

        "message": "Model loaded successfully.",

        "classes": len(label_encoder.classes_),

        "recommendation_categories":
        label_encoder.classes_.tolist()

    })


# ==========================================================
# APPLICATION INFO
# ==========================================================

@app.route("/about")
def about():

    return jsonify({

        "application":
        "STARLIGHT AI Cybersecurity Recommendation System",

        "framework":
        "Flask",

        "machine_learning":
        "Scikit-Learn",

        "charting":
        "Chart.js",

        "prediction":
        "Multi-Class Classification",

        "recommendations":
        MAX_RECOMMENDATIONS

    })
# ==========================================================
# PREDICT API
# PART 1
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------------
        # CHECK MODEL
        # ----------------------------------------------

        if model is None or label_encoder is None:

            return jsonify({

                "status": "error",

                "message": "Machine Learning model is not loaded."

            }), 500

        # ----------------------------------------------
        # GET JSON DATA
        # ----------------------------------------------

        data = request.get_json()

        if data is None:

            return jsonify({

                "status": "error",

                "message": "Invalid JSON request."

            }), 400

        # ----------------------------------------------
        # VALIDATE REQUEST
        # ----------------------------------------------

        valid, message = validate_request(data)

        if not valid:

            return jsonify({

                "status": "error",

                "message": message

            }), 400

        # ----------------------------------------------
        # PREPROCESS INPUT
        # ----------------------------------------------

        client = preprocess_input(data)

        # ----------------------------------------------
        # CALCULATE RISK
        # ----------------------------------------------

        risk_score, risk_level = calculate_risk(

            client.iloc[0]

        )

        client["Risk_Level"] = risk_level

        # ----------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------

        prediction = model.predict(client)

        probabilities = model.predict_proba(client)[0]

        primary_solution = label_encoder.inverse_transform(

            prediction

        )[0]

        confidence = round(

            float(np.max(probabilities) * 100),

            2

        )

        # ----------------------------------------------
        # BUILD RECOMMENDATIONS
        # ----------------------------------------------

        recommendations = get_top_recommendations(

            probabilities

        )

        explanation = generate_explanation(

            data,

            risk_level

        )
                # ----------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------

        return jsonify({

            "status": "success",

            "risk_score": risk_score,

            "risk_level": risk_level,

            "primary_solution": primary_solution,

            "confidence": confidence,

            "recommendations": recommendations,

            "explanation": explanation

        })

    # ----------------------------------------------
    # ERROR HANDLING
    # ----------------------------------------------

    except Exception as e:

        logging.error("Prediction Error")

        logging.error(traceback.format_exc())

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500
    # ==========================================================
# GLOBAL ERROR HANDLERS
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "status": "error",

        "code": 404,

        "message": "Requested resource not found."

    }),404


# ==========================================================

@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({

        "status":"error",

        "code":405,

        "message":"Method not allowed."

    }),405


# ==========================================================

@app.errorhandler(500)
def internal_server_error(error):

    logging.error(error)

    return jsonify({

        "status":"error",

        "code":500,

        "message":"Internal server error."

    }),500


# ==========================================================
# BEFORE REQUEST
# ==========================================================

@app.before_request
def before_request():

    logging.info(

        f"{request.method} {request.path}"

    )


# ==========================================================
# AFTER REQUEST
# ==========================================================

@app.after_request
def after_request(response):

    response.headers["Cache-Control"]="no-store"

    response.headers["Pragma"]="no-cache"

    response.headers["Expires"]="0"

    return response


# ==========================================================
# START APPLICATION
# ==========================================================

if __name__=="__main__":

    print("\n")

    print("==============================================")

    print(" STARLIGHT AI")

    print(" Enterprise Cybersecurity Recommendation System")

    print("==============================================")

    print(" Flask Server Starting...")

    print(" URL : http://127.0.0.1:5000")

    print("==============================================")

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
    