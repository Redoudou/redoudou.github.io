[←   Back to Selected work](https://helloredwan.me/index.html#stage-work)   Identity & tokenization

# A passport for tokenized markets

How shared eligibility credentials could help assets circulate across Ethereum networks.

Redwan Meslem

Consider a bank issuing a tokenized security that it wants to distribute through two venues on different Ethereum networks. The asset can be issued onchain, but each venue still needs to determine who is eligible to hold it. If the issuer, custodian, and transfer agent all use different formats for the same checks, adding a venue means building another integration and often asking investors for the same information again.

## What passports got right

ICAO’s machine-readable passport standards gave border authorities a common way to read a document. Countries still issue their own passports and decide whom to admit. The same distinction matters for securities. An issuer can accept eligibility claims in a shared format while deciding which providers it trusts and which rules apply to its asset. A venue that checks residency and a venue that checks accreditation can interpret the same credential and reach different decisions.

## What Shibui tests

Shibui is an open-source research prototype that connects ERC-3643 security tokens to credentials issued through the Ethereum Attestation Service. A token can check whether an approved provider issued a claim, whether its contents meet the token’s policy, and whether it has expired or been revoked. The issuer controls the policy and the set of trusted providers.

Using the same schema on two networks lets the institutions reuse the format and the integration logic. Shibui’s prototype still issues attestations separately on each chain. An institution that wants an asset to circulate across networks must also decide how the asset’s supply and ownership stay consistent, how settlement instructions move, and how updates to eligibility are reflected on each network. A shared credential tackles one part of that larger problem.

## What an institutional pilot should prove

Start with two venues, one instrument, and two policies. Have both venues read the same eligibility schema, then test a transfer that one venue accepts and the other rejects. Expire one credential and revoke another. Check that the next transfer is handled correctly on each network and that the transfer agent can explain the decision from its audit trail.

If that works, measure which onboarding steps and integrations the venues can actually reuse. The outcome that matters is whether adding a venue gets easier while issuers keep control over who can hold and transfer the asset.

## Sources

- [The Passport Problem on LinkedIn](https://www.linkedin.com/pulse/passport-problem-why-tokenized-markets-need-shared-identity-meslem-iryvf)
- [Shibui prototype and specification](https://hub.entethalliance.org/rnd-rwa-erc3643-eas/)
- [ERC-3643 token standard](https://eips.ethereum.org/EIPS/eip-3643)

## Related work

- [The EIP Matrix](https://intelligence.entethalliance.org/eip-matrix.html)

Source: https://helloredwan.me/passport-for-tokenized-markets.html
