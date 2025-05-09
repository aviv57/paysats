# Paysats Online

**Paysats Online** is a project focused on creating a unified, email-like address for Bitcoin users.  
Instead of managing separate bitcoin addresses or payment platforms, Paysats Online introduces a single memorable address:

This projects is inspired by https://github.com/andrerfneves/lightning-address

## Live Demo:
Main page: [paysats.online](https://paysats.online)

User profile page: [Aviv](https://paysats.online/u/aviv)

## Client Integration with Paysats Addresses
To resolve a Paysats address, clients must perform an HTTP `GET` request to the following well-known endpoint:

`https://domain.com/.well-known/paysats/<USER>`

### Example request and response
```bash
curl https://paysats.online/.well-known/paysats/aviv
```
```js
{
  "contact": {
    "nickname": "aviv",
    "x": "@Aviv__BarEl",
    "email": "aviv@paysats.online",
    "nostr": "npub1mk6ht4a96tda4mzdkanjnzcznew3znv6tmmapwj3q0ne2ek8rj5q8vpf5q"
  },
  "bitcoin": {
    "address": "bc1qft4764g468c09rzv6huzjnzcfelzrva9mcjk75",
    "xpub": "N/A",
    "lightning_address": "aviv@paysats.online",
    "payment_url": "N/A",
    "silent_payments": "N/A"
  }
}
```


## Paysats standard
Paysats standard is a new standard for any application to get Bitcoin payment options and contact information about
any person willing to recieve a bitcoin payment.
The Paysats standard addresses looks like an email / lightning address user@domain.com
In order to retrieve payment options client should make a GET request to the following endpoint: `http://domain.com/.well-known/paysats/<username>`


## Paysats server
This repo contains a POC server written in Python, with fastapi and Jinja2 to serve three endpoints
- `http://server.com/.well-known/paysats/<username>` - This endpoint will return contact infromation about the user and bitcoin payment options
- `http://server.com/.well-known/lnurlp/<username>` - This endpoint should return a json like defined in [lightning-address](https://github.com/andrerfneves/lightning-address)
- `http://server.com/.well-known/nostr.json` - This endpoint will return NIP-05 related public keys (See: https://github.com/nostr-protocol/nips/blob/master/05.md)

This server also serve a "linktree" like page available from mobile / desktop under the following url:
`http://server.com/u/<username>` you can see here an example: https://paysats.online/u/aviv


## Note
The project is now in alpha stage, so all users are hardcoded and not fetched from DB,
if you want me to add your payment details you can contact me via email on aviv@paysats.online
