import requests
import json

print("Uploading test HR policy to compliance engine...")
print("This will take 20-30 seconds — Claude is analyzing...\n")

with open("test_hr_policy.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/audit",
        files={"file": ("test_hr_policy.pdf", f, "application/pdf")}
    )

if response.status_code == 200:
    result = response.json()
    analysis = result["analysis"]

    print(f"{'='*55}")
    print(f"  COMPLIANCE SCORE: {analysis['overall_score']}/100")
    print(f"{'='*55}")
    print(f"\nSUMMARY:\n{analysis['summary']}")

    print(f"\nGAPS FOUND: {len(analysis['gaps'])}")
    print("-"*55)
    for i, gap in enumerate(analysis["gaps"], 1):
        severity = gap['severity'].upper()
        print(f"\n[{i}] {severity} — {gap['code']}")
        print(f"    Section : {gap['section']}")
        print(f"    Issue   : {gap['issue']}")
        print(f"    Fix     : {gap['compliant_text'][:120]}...")

    print(f"\n{'='*55}")
    print(f"COMPLIANT AREAS: {len(analysis.get('compliant_areas', []))}")
    for area in analysis.get("compliant_areas", []):
        print(f"  ✓ {area}")

    print("\nSaving full report to report.json...")
    with open("report.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Done. Open report.json to see the full output.")

else:
    print(f"ERROR {response.status_code}:")
    print(response.text)
