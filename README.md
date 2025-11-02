# BlockYoutubeInPfsenseDNS

If you need to temporarely block access to youtube (for instance if your children 
are using it on the smart tv when not supervised) using DNS, BlockYoutubeInPfsenseDNS
might be your solution.

## Installation

### Prerequesites:

- You need a firewall running pfsense (working successful with CE 2.8.1)
- On that firewall you have API access enabled using the package pfrest (https://pfrest.org/); export
an API key as documented on that page (https://pfrest.org/AUTHENTICATION_AND_AUTHORIZATION/#api-key-authentication)
- You need to provide your details (IP of pfsense and API key) in the .env file

## Technologies

- Python
- Packages
  - os
  - requests
  - environs

## Authors and contributors

Michael Pilgermann (kickkasch@posteo.de)

## Change log

- 2025-11-02 Initial import: backend (access to firewall via API) fully functional - frontend tbd 

## License
MIT License
See LICENSE.txt