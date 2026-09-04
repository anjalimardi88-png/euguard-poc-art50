import yaml

print("Compiling policy.yaml to Rego...")

with open('policy.yaml', 'r') as f:
    data = yaml.safe_load(f)
    policy = data[0]

rego_content = f'''package euguard.art50

default allow = false

allow {{
    input.actor == "{policy['actor']}"
    input.obligation == "{policy['obligation']}"
}}
'''

with open('policy.rego', 'w') as out:
    out.write(rego_content)

print("Compiled successfully to policy.rego")
