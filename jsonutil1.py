## GoldStandard_v5.xlsx

import pandas as pd
import json
import os

# Specify the dataset directory
base_dir = r"D:\\다운로드\\dataset\\dataset"  ## 파일 저장 위치 변경 

# Load the Excel file
ctcn_path = os.path.join(base_dir, 'GoldStandard_v5.xlsx')

# Load the data
ctcn_df = pd.read_excel(ctcn_path)

# Specify columns for actual and observed values
columns_to_compare = {
    "GS": [
        "Tumor Profile.Morphology_status_pCR_GS",
        "Tumor Marker Test Profile.Code_Value_ER_GS",
        "Tumor Marker Test Profile.Code_Value_PR_GS",
        "Tumor Marker Test Profile.Code_Value_HER2_GS",
        "Tumor Marker Test Profile.Code_Value_KI67_GS",
        "Primary Cancer Condition Profile.Code_clinicalStatus_IDC_GS",
        "Primary Cancer Condition Profile.Code_clinicalStatus_DCIS_GS",
        "Primary Cancer Condition Profile.Code_clinicalStatus_ILC_GS",
        "Primary Cancer Condition Profile.Code_clinicalStatus_LCIS_GS"
    ],
    "AI": [
        "Tumor Profile.Morphology_status_pCR_AI",
        "Tumor Marker Test Profile.Code_Value_ER_AI",
        "Tumor Marker Test Profile.Code_Value_PR_AI",
        "Tumor Marker Test Profile.Code_Value_HER2_AI",
        "Tumor Marker Test Profile.Code_Value_KI67_AI",
        "Primary Cancer Condition Profile.Code_clinicalStatus_IDC_AI",
        "Primary Cancer Condition Profile.Code_clinicalStatus_DCIS_AI",
        "Primary Cancer Condition Profile.Code_clinicalStatus_ILC_AI",
        "Primary Cancer Condition Profile.Code_clinicalStatus_LCIS_AI"
    ],
    "Human": [
        "Tumor Profile.Morphology_status_pCR_Human",
        "Tumor Marker Test Profile.Code_Value_ER_Human",
        "Tumor Marker Test Profile.Code_Value_PR_Human",
        "Tumor Marker Test Profile.Code_Value_HER2_Human",
        "Tumor Marker Test Profile.Code_Value_KI67_Human",
        "Primary Cancer Condition Profile.Code_clinicalStatus_IDC_Human",
        "Primary Cancer Condition Profile.Code_clinicalStatus_DCIS_Human",
        "Primary Cancer Condition Profile.Code_clinicalStatus_ILC_Human",
        "Primary Cancer Condition Profile.Code_clinicalStatus_LCIS_Human"
    ]
}

# Function to create grouped JSON data for GS/AI comparison
def create_gs_ai_json():
    grouped_data = {"data": {"values": []}}
    
    for col_gs, col_ai in zip(columns_to_compare["GS"], columns_to_compare["AI"]):
        # Group by actual and observed AI values and count occurrences
        group = (
            ctcn_df.groupby([col_gs, col_ai])
            .size()
            .reset_index(name="count")
        )
        
        # Add each group to the JSON structure
        for _, row in group.iterrows():
            grouped_data["data"]["values"].append({
                "actual": [col_gs, row[col_gs]],
                "observed": [col_ai, row[col_ai]],
                "count": row["count"]
            })

    # Save the JSON data to a file
    output_path = os.path.join(base_dir, 'GS_AI_Comparison.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(grouped_data, f, ensure_ascii=False, indent=4)

    print(f"JSON file created at: {output_path}")

# Function to create grouped JSON data for GS/Human comparison
def create_gs_human_json():
    grouped_data = {"data": {"values": []}}
    
    for col_gs, col_human in zip(columns_to_compare["GS"], columns_to_compare["Human"]):
        # Group by actual and observed Human values and count occurrences
        group = (
            ctcn_df.groupby([col_gs, col_human])
            .size()
            .reset_index(name="count")
        )
        
        # Add each group to the JSON structure
        for _, row in group.iterrows():
            grouped_data["data"]["values"].append({
                "actual": [col_gs, row[col_gs]],
                "observed": [col_human, row[col_human]],
                "count": row["count"]
            })

    # Save the JSON data to a file
    output_path = os.path.join(base_dir, 'GS_Human_Comparison.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(grouped_data, f, ensure_ascii=False, indent=4)

    print(f"JSON file created at: {output_path}")

# Run the functions to create JSON files
create_gs_ai_json()
create_gs_human_json()
