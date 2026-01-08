This will be a site that will help countless of spinning instructors all over the world.
Our plan is to make a tool that helps immensly.

all of this will only be possible because spotify did an ~~awesome~~ stupid job with their API. They don't allow us to get the bpm :(


i dont have time to make a good readme i have to get back to coding

The site: not online yet

>":3" - moos4 2025

below here is some information for drad:
#### users.json (hoe het nu is)
{
"admin": "password",
"username": "password"
}

## de shit die ik wil doen

### files

#### usernames.json
{
"username": "user id"
}

#### emails.json
{
"email": "user id"
}

#### users.json
{
"user id": {
  "username": "username",
  "email": "email",
  "password": "password",
  "premium": true/false
  }
}


### Script plan:

#js: in script wanneer je inlogt stuurt hij de username/email input door en de password input

#py: als het aankomt checkt hij eerst of de username/email een email endpoint heeft (e.g. @gmail.com, @hotmail.com, @laurenslyceum.nl)

#py: als het een email endpoint heeft checkt hij in de emails.json of die een account eraan heeft, zo niet stuurt hij de wrong username/password message naar website

py: als het wel een account heeft haalt hij de user id en in users.json haalt hij de password bij die id en checkt of het klopt met de password input

py: als het klopt stuurt hij dat naar de servern en zo niet de worng shit message

Py: als de username/emaill geen email endpoint heeft (e.g. persoon1234) dan doet hij exact het zelfde als bij de email, maar dan chekt hij in usernames.json

### notes

de user id zal gewoon een optellend cijfer zijn per user, dus als er 5 accounts zijn gemaakt, bestaan de user id's 0, 1, 2, 3, 4.

shit met premium zullen we later fixen

### sign up

in de sign up screen zal hij ook om een email vragen en voordat hij het account maakt sturen we een email naar dat adres wat of een link bevat die ons het laat checken of een 6 cijferige code die de user moet invoeren om zijn email te verifieren (de email word waarschijnlijk in de .py gestuurd)

side note: we kunnen de email adressen verkopen aan bedrijven die er reclame naar kunnen sturen (dit is iets wat heel veel bedrijven doen)

### toekomstige ideeën

we kunnen user data storen in de users.json zoals de lessen die ze gemaakt hebben, het gelinkte spotify account, laatste login (zal zo meer over praten), en veel andere stats.

als de user 1 jaar (kan tijd veranderen) niet heeft ingelogt zullen we een mail sturen naar zijn emailadres waarin we dat zeggen en dat ze een keer moeten inloggen, want als ze een maand na die email nog steeds niet zijn ingelogd zullen we het account wat erbij hoort verwijderen.