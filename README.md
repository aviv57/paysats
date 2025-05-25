# Paysats Online

**Paysats Online** is a project aimed at creating a unified, email-like identity for Bitcoin users.  
Instead of managing multiple Bitcoin addresses or payment platforms, Paysats Online provides a single, memorable address format:

> `user@paysats.online`

This project is inspired by [lightning-address](https://github.com/andrerfneves/lightning-address).

---

## Live Demo

- **Main Page:** [paysats.online](https://paysats.online)  
- **Example User Profile:** [Aviv](https://paysats.online/u/aviv)

---

## How Client Integration Works

To resolve a Paysats address, clients should perform an HTTP `GET` request to the well-known endpoint:

```
https://<domain>/.well-known/paysats/<username>
```

### Example Request

```bash
curl https://paysats.online/.well-known/paysats/aviv
```

### Example Response

```json
{
  "contact": {
    "nickname": "aviv",
    "x": "@Aviv__BarEl",
    "email": "aviv@paysats.online",
    "nostr": "npub1mk6ht4a96tda4mzdkanjnzcznew3znv6tmmapwj3q0ne2ek8rj5q8vpf5q"
  },
  "bitcoin": {
    "address": "bc1qft4764g468c09rzv6huzjnzcfelzrva9mcjk75",
    "lightning_address": "aviv@paysats.online",
    "payment_url": "N/A",
    "silent_payments": "N/A"
  }
}
```

## Paysats Server

This repository contains a proof-of-concept server written in Python using FastAPI and Jinja2. It currently supports few endpoints:

- `/.well-known/paysats/<username>`  
  - Returns contact information and Bitcoin payment options.
- `/.well-known/lnurlp/<username>`  
  - Returns JSON as defined in [lightning-address](https://github.com/andrerfneves/lightning-address).
- `/.well-known/nostr.json`  
  - Returns NIP-05 public keys. See [NIP-05](https://github.com/nostr-protocol/nips/blob/master/05.md).

The server also provides a "linktree-style" profile page (mobile and desktop friendly) at:

> `https://<domain>/u/<username>`  

Example: [https://paysats.online/u/aviv](https://paysats.online/u/aviv)

---

## Alpha Notice

This project is currently in **alpha**. All users are hardcoded and not stored in a database.

If you’d like your payment details added, feel free to contact me at:

**aviv@paysats.online**