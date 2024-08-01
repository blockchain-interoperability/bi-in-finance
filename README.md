# Cross-Border Payments with Smart Contracts

Demo Video:
https://www.youtube.com/watch?v=BXOKMy0x-ng


A framework leveraging blockchain technology and smart contracts to emulate cross-border payments, ensuring interoperability and compliance with international standards such as ISO20022. 

![image](https://github.com/user-attachments/assets/2a6ccf94-4b66-4b6b-8fcc-63244c3f2ffa)


## Instructions

* Install Foundry : https://book.getfoundry.sh/getting-started/installation 
* foundry_project (cbpr_dapp/foundry_project) should be used to deploy the smart contract (use deploy_contracts.sh with your intended rpc_urls and deploy commands). It can also be used to run local blockchains in the local machine. Follow the instructions in cbpr_dapp/foundry_project.
* python3 and flask should be installed to run the web client.
* The smart contracts can be initialized from the web client with the information in sc_init.json.
* ISO20022 standard pacs.008 messages maybe used for testing the transaction process


### Cite

https://arxiv.org/abs/2407.19283

```
@misc{mridul2024smartcontractssmarterpayments,
      title={Smart Contracts, Smarter Payments: Innovating Cross Border Payments and Reporting Transactions}, 
      author={Maruf Ahmed Mridul and Kaiyang Chang and Aparna Gupta and Oshani Seneviratne},
      year={2024},
      eprint={2407.19283},
      archivePrefix={arXiv},
      primaryClass={cs.CE},
      url={https://arxiv.org/abs/2407.19283}, 
}
