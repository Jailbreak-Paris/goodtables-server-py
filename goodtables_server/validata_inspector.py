from goodtables import Inspector

checks = ['structure', 'schema']

checks.append({"french-siret-value": {"column": "ACHETEURS_ID"}})

inspector = Inspector(checks=checks)
