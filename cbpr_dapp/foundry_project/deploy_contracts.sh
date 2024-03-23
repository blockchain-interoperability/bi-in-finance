#!/bin/bash

contract="src/FinancialInstitution.sol:FinancialInstitution"

# RPC URLs for the four Anvil instances
rpc_urls=(
    "http://localhost:8545"
    "http://localhost:8546"
    "http://localhost:8547"
    "http://localhost:8548"
)

private_keys=(
    "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"
    "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"
    "0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6"
    "0x47e179ec197488593b187f80a00eb0da91f1b9d0b13f8733639f19c30a34926a"
)

index=0
for key in "${private_keys[@]}"; do
    rpc_url=${rpc_urls[$index]}

    forge create --rpc-url="$rpc_url" --private-key="$key" "$contract"

    ((index++))
done
