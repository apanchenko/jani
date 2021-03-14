# Jani backlog

## Todo

- black and white spam words lists
- categorize message theme to block deprecated themes
- welcome messages
- statistics
- configure custom bots selecting features
  - update channel admins
- vote for new features
  - payments
- debt
  - refactor using injector
  - builder image to decrease image size
  - tests
  - github action to deploy to DO
- save processed message offsets to not skip messages during restart
  - iter_messages not available to bot. Login as user? [lonami](https://t.me/TelethonChat/312114)
  - update telethon, research its catch_up
  - research using TDLib

## Done

- use compose and mongo
- performance monitoring separated in peano lib
- filter documents in private messages
- forward private messages between user and admin
- add /help command
- add /version command
- add /ping command
- deploy using DOCR
- add basic spam filter
- delete message about joined user
