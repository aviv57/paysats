<pre>
  BIP: XXX
  Layer: Applications
  Title: Well-Known Bitcoin Identity Endpoint
  Author: Aviv Bar-el <aviv57@gmail.com>
  Status: Proposed
  Type: Standards Track
  Created: 2025-05-15
</pre>

## Introduction

### Abstract

This BIP proposes a standardized way for Bitcoin wallets and related software to retrieve contact and payment information using a simple HTTPS GET request to a `.well-known` endpoint. Inspired by the Lightning Address specification, this mechanism supports on-chain, off-chain, and identity metadata lookups, enabling richer identity-based interoperability in the Bitcoin ecosystem.

### Copyright

This BIP is licensed under the BSD 2-clause license.

### Motivation

Today, users can receive Bitcoin through various methods—such as Lightning Addresses, static on-chain addresses, or dynamic addresses generated per payment. However, there is no unified and interoperable standard for resolving a user's identity (e.g., `user@domain.com`) into these different formats.

While the Lightning Address standard has demonstrated utility, it is limited to Lightning-specific use cases. This BIP generalizes the concept, enabling wallets and applications to resolve a single identity into a broader set of Bitcoin-related payment and contact methods.

## Specification

Clients should query:
```plain
https://<domain>/.well-known/bipXXX/<username>
```

Servers must respond with a valid JSON document in the following structure:

```json
{
  "contact": {
    "nickname": "Alice",
    "x": "@Alice",
    "email": "alice@gmail.com",
    "nostr": "nprofile1......"
  },
  "bitcoin": {
    "address": "bc1q......",
    "lightning_address": "alice@walletofsatoshi.com",
    "payment_url": "N/A",
    "silent_payments": "N/A"
  }
}
```

## Reference Implementation

A working proof-of-concept server is live at:
https://paysats.online/
Source code:
https://github.com/aviv57/paysats

This implementation can be easily forked and self-hosted by anyone, minimizing reliance on third parties and reducing centralization risk.

## Example usage

You can test it out your self using the following command
```bash
curl https://paysats.online/.well-known/paysats/sni | jq
```
Note: The current path uses .well-known/paysats as a placeholder.
Once this proposal is assigned a BIP number, it is expected to be updated to:
.well-known/bipXXX


## Relationship to Existing Work

This BIP shares common goals with BIP 353 ("DNS Rather than HTTP-based solutions"), which also aims to improve identity resolution for Bitcoin and Lightning Address usage.
While BIP 353 proposes a DNS-based approach to avoid reliance on HTTPS and centralized infrastructure,
this BIP takes a more flexible and extensible route using a `.well-known` HTTPS endpoint.

Both approaches are complementary. BIP 353 prioritizes privacy and decentralization, whereas this BIP emphasizes metadata richness.
Wallets and other softwares may choose to support one or both mechanisms depending on user preferences and application context.


## Inspired by:

- Lightning Address
  https://github.com/andrerfneves/lightning-address

- NIP-05 (Nostr Identifier Protocol)
  https://github.com/nostr-protocol/nips/blob/master/05.md