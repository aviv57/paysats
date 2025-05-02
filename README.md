# Paysats Online

**Paysats Online** is a project focused on creating a unified, email-like address for Bitcoin users.  
Instead of managing separate identifiers across different platforms and payment methods, Paysats Online introduces a single memorable address:

This projects is inspired by https://github.com/andrerfneves/lightning-address

## Client Integration with Paysats Addresses
To resolve a Paysats address, clients must perform an HTTP `GET` request to the following well-known endpoint:

`https://domain.com/.well-known/paysats/<USER>`

The response will be a structured JSON with contact information like mail, nostr profile, etc.
and with bitcoin payment related details, for example silent payment address or an xpub.