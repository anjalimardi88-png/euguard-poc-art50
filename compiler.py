import yaml
print("Compiling Policy to Rego...")
with open('policy.yaml','r') as f:
    p = yaml.safe_load(f)[0]
rego = f"""
package euguard.art50
default allow = false
allow {{
    input.actor == "{p['actor']}"
    input.obligation == "{p['obligation']}"
}}
"""
with open('policy.rego','w') as out:
    out.write(rego)
print("✅ policy.rego toiri holo")
