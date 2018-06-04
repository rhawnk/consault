from seed import seed_consul, seed_vault

def main():
  c = seed_consul.Consul()
  c.seed()
  v = seed_vault.Vault()
  v.seed()

if __name__== "__main__":
  main()
