[←   Back to Selected work](https://helloredwan.me/index.html#stage-work)   Privacy & market infrastructure

# How to choose a privacy solution on Ethereum

A practical way to compare privacy options around a real institutional transaction.

Redwan Meslem

Take a transfer of a tokenized private credit note. The buyer and seller need to know the price and amount. A transfer agent may need proof the buyer is eligible. An authorized reviewer may need access to the underlying record later. Putting the whole trade on a public ledger exposes more than those parties need. Keeping it entirely inside one institution makes it harder for other participants to verify what happened.

## Write down who can see what

Pick a transaction your team expects to run. List the fields, including identity, amount, price, timing, and position. For each field, specify who needs the original, who only needs proof of a condition, and who can grant or revoke access. Include the operator and vendors in that exercise. A system can hide data from the public and still expose it to the operator, or leak useful patterns through timing and repeated interactions.

## Compare the trust models

The EEA Privacy Working Group report profiles several ways to deliver confidentiality. Its 2026 edition includes Nightfall for confidential token transfers, Paladin for privacy groups, and Silent Data for execution in trusted hardware. These are starting points for a shortlist. The report draws on documentation and deployment evidence, with different levels of maturity across the products it covers.

- Zero-knowledge proofs.  A verifier can check a defined claim without seeing the inputs. Ask what the proof actually covers, where it is generated, and what remains visible onchain.
- Privacy groups.  A defined set of parties can share private state. Ask which members hold a copy, what happens when a member leaves, and how the group interacts with outside systems.
- Trusted hardware.  Sensitive data can be processed inside an isolated environment. Ask who operates it, how its configuration is verified, and what access or recovery looks like if the operator is unavailable.

## Run the same test with each provider

Give each provider the same transfer, with a permitted buyer, a rejected buyer, and an audit request. Check what each participant and the operator can see. Test key recovery, revocation, and how the transfer integrates with custody and settlement. Ask for evidence of a live deployment that resembles your use case, and record pilots and audit coverage separately.

The result should be a short list of controls the institution can explain and operate. That is a stronger basis for choosing a privacy solution than comparing cryptographic features in isolation.

## Sources

- [A field guide to privacy on Ethereum](https://entethalliance.org/eea-privacy-ethereum/)
- [EEA Privacy Working Group report](https://hub.entethalliance.org/wg-privacy/privacy-report.html)

Source: https://helloredwan.me/choosing-ethereum-privacy.html
